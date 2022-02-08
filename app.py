from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, flash, session, url_for, redirect, abort
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "hs6dkjh1a3fou2hebfhb"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Users {self.id}>"

# class Data(db.Model): С этим что-то не так
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
#
#     def __repr__(self):
#         return f"<data {self.id}>"


@app.route("/main", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        if len(request.form["email"]) > 2:
            flash("Отправлено")
        else:
            flash("Ошибка")
    return render_template("contact.html", title="Введите пароль")


@app.route("/profile/<username>")
def profile(email):
    if 'userLogged' not in session or session['userLogged'] != email:
        abort(401)
    return f"Пользователь"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', email=session['userLogged']))
    elif request.form['psw'] == "123":
        session['userLogged'] = request.form['email']
        return redirect(url_for('profile', email=session['userLogged']))

    return render_template('login.html', title="Добавление пользователя")


@app.route('/d', methods=["GET"])
def create_article():

    arr = Users(psw=12345)
    try:
        db.session.add(arr)
        db.session.commit()
    except:
        pass
    return 'добавлено'


@app.errorhandler(404)
def pageNoFound(error):
    return render_template("page404.html", title="Страница не найдена"), 404


if __name__ == "__main__":
    app.run(debug=True)