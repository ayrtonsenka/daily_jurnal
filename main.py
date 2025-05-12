from flask import Flask, render_template, request, redirect, url_for
import datetime
import json
import os

EMAIL = 'cordandanilo@gmail.com'
PASSWORD = 'danilo170119'
DATA_FILE = "blogs.json"

app = Flask(__name__)

def load_blogs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_blogs(blogs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(blogs, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == EMAIL and password == PASSWORD:
            return render_template('welcome.html')
        else:
            error = "Invalid email or password"
            return render_template('home.html', error=error)
    return render_template("home.html")

@app.route('/create_new', methods=['GET', 'POST'])
def create_new():
    if request.method == "POST":   
        date = request.form.get('date')
        text = request.form.get('content')
        blogs = load_blogs()
        blogs.append({'date': date, 'text': text})
        save_blogs(blogs)
        return redirect(url_for('my_docs')) 

    date = datetime.datetime.now()           
    now = date.strftime("%Y-%m-%d")
    return render_template('new.html', now=now)

@app.route('/my_docs')
def my_docs():
    blogs = load_blogs()
    return render_template('docs.html', blogs=blogs)

@app.route('/remove_entry/<int:index>', methods=['POST'])
def remove_entry(index):
    blogs = load_blogs()
    if 0 <= index < len(blogs):
        blogs.pop(index)
        save_blogs(blogs)
    return redirect(url_for('my_docs'))

if __name__ == "__main__":
    app.run(debug=True)