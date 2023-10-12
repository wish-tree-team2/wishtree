from flask import Flask, render_template
import random

app = Flask(__name__)

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

@app.route('/')
def index():
    random_encouragement = random.choice(random_encouragements)
    return render_template('index.html', random_encouragement=random_encouragement)

if __name__ == '__main__':
    app.run()
