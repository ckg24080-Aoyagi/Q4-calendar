from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import calendar
import holidays

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#templatesフォルダを使うという設定
templates = Jinja2Templates(directory="templates")

#スケジュール保存用の変数を用意
schedules = {} #{ "2026-02-11": "建国記念日", ... } 形式での保存

#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root(request: Request):
    jp_holidays = holidays.Japan(years=2026)
    
    #monthcalendar(年,月)は1週間ごとのリストを返す。その月に含まれていない日(今回の場合3/1等)は 0 として帰ってくる
    cal = calendar.monthcalendar(2026, 2)
    
    #曜日リスト(HTMLで表示する用)
    week_days = ["月", "火", "水", "木", "金", "土", "日"]
    
    return templates.TemplateResponse("index.html",{
        "request": request,
        "title": "2026年 2月",
        "week_days": week_days,
        "cal": cal, # 2次元のリスト（リストの中にリストが入っている状態）を送る
        "jp_holidays": jp_holidays, #祝日データを送る
        "schedules": schedules #schedule変数（保存済みデータ）もHTMLに送る
    })
    
#スケジュールを受け取るためのルート
@app.post("/save_schedule")
async def save_schedule_api(request: Request):
    data = await request.json()
    day = data.get("day")
    text = data.get("text")
    
    #2026-02-xx というキーで保存
    date_key = f"2026-02-{int(day):02d}"
    schedules[date_key] = text
    
    return {"status": "success"}