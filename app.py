from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, flash, session, url_for, redirect, abort
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "hs6dkjh1a3fou2hebfhb"

db = SQLAlchemy(app)


class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.psw}"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<data {self.id}>"


@app.route("/", methods=["GET"])  # Главная
def main():
    users = Passwords.query.all()
    print(users)
    return render_template("main.html", title="Введите пароль")


@app.route("/add-password", methods=["POST", "GET"])  # страница добавления нового пароля
def add_password():
    if request.method == "POST":
        password = request.form['psw']
        arr = Passwords(psw=password)
        # надо будет сделать проверку на то что парольне пустой и на то что такого пароля ешё нет в бд
        try:
            db.session.add(arr)
            db.session.commit()
        except:
            pass
        return redirect('/')

    paswords = Passwords.query.all()
    return render_template('pas-add.html', paswords=paswords)


@app.errorhandler(404)
def pageNoFound(error):
    return 'страница не найдена'


if __name__ == "__main__":
    app.run(debug=True)
