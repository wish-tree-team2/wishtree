# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.title} {self.artist} 추천 by {self.username}'

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    name = '최지웅'
    motto = "행복해서 웃는게 아니라 웃어서 행복합니다."

    context = {
        "name": name,
        "motto": motto,
    }
    return render_template('wishtree.html')






if __name__ == "__main__":
    app.run(debug=True)