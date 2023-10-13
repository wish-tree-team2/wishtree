# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''

import random
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from datetime import datetime,timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from pytz import timezone


app = Flask(__name__)
app.secret_key = "super secret key"


# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

#유저 테이블
class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.String(80), nullable=False,unique=True)
	password = db.Column(db.String(80), nullable=False)
	username = db.Column(db.String(80), nullable=False,unique=True)

	def __init__(self, user_id, password, username):
		self.user_id = user_id
		self.password = password
		self.username = username
        
    
#소원 테이블
class Wish(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'Wish for User Id {self.user_id}:{self.contents}'
    

# Cheering 테이블
class Cheering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish_id = db.Column(db.Integer, db.ForeignKey('wish.id'), nullable=False)
    comment_contents = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Seoul')))
    
    def __repr__(self):
        return f'Cheering for Wish ID {self.wish_id}: {self.comment_contents}'

with app.app_context():
    db.create_all()


#로그인 기능
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_id_receive = request.form['user_id']
        password_receive = request.form['password']
        user = User.query.filter_by(user_id = user_id_receive, password = password_receive).first()

        if user is not None:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('로그인 성공!', 'success') 
            return redirect('/')
        else:
            flash('로그인 실패. 다시 시도하세요.', 'danger')

@app.route('/wish/create/', methods=['POST'])
def wish_create():
    if request.method == 'POST':
        contents = request.form['contents']
        # Get the user ID from the session
        user_id = session.get('user_id')
        username = session.get('username')
        
        if user_id is not None:
            wish = Wish(contents=contents, user_id=user_id, username = username)
            db.session.add(wish)
            db.session.commit()
        else:
            wish = Wish(contents=contents, user_id="익명", username = "익명")
            db.session.add(wish)
            db.session.commit()

    return redirect('/')

#소원 게시글 목록 불러오기
# @app.route("/")
# def wish():
#     wish_list = Wish.query.all()
#     return render_template('index-init.html', data=wish_list)

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
def home():
    encouragementMessages = [
    "너는 할 수 있어!",
    "포기하지 마세요. 꿈을 이루세요!",
    "언제나 긍정적으로 생각하세요.",
    "오늘도 힘차게 달려봐요!",
    "어제보다 오늘 더 나은 일 하시길 바랍니다.",
    "당신은 놀라울 정도로 강하고 용감해요.",
    "힘들어도 웃어요, 모든 게 괜찮아질 거예요.",
    "지금이 최고의 순간이에요.",
    "당신은 뛰어난 성과를 이룰 수 있어요.",
    "절대 포기하지 마세요!",
    "불가능한 것은 없어요.",
    "당신은 특별한 사람이에요.",
    "성공은 힘든 노력 뒤에 숨어 있어요.",
    "오늘은 더 나은 날이 될 거예요.",
    "자신을 믿어보세요, 당신은 충분히 강해요.",
    "도전은 성장의 시작이에요.",
    "당신은 어떤 일도 이길 수 있어요.",
    "매일이 좋은 기회에요.",
    "긍정적인 생각은 긍정적인 결과를 가져올 거예요.",
    "당신의 꿈을 위해 노력하세요!",
    "모든 것은 당신의 노력에 달려있어요."
    ]
    list = Wish.query.all()
    random_message = random.choice(encouragementMessages)
    context = {
        "list": list,
        "message": random_message,
        "user_id": session.get('user_id'),
        "username": session.get('uesrname'),
    }
    if 'user_id' in session:
        return render_template('index-init.html',data=context)
    else:
        return render_template('index-init.html',data=context)
    
@app.route('/wish/list')
def wish_list():
    cheerings = Cheering.query.all()
    cheerings_count = len(cheerings)
    # def comment_count(self, wish_id):
    #     #댓글 수를 반환
    #     return db.session.query(Cheering).filter_by(wish_id=wish_id).count()
    return render_template('wishTree.html', cheerings = cheerings ,data=cheerings_count)

@app.route("/signup", methods=["POST"])
def signup():

        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']

        # 사용자 정보를 데이터베이스에 저장
        user = User(user_id=user_id,username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("회원 가입이 완료되었습니다.", "success")
        return redirect("/")

@app.route('/logout')
def logout():
    # 세션에서 user_id 제거
    session.pop('user_id', None)
    flash('로그아웃되었습니다.', 'success')
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)