from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import calendar
import holidays
import json
import os
import time

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#templatesフォルダを使うという設定
templates = Jinja2Templates(directory="templates")

#スケジュール保存先のファイルパス
DATA_FILE = "schedules.json"
GROUP_FILE = "groups.json"
groups = {}

#起動時にファイルからデータを読み込む関数
def load_schedules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

#初回起動時に読み込み
schedules = load_schedules()

#バラバラな順番で保存されているデータがあれば、起動時にソートし直す
for date in schedules:
    schedules[date].sort(key=lambda x: x.get("time", "23:59"))

#データをファイルに保存する関数
def save_to_file():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=4)
                                # ↑ これがないと日本語が文字化けする


#グループ機能
#起動時にグループを読み込む
if os.path.exists(GROUP_FILE):
    with open(GROUP_FILE, "r", encoding="utf-8") as f:
        groups = json.load(f)
        
def save_groups():
    with open(GROUP_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)
        

#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root(request: Request, year: int = 2026, month: int = 3):
    # calendar.monthcalendar(年、月)を使って、指定された月のデータを生成
    cal = calendar.monthcalendar(year, month)
    
    jp_holidays = holidays.Japan(years=year, language="ja")
    
    #曜日リスト(HTMLで表示する用)
    week_days = ["月", "火", "水", "木", "金", "土", "日"]
    
    #予定データのキーを月ごとに判定しやすくするために年、月もHTMLに渡す
    return templates.TemplateResponse("index.html",{
        "request": request,
        "title": f"{year}年 {month}月",
        "year": year,
        "month": month,
        "week_days": week_days,
        "cal": cal, # 2次元のリスト（リストの中にリストが入っている状態）を送る
        "jp_holidays": jp_holidays, #祝日データを送る
        "schedules": schedules, #schedule変数（保存済みデータ）もHTMLに送る
        "groups": groups
    })
    
#スケジュールを受け取るためのルート
@app.post("/save_schedule")
async def save_schedule_api(request: Request):
    data = await request.json()
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    
    #届いたデータ（タイトル、時間、メモ等）を丸ごと保存
    new_entry = {
        "title": data.get("title"),
        "time": data.get("time") if data.get("time") else "23:59", #時間未入力なら最後尾に
        "group_id": data.get("group_id"),
        "memo": data.get("memo"),
        "is_locked": data.get("is_locked", False)
    }
    
    #2026-02-xx というキーで保存
    date_key = f"{year}-{int(month):02d}-{int(day):02d}"
    
    if date_key not in schedules:
        schedules[date_key] = [] #その日の予定リストが無い場合は作成する
    
    schedules[date_key].append(new_entry) #リストに予定を追加
    
    #timeを基準に並び替える
    schedules[date_key].sort(key=lambda x: x["time"])
    
    #辞書を更新した後にファイルにも書き出す
    save_to_file()
    
    return {"status": "success"}

@app.post("/delete_schedule")
async def delete_schedule_api(request: Request):
    data = await request.json()
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    index = data.get("index") #消したい予定が何番目にあるかを受け取る
    
    date_key = f"{year}-{int(month):02d}-{int(day):02d}"
    
    #もしデータがあれば削除する
    if date_key in schedules:
        try:
            # Pythonのリストから「〇番目」の要素を取り除く
            schedules[date_key].pop(index)
            
            # もしその日の予定がゼロになったら、キー自体を消す
            if not schedules[date_key]:
                del schedules[date_key]
                
            save_to_file()
        except IndexError:
            pass # 指定された番号がなければ何もしない
        
    return {"status": "success"}


#グループ作成
@app.post("/create_group")
async def create_group_api(request: Request):
    data = await request.json()
    name = data.get("name")
    color = data.get("color")
    
    #IDを自動生成 
    group_id = f"group_{int(time.time())}"
    groups[group_id] = {"name": name, "color":color}
    
    save_groups()
    return {"status": "success", "group_id": group_id}