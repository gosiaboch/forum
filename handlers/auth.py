import os

import smartninja_redis

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))

from flask import render_template, request, url_for, make_response, Blueprint
from werkzeug.utils import redirect
from models.baza import db
from models.user import User
import hashlib
from utils.redis_helper import *

# app = Flask(__name__)
auth_handlers = Blueprint("auth", __name__)
db.create_all()

@auth_handlers.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repeat = request.form.get("repeat")
        email_address = request.form.get("email-address")

        if password != repeat:
            return "Hasła nie pasuja do siebie!"

        # print(username)
        # print(password)
        # print(repeat)

        user = User(username=username, password_hash=hashlib.sha256(password.encode()).hexdigest(), session_token = str(uuid.uuid4()), email_address=email_address)

        # print(user.session_token)
        # print(hashlib.sha256(password.encode()).hexdigest())

        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('topic.index')))
        response.set_cookie("session_token", user.session_token, httponly=True, samesite='Strict')

        return response

@auth_handlers.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.query(User).filter_by(username=username).first()

        if not user:
            return "Bledne haslo lub nazwa uzytkownika"
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user.password_hash:
                user.session_token = str(uuid.uuid4())
                db.add(user)
                db.commit()

                response = make_response(redirect(url_for('topic.index')))
                response.set_cookie("session_token", user.session_token, httponly=True, samesite='Strict')

                return response

            else:
                return "Bledne haslo lub nazwa uzytkownika"



if __name__ == '__main__':
    auth_handlers.run()