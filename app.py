# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

app.static_folder = 'static'

import random, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

# Wish 테이블
class Wish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(10000), nullable=False)
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

# 데이터베이스 초기화
with app.app_context():
    db.create_all()

@app.route("/")
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
    }
    return render_template('index.html', data=context)


@app.route('/wish/create/', methods=['POST'])
def wish():
    if request.method == 'POST':
        contents = request.form['contents']
        wish = Wish(contents=contents)
        db.session.add(wish)
        db.session.commit()
    return redirect('/')

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


@app.route('/wish/<int:wish_id>/comments', methods=['GET'])
def count_cheering(wish_id):
    cheering_list = Cheering.query.filter_by(wish_id=wish_id).all()
    print(cheering_list)
    print(len(cheering_list))
    return redirect('/');

if __name__ == "__main__":
    app.run(debug=True)