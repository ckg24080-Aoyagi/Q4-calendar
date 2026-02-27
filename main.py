from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import calendar
import holidays
import json
import os

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#templatesフォルダを使うという設定
templates = Jinja2Templates(directory="templates")

#スケジュール保存先のファイルパス
DATA_FILE = "schedules.json"

#起動時にファイルからデータを読み込む関数
def load_schedules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

#初回起動時に読み込み
schedules = load_schedules()

#データをファイルに保存する関数
def save_to_file():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=4)
                                # ↑ これがないと日本語が文字化けする


#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root(request: Request, year: int = 2026, month: int = 2):
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
        "schedules": schedules #schedule変数（保存済みデータ）もHTMLに送る
    })
    
#スケジュールを受け取るためのルート
@app.post("/save_schedule")
async def save_schedule_api(request: Request):
    data = await request.json()
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    text = data.get("text")
    
    #2026-02-xx というキーで保存
    date_key = f"{year}-{int(month):02d}-{int(day):02d}"
    schedules[date_key] = text
    
    #辞書を更新した後にファイルにも書き出す
    save_to_file()
    
    return {"status": "success"}

@app.post("/delete_schedule")
async def delete_schedule_api(request: Request):
    data = await request.json()
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")
    
    date_key = f"{year}-{int(month):02d}-{int(day):02d}"
    
    #もしデータがあれば削除する
    if date_key in schedules:
        del schedules[date_key]
        save_to_file() #ファイルも同時に更新
        
    return {"status": "success"}