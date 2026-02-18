from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import calendar

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#templatesフォルダを使うという設定
templates = Jinja2Templates(directory="templates")

#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root(request: Request):
    #2026年2月のカレンダーを生成
    #monthcalendar(年,月)は1週間ごとのリストを返す。その月に含まれていない日(今回の場合3/1等)は 0 として帰ってくる
    cal = calendar.monthcalendar(2026, 2)
    
    #曜日リスト(HTMLで表示する用)
    week_days = ["月", "火", "水", "木", "金", "土", "日"]
    
    return templates.TemplateResponse("index.html",{
        "request": request,
        "title": "2026年 2月",
        "week_days": week_days,
        "cal": cal # 2次元のリスト（リストの中にリストが入っている状態）を送る
    })