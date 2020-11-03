import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbrebook

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list', methods=['GET'])
def showBooks():
    result = list(db.books.find({},{'_id':0}))
    return jsonify({'result':'success','books':result})


@app.route('/list', methods=['POST'])
def postBook():
    url = request.form['url_give']
    tag = request.form['tag_give']
    quote = request.form['quote_give']
    comment = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    img = soup.select_one('#yDetailTopWrap > div.topColLft > div.gd_imgArea > span > em > img')
    author = soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth > a').text
    img_url = img['src']
    title = img['alt']

    book = {
        'img':img_url,
        'tag':tag,
        'title':title,
        'author':author,
        'quote':quote,
        'comment':comment,
        'url':url
    }

    db.books.insert_one(book)
    return jsonify({'result':'success','msg':title + ': 저장되었습니다.'})


@app.route('/list/del', methods=['POST'])
def delBook():
    title = request.form['title']
    db.books.delete_one({'title':title})
    return jsonify({'result':'success','msg':title + ': 삭제되었습니다.'})


@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['pw']
    if id=="yeny" and pw=="yeny":
        return jsonify({'result':'success','msg':'로그인 성공!'})


if __name__ == '__main__':
    app.run()
