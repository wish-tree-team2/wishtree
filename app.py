# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
import random
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

    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Wish: {self.contents}'
    
# Cheering 테이블
class Cheering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish_id = db.Column(db.Integer, db.ForeignKey('wish.id'), nullable=False)
    comment_contents = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Cheering for Wish ID {self.wish_id}: {self.comment_contents}'

with app.app_context():
    db.create_all()

    # 20개의 응원문구 리스트
random_encouragements = [
    "You can do it!",
    "Believe in yourself!",
    "Stay positive!",
    "Dream big!",
    "Keep going!",
    "Never give up!",
    "You are amazing!",
    "You've got this!",
    "You're doing great!",
    "Make it happen!",
    "Stay focused!",
    "Chase your dreams!",
    "Stay strong!",
    "Good things are coming!",
    "Stay motivated!",
    "Stay inspired!",
    "Shine bright!",
    "You're unstoppable!",
    "Embrace the journey!",
    "Keep smiling!"
]

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

@app.route('/wish/<int:wish_id>/comment', methods=['POST'])
def add_cheering(wish_id):
    if request.method == 'POST':
        comment_contents = request.form['comment_contents']
        wish = Wish.query.get(wish_id) 
        if wish:
            cheering = Cheering(wish_id=wish_id, comment_contents=comment_contents)
            db.session.add(cheering)
            db.session.commit()
    return redirect('/')

@app.route('/')
def index():
    random_encouragement = random.choice(random_encouragements)
    return render_template('index-init.html', random_encouragement=random_encouragement)

if __name__ == "__main__":
    app.run(debug=True)