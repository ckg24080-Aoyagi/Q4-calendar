#（超重要）Dockerfileを書き換えた時はdockerをビルドしなおす


#ベースとなるPythonが入ったOSを選ぶ
FROM python:3.11-slim

#作業する部屋（フォルダ）を決める
WORKDIR /app

#必要な道具をインストールする
RUN pip install fastapi uvicorn jinja2 holidays
#                                       ↑祝日判定ライブラリ

#自分のパソコンにあるファイルを箱の中（コンテナ）にコピーする
COPY . .

#アプリを起動するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
                #↑ main.py の中にある app というインスタンスを探してという意味