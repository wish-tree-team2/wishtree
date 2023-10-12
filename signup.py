from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 기본 설정
app.config['SECRET_KEY'] = '0000'

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 테이블 생성
with app.app_context():
    db.create_all()
    def __init__(self, user_id, password, username):
        self.user_id = user_id
        self.password = password
        self.username = username
    

class SignupForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

@app.route("/", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # 사용자 정보를 데이터베이스에 저장
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("회원 가입이 완료되었습니다.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)
