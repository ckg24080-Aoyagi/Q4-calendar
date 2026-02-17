from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#templatesフォルダを使うという設定
templates = Jinja2Templates(directory="templates")

#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root(request: Request):
    #index.htmlを表示し、titleという変数に文字を入れて送る
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "マイ・スケジュール管理"
    })