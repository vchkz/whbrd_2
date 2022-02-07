from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from datetime import datetime
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psw = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Users {self.id}>"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))

    def __repr__(self):
        return f"<data {self.id}>"


@app.route('/d', methods=["GET"])
def create_article():

    arr = Users(psw=12345)
    next = Data(user_id=678)
    try:
        db.session.add(arr)
        db.session.add(next)
        db.session.commit()
    except:
        pass
    return 'добавлено'


if __name__ == "__main__":
    app.run(debug=True)