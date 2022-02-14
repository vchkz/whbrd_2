from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect
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
    passw = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.passw}, {self.data}"


@app.route("/", methods=["GET"])  # Главная
def main():
    passwords = []
    for i in Data.query.all():
        a, b = str(i).split(', ')
        passwords.append([a, str(b)[:-16]])
    print(passwords)
    return render_template("main.html", passwords=passwords)


@app.route("/delete-password", methods=["POST"])  # Удаление
def delete_pasw():
    password = request.form['delete']
    Passwords.query.filter(Passwords.psw == password).delete()
    db.session.commit()
    return redirect('/')


@app.route("/upload", methods=["POST"])
def upload():
    data = request.json["password"]
    arr = Data(passw=data)
    db.session.add(arr)
    db.session.commit()
    if any(list(map(lambda x: x == data, Data.query.all()))):
        return "open"
    else:
        return "invalid password"


@app.route("/a", methods=["GET"])
def a():
    data = '234832'
    arr = Data(passw=data)
    db.session.add(arr)
    db.session.commit()
    return 'a'


@app.route("/add-password", methods=["POST", "GET"])  # страница добавления нового пароля
def add_password():
    if request.method == "POST":
        password = request.form['psw']
        arr = Passwords(psw=password)
        if len(password) == 0:
            pass
        if all(list(map(lambda x: str(x) != password, Passwords.query.all()))):
            try:
                db.session.add(arr)
                db.session.commit()
            except:
                pass
        else:
            pass
        return redirect('/')

    paswords = Passwords.query.all()
    return render_template('pas-add.html', paswords=paswords)


@app.errorhandler(404)
def pageNoFound(error):
    return 'страница не найдена'


if __name__ == "__main__":
    app.run(debug=True)
