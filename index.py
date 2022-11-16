import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>蕭莉瓊Python讀取Firestore</h1>"
    homepage = "<h1>蕭莉瓊的求職網頁</h1>"
    homepage += "<a href=/me1>個人簡介</a><br>"
    homepage += "<a href=/career>職涯測驗</a><br>"
    homepage += "<a href=/me>自傳簡介</a><br>"
    homepage += "<a href=/MIS>MIS工作</a><br>"
    homepage += "<br><a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
    return homepage

@app.route("/me1")
def route():
    return render_template("me1.html")

@app.route("/career")
def career():
    return render_template("career.html")

@app.route("/me")
def me():
    return render_template("me.html")

@app.route("/MIS")
def MIS():
    return render_template("MIS.html")

@app.route("/movie")
def movie():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    lastUpdate = sp.find("div", class_="smaller09").text[5:]

    for item in result:
        picture = item.find("img").get("src").replace(" ", "")
        title = item.find("div", class_="filmtitle").text
        movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
        show = item.find("div", class_="runtime").text.replace("上映日期：", "")
        show = show.replace("片長：", "")
        show = show.replace("分", "")
        showDate = show[0:10]
        showLength = show[13:]

        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "lastUpdate": lastUpdate
         }

        doc_ref = db.collection("電影").document(movie_id)
        doc_ref.set(doc)
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate 

@app.route("/search", methods=["POST","GET"])
def search():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""     
        collection_ref = db.collection("電影")
#       docs = collection_ref.where("title","==", "夜鷹的單戀").get()  
        for doc in docs:
            if MovieTitle in doc.to_dict()["title"]:
            info += "片名：" + doc.to_dict()["title"] + "<br>" 
            info += "海報：" + doc.to_dict()["picture"] + "<br>"
            info += "影片介紹：" + doc.to_dict()["hyperlink"] + "<br>"
            info += "片長：" + doc.to_dict()["showLength"] + " 分鐘<br>" 
            info += "上映日期：" + doc.to_dict()["showDate"] + "<br><br>"           
        return info
    else:  
        return render_template("input.html")

if __name__ == "__main__":
    app.run()
