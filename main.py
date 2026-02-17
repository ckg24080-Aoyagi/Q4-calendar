from fastapi import FastAPI

#FastAPI の app(アプリの本体) を作る
app = FastAPI()

#ブラウザでトップページ(/)にアクセスしたときの動きを決める
@app.get("/")
def read_root():
    return {"message": "Hello, Calendar App!"}