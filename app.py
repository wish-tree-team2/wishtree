# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)
# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Wish(db.Model):

    wish_id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Wish: {self.contents}'

with app.app_context():
    db.create_all()

#소원 게시글 생성
@app.route("/wish/create/")
def wish_create():

    #form에서 보낸 데이터 받아오기
    contents_receive = request.args.get("contents")

    # 데이터를 DB에 저장하기
    wish = Wish(contents = contents_receive)
    db.session.add(wish)
    db.session.commit()
    return redirect(url_for('wish'))

#소원 게시글 목록 불러오기
@app.route("/wish/")
def wish():
    wish_list = Wish.query.all()
    return render_template('index-init.html', data=wish_list)

if __name__ == "__main__":
    app.run(debug=True)