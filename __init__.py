from flask import Flask
import app.config
from flask import render_template
from app.weather import weather_by_city
from app.news import get_data_news
from app.model import db

from app.forms import LoginForm
from flask import current_app

from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.model import db, User, News

from flask import redirect, url_for, flash



def create_app(): 
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # when user open page, login manager get from cookies user_id and put user_id func load_user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)



    @app.route('/')
    def index():
        title = "Flask"
        content_title = "Flask Blog"
        weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
        return render_template ("index.html", title=title, content_title=content_title, weather=weather)

    @app.route('/news')
    def news():
        title = "Новости"
        content_title = "Новости Python"
        news_list = get_data_news()      
        return render_template ("news.html", title=title, 
                                newslist=news_list, content_title=content_title
                                )
    
    @app.route("/login")
    def login():
        if current_user.is_authenticated: 
            return redirect(url_for("index"))
        title = "Авторизация"
        form = LoginForm()
        return render_template("login.html", form=form, title=title)

    @app.route("/process-login", methods=["POST"])
    def process_login():
        form = LoginForm() 
        if form.validate_on_submit(): # check form
            user = User.query.filter_by(username=form.username.data).first() 
            if user and user.check_password(form.password.data): # check password 
                login_user(user)
                flash("Вы вошли на сайт") 
                return redirect(url_for("index")) 

        flash("Неправильное имя пользователя или пароль")
        return redirect(url_for("login")) 


    @app.route("/logout")
    def logout():
        logout_user()
        flash("Вы успешно разлогинились!")
        return redirect(url_for("index"))

    @app.route("/admin/")
    @login_required # check login to access this page
    def admin():
        if current_user.is_admin:  # check admin  in session/ decorator model User
            return "Привет админ"
        else:
            return "Ты кто?" 
    
        



    return app


