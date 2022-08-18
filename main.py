from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import database_exists
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import and_, or_

# Global variables
TAINAIN_ZONES = """中西區
東區
南區
北區
安平區
安南區
永康區
歸仁區
新化區
左鎮區
玉井區
楠西區
南化區
仁德區
關廟區
龍崎區
官田區
麻豆區
佳里區
西港區
七股區
將軍區
學甲區
北門區
新營區
後壁區
白河區
東山區
六甲區
下營區
柳營區
鹽水區
善化區
大內區
山上區
新市區
安定區
"""

# Main Procedures
app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


# Connect to DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# database_url = os.environ.get("DATABASE_URL", 'sqlite:///cafe.db').replace("postgres://", "postgresql://")
database_url = os.environ.get("DATABASE_URL", 'sqlite:///cafe_with_comment.db').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# for flash message
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB classes
class Cafe(db.Model):
    __tablename__ = "cafe_table"

    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=False)
    website = db.Column(db.String(1000), nullable=False)
    rest = db.Column(db.String(250), nullable=False)
    openhours = db.Column(db.String(250), nullable=False)
    # opentime = db.Column(db.String(250), nullable=False)
    # closetime = db.Column(db.String(250), nullable=False)
    timelimit = db.Column(db.String(250), nullable=False)
    wifi = db.Column(db.String(250), nullable=False)
    table = db.Column(db.String(250), nullable=False)
    toilet = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    meal = db.Column(db.String(1000), nullable=False)
    visited = db.Column(db.String(250), nullable=False)
    recommend = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(250), nullable=False)


class StreetfoodStore(db.Model):
    __tablename__ = "streetfood_store"

    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=False)
    website = db.Column(db.String(1000), nullable=False)
    rest = db.Column(db.String(250), nullable=False)
    openhours = db.Column(db.String(250), nullable=False)
    # opentime = db.Column(db.String(250), nullable=False)
    # closetime = db.Column(db.String(250), nullable=False)
    # timelimit = db.Column(db.String(250), nullable=False)
    # wifi = db.Column(db.String(250), nullable=False)
    # table = db.Column(db.String(250), nullable=False)
    toilet = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    meal = db.Column(db.String(1000), nullable=False)
    visited = db.Column(db.String(250), nullable=False)
    recommend = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(250), nullable=False)


class IceStore(db.Model):
    __tablename__ = "ice_store"

    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=False)
    website = db.Column(db.String(1000), nullable=False)
    rest = db.Column(db.String(250), nullable=False)
    openhours = db.Column(db.String(250), nullable=False)
    # opentime = db.Column(db.String(250), nullable=False)
    # closetime = db.Column(db.String(250), nullable=False)
    # timelimit = db.Column(db.String(250), nullable=False)
    # wifi = db.Column(db.String(250), nullable=False)
    # table = db.Column(db.String(250), nullable=False)
    toilet = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    meal = db.Column(db.String(1000), nullable=False)
    visited = db.Column(db.String(250), nullable=False)
    recommend = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(250), nullable=False)

class BreakfastStore(db.Model):
    __tablename__ = "breakfast_store"

    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=False)
    website = db.Column(db.String(1000), nullable=False)
    rest = db.Column(db.String(250), nullable=False)
    openhours = db.Column(db.String(250), nullable=False)
    # opentime = db.Column(db.String(250), nullable=False)
    # closetime = db.Column(db.String(250), nullable=False)
    # timelimit = db.Column(db.String(250), nullable=False)
    # wifi = db.Column(db.String(250), nullable=False)
    # table = db.Column(db.String(250), nullable=False)
    # toilet = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    meal = db.Column(db.String(1000), nullable=False)
    visited = db.Column(db.String(250), nullable=False)
    recommend = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(250), nullable=False)

# registered user class
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))



# HTLM Form classes
class CafeForm(FlaskForm):
    cafe = StringField('店名', validators=[DataRequired()])
    location = SelectField('地區', choices=[(zone, zone) for zone in TAINAIN_ZONES.split("\n")])
    maps_url = StringField('Google Maps(URL) 地圖', validators=[URL()])
    website = StringField('店家網站、FB、IG擇一(URL)', validators=[URL()])
    rest = StringField('公休日 e. g. 三、四', validators=[DataRequired()])
    openhours = StringField('營業時間 e.g. 11:30–18:00', validators=[DataRequired()])
    timelimit = SelectField('是否限時', choices=[('v', '有限時'), (' ', '不限時或不確定')])
    wifi = SelectField('提供Wifi', choices=[('v', '有Wifi'), (' ', '沒有Wifi')])
    table = SelectField('提供工作桌', choices=[('v', '有工作桌'), (' ', '沒有工作桌')])
    toilet = SelectField('提供廁所', choices=[('v', '有廁所'), (' ', '沒有廁所')])
    seats = SelectField('座位個數', choices=[('< 8', '少於8桌'), ('>=8', '至少8桌')])
    meal = StringField('推薦餐點', validators=[DataRequired()])
    visited = SelectField('曾經造訪過', choices=[('v', '吃過'), (' ', '沒吃過')])
    recommend = SelectField('推薦程度', choices=[
            ("??️", "沒吃過"), ("❤️", "❤ 不推薦"), ("❤️❤️️", "❤❤ 普通"), ("❤️❤️❤️️", "❤❤❤ 中上"), ("❤️❤️❤️❤️", "❤❤❤❤ 不錯"), ("❤️❤️❤️❤️❤️", "❤❤❤❤❤ 推薦")])
    comment = StringField('心得', validators=[DataRequired()])
    # cafe = StringField('Cafe name', validators=[DataRequired()])
    # location = StringField('Cafe Location', validators=[DataRequired()])
    # maps_url = StringField('Cafe Location on Google Maps(URL)', validators=[URL()])
    # website = StringField('Cafe Website(URL)', validators=[URL()])
    # rest = StringField('Rest Day e.g. Sat & Sun', validators=[DataRequired()])
    # opentime = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    # closetime = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    # timelimit = StringField('Time Limit e.g. 2 hours', validators=[DataRequired()])
    # wifi = StringField('WIFI Available', validators=[DataRequired()])
    # table = StringField("Table for Working", validators=[DataRequired()])
    # toilet = StringField('Toilet Available', validators=[DataRequired()])
    # seats = StringField('Seats Number', validators=[DataRequired()])
    # visited = StringField('Visited', validators=[DataRequired()])

    submit = SubmitField('Submit')

# Street Food/Ice Store Form classes
class StoreForm(FlaskForm):
    cafe = StringField('店名', validators=[DataRequired()])
    location = SelectField('地區', choices=[(zone, zone) for zone in TAINAIN_ZONES.split("\n")])
    maps_url = StringField('Google Maps(URL) 地圖', validators=[URL()])
    website = StringField('店家網站、FB、IG擇一(URL)', validators=[URL()])
    rest = StringField('公休日 e. g. 三、四', validators=[DataRequired()])
    openhours = StringField('營業時間 e.g. 11:30–18:00', validators=[DataRequired()])
    # timelimit = SelectField('是否限時', choices=[('v', '有限時'), (' ', '不限時或不確定')])
    # wifi = SelectField('提供Wifi', choices=[('v', '有Wifi'), (' ', '沒有Wifi')])
    # table = SelectField('提供工作桌', choices=[('v', '有工作桌'), (' ', '沒有工作桌')])
    toilet = SelectField('提供廁所', choices=[('v', '有廁所'), (' ', '沒有廁所')])
    seats = SelectField('座位個數', choices=[('0', '無內用'), ('< 8', '少於8桌'), ('>=8', '至少8桌')])
    meal = StringField('推薦餐點', validators=[DataRequired()])
    visited = SelectField('曾經造訪過', choices=[('v', '吃過'), (' ', '沒吃過')])
    recommend = SelectField('推薦程度', choices=[
        ("??️", "沒吃過"), ("❤️", "❤ 不推薦"), ("❤️❤️️", "❤❤ 普通"), ("❤️❤️❤️️", "❤❤❤ 中上"), ("❤️❤️❤️❤️", "❤❤❤❤ 不錯"), ("❤️❤️❤️❤️❤️", "❤❤❤❤❤ 推薦")])
    comment = StringField('心得', validators=[DataRequired()])

    submit = SubmitField('Submit')

# Breakfast Store Form classes
class BreakfastForm(FlaskForm):
    cafe = StringField('店名', validators=[DataRequired()])
    location = SelectField('地區', choices=[(zone, zone) for zone in TAINAIN_ZONES.split("\n")])
    maps_url = StringField('Google Maps(URL) 地圖', validators=[URL()])
    website = StringField('店家網站、FB、IG擇一(URL)', validators=[URL()])
    rest = StringField('公休日 e. g. 三、四', validators=[DataRequired()])
    openhours = StringField('營業時間 e.g. 11:30–18:00', validators=[DataRequired()])
    # timelimit = SelectField('是否限時', choices=[('v', '有限時'), (' ', '不限時或不確定')])
    # wifi = SelectField('提供Wifi', choices=[('v', '有Wifi'), (' ', '沒有Wifi')])
    # table = SelectField('提供工作桌', choices=[('v', '有工作桌'), (' ', '沒有工作桌')])
    # toilet = SelectField('提供廁所', choices=[('v', '有廁所'), (' ', '沒有廁所')])
    seats = SelectField('座位個數', choices=[('0', '無內用'), ('< 8', '少於8桌'), ('>=8', '至少8桌')])
    meal = StringField('推薦餐點', validators=[DataRequired()])
    visited = SelectField('曾經造訪過', choices=[('v', '吃過'), (' ', '沒吃過')])
    recommend = SelectField('推薦程度', choices=[
        ("??️", "沒吃過"), ("❤️", "❤ 不推薦"), ("❤️❤️️", "❤❤ 普通"), ("❤️❤️❤️️", "❤❤❤ 中上"), ("❤️❤️❤️❤️", "❤❤❤❤ 不錯"), ("❤️❤️❤️❤️❤️", "❤❤❤❤❤ 推薦")])
    comment = StringField('心得', validators=[DataRequired()])

    submit = SubmitField('Submit')



# User Login Form
class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("確定登入")


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# check db to see if need to create the title line
db.create_all()

# title = Cafe (
#     cafe="Cafe Name",
#     location="Location",
#     maps_url="Google Map",
#     website="Website",
#     rest="Rest Day",
#     opentime="Open",
#     closetime="Close",
#     timelimit="Time Limit",
#     wifi="WiFi",
#     table="Table",
#     toilet="Toilet",
#     seats="Seats",
#     meal="Meals",
#     visited="Visited",
# )

# title = BreakfastStore (
#     cafe="店名",
#     location="地區",
#     maps_url="地圖",
#     website="網站",
#     rest="公休日",
#     openhours="營業時間",
#     # timelimit="限時",
#     # wifi="WiFi",
#     # table="工作桌",
#     # toilet="廁所",
#     seats="座位",
#     meal="餐點",
#     visited="吃過",
#     recommend="推薦程度",
#     comment="心得",
# )
#
# db.session.add(title)
# db.session.commit()


# user = User (
#     name = "mickey",
#     password = "mm52TT18",
# )
#
# db.session.add(user)
# db.session.commit()

# variables

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

# -------- add tables -------- #

@app.route('/add/<db_name>', methods=["GET", "POST"])
def add_stores(db_name):

    # create form
    if db_name == "Cafe":
        form = CafeForm()
    elif db_name == "StreetfoodStore":
        form = StoreForm()
    elif db_name == "IceStore":
        form = StoreForm()
    elif db_name == "BreakfastStore":
        form = BreakfastForm()

    # detect submit button clicked
    if form.validate_on_submit():
        if db_name == "Cafe":
            add_cafe(form=form)
        elif db_name == "StreetfoodStore":
            add_streetfood(form=form)
        elif db_name == "IceStore":
            add_icestroe(form=form)
        elif db_name == "BreakfastStore":
            add_breakfast(form=form)
        return redirect(url_for("stores", db_name=db_name))

    return render_template('add.html', form=form, db_name=db_name)

def add_cafe(form):
    # add new cafe
    new_cafe = Cafe (
        cafe=form.cafe.data,
        location=form.location.data,
        maps_url=form.maps_url.data,
        website=form.website.data,
        rest=form.rest.data,
        openhours = form.openhours.data,
        # opentime=form.opentime.data,
        # closetime=form.closetime.data,
        timelimit=form.timelimit.data,
        wifi=form.wifi.data,
        table=form.table.data,
        toilet=form.toilet.data,
        seats=form.seats.data,
        meal=form.meal.data,
        visited=form.visited.data,
        recommend=form.recommend.data,
        comment=form.comment.data,
    )
    db.session.add(new_cafe)
    db.session.commit()



def add_streetfood(form):
    # add new cafe
    new_cafe = StreetfoodStore (
        cafe=form.cafe.data,
        location=form.location.data,
        maps_url=form.maps_url.data,
        website=form.website.data,
        rest=form.rest.data,
        openhours = form.openhours.data,
        # opentime=form.opentime.data,
        # closetime=form.closetime.data,
        # timelimit=form.timelimit.data,
        # wifi=form.wifi.data,
        # table=form.table.data,
        toilet=form.toilet.data,
        seats=form.seats.data,
        meal=form.meal.data,
        visited=form.visited.data,
        recommend=form.recommend.data,
        comment=form.comment.data,
    )
    db.session.add(new_cafe)
    db.session.commit()

def add_icestroe(form):
    # add new cafe
    new_cafe = IceStore (
        cafe=form.cafe.data,
        location=form.location.data,
        maps_url=form.maps_url.data,
        website=form.website.data,
        rest=form.rest.data,
        openhours = form.openhours.data,
        # opentime=form.opentime.data,
        # closetime=form.closetime.data,
        # timelimit=form.timelimit.data,
        # wifi=form.wifi.data,
        # table=form.table.data,
        toilet=form.toilet.data,
        seats=form.seats.data,
        meal=form.meal.data,
        visited=form.visited.data,
        recommend=form.recommend.data,
        comment=form.comment.data,
    )
    db.session.add(new_cafe)
    db.session.commit()

def add_breakfast(form):
    # add new cafe
    new_cafe = BreakfastStore (
        cafe=form.cafe.data,
        location=form.location.data,
        maps_url=form.maps_url.data,
        website=form.website.data,
        rest=form.rest.data,
        openhours = form.openhours.data,
        # opentime=form.opentime.data,
        # closetime=form.closetime.data,
        # timelimit=form.timelimit.data,
        # wifi=form.wifi.data,
        # table=form.table.data,
        # toilet=form.toilet.data,
        seats=form.seats.data,
        meal=form.meal.data,
        visited=form.visited.data,
        recommend=form.recommend.data,
        comment=form.comment.data,
    )
    db.session.add(new_cafe)
    db.session.commit()

# -------- delete tables -------- #

@app.route('/delete_query/<db_name>/<cafe_title>')
def delete_query(db_name, cafe_title):
    if db_name == "Cafe":
        cafe_to_delete = Cafe.query.filter_by(cafe=cafe_title).first()
    elif db_name == "StreetfoodStore":
        cafe_to_delete = StreetfoodStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "IceStore":
        cafe_to_delete = IceStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "BreakfastStore":
        cafe_to_delete = BreakfastStore.query.filter_by(cafe=cafe_title).first()
    return render_template('delete.html', cafe=cafe_to_delete.cafe, db_name=db_name)

@app.route('/delete/<db_name>/<cafe_title>')
def delete_cafe(cafe_title):
    # cafe_to_delete = Cafe.query.filter_by(cafe=cafe_title).first()
    if db_name == "Cafe":
        cafe_to_delete = Cafe.query.filter_by(cafe=cafe_title).first()
    elif db_name == "StreetfoodStore":
        cafe_to_delete = StreetfoodStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "IceStore":
        cafe_to_delete = IceStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "BreakfastStore":
        cafe_to_delete = BreakfastStore.query.filter_by(cafe=cafe_title).first()
    db.session.delete(cafe_to_delete)
    db.session.commit()

    return redirect(url_for("stores", db_name=db_name))

# -------- edit tables -------- #

@app.route('/edit-cafe/<db_name>/<cafe_title>', methods=["GET", "POST"])
def edit_cafe(db_name, cafe_title):
    # query a cafe
    if db_name == "Cafe":
        cafe = Cafe.query.filter_by(cafe=cafe_title).first()
    elif db_name == "StreetfoodStore":
        cafe = StreetfoodStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "IceStore":
        cafe = IceStore.query.filter_by(cafe=cafe_title).first()
    elif db_name == "BreakfastStore":
        cafe = BreakfastStore.query.filter_by(cafe=cafe_title).first()
    # create form
    if db_name == "Cafe":
        form = CafeForm()
    elif db_name == "StreetfoodStore":
        form = StoreForm()
    elif db_name == "IceStore":
        form = StoreForm()
    elif db_name == "BreakfastStore":
        form = BreakfastForm()

    # initialize form default value
    form.cafe.data = cafe.cafe
    form.location.data = cafe.location
    form.maps_url.data = cafe.maps_url
    form.website.data = cafe.website
    form.rest.data = cafe.rest
    form.openhours.data = cafe.openhours
    if db_name == "Cafe":
        form.timelimit.data = cafe.timelimit
        form.wifi.data = cafe.wifi
        form.table.data = cafe.table
    if db_name != "BreakfastStore":
        form.toilet.data = cafe.toilet
    form.seats.data = cafe.seats
    form.meal.data = cafe.meal
    form.visited.data = cafe.visited
    form.recommend.data = cafe.recommend
    form.comment.data = cafe.comment

    # detect the submit buttons clicked
    if form.validate_on_submit():
        # add new cafe
        cafe.cafe = request.form["cafe"]
        cafe.location=request.form["location"]
        cafe.maps_url=request.form["maps_url"]
        cafe.website=request.form["website"]
        # cafe.rest = form.rest.data
        cafe.rest = request.form["rest"]
        cafe.openhours = request.form["openhours"]
        if db_name == "Cafe":
            cafe.timelimit=request.form["timelimit"]
            cafe.wifi=request.form["wifi"]
            cafe.table=request.form["table"]
        if db_name != "BreakfastStore":
            cafe.toilet=request.form["toilet"]
        cafe.seats=request.form["seats"]
        cafe.meal=request.form["meal"]
        cafe.visited=request.form["visited"]
        cafe.recommend=request.form["recommend"]
        cafe.comment = request.form["comment"]
        # update db
        db.session.commit()
        return redirect(url_for("stores", db_name=db_name))
    return render_template('edit.html', form=form, db_name=db_name)

# -------- show tables -------- #

def get_tables(db_class, db_name):
    """Get tables based on the input format"""

    list_of_rows = []

    title = db_class.query.get(1)
    ordered_db_class = db_class.query.order_by(db_class.location).order_by(db_class.cafe).all()
    all_cafes = [
        cafe for cafe in ordered_db_class if cafe.id != 1
    ]

    # loop through all db and save in list_of_rows
    for cafe in [title]+all_cafes:
        items = [
            cafe.cafe,
            cafe.location,
            cafe.maps_url,
            cafe.website,
            cafe.rest,
            cafe.openhours,
        ]
        if db_name == "Cafe":
            items += [
                cafe.timelimit,
                cafe.wifi,
                cafe.table,
            ]
        if db_name != "BreakfastStore":
            items += [
                cafe.toilet,
            ]
        items += [
            cafe.seats,
            cafe.meal,
            cafe.visited,
            cafe.recommend,
            cafe.comment,
        ]
        list_of_rows.append(items)

    return list_of_rows

@app.route('/<db_name>/stores')
def stores(db_name):

    if db_name == "Cafe":
        list_of_rows = get_tables(Cafe, db_name)
    elif db_name == "StreetfoodStore":
        list_of_rows = get_tables(StreetfoodStore, db_name)
    elif db_name == "IceStore":
        list_of_rows = get_tables(IceStore, db_name)
    elif db_name == "BreakfastStore":
        list_of_rows = get_tables(BreakfastStore, db_name)

    # reusable
    return render_template('cafes.html', db_name=db_name, cafes=list_of_rows, logged_in=current_user.is_authenticated)

# # @app.route('/cafes')
# def cafes():
#     # list_of_rows = []
#     # with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
#     #     csv_data = csv.reader(csv_file, delimiter=',')
#     #     list_of_rows = []
#     #     for row in csv_data:
#     #         list_of_rows.append(row)
#     # return render_template('cafes.html', cafes=list_of_rows)
#
#     # for different db_name
#     # title = Cafe.query.get(1)
#     # all_cafes = [cafe
#     #     for cafe in Cafe.query.order_by(Cafe.location).all() if cafe.id != 1
#     # ]
#     # for cafe in [title]+all_cafes:
#     #     list_of_rows.append(
#     #         [
#     #             cafe.cafe,
#     #             cafe.location,
#     #             cafe.maps_url,
#     #             cafe.website,
#     #             cafe.rest,
#     #             cafe.openhours,
#     #             cafe.timelimit,
#     #             cafe.wifi,
#     #             cafe.table,
#     #             cafe.toilet,
#     #             cafe.seats,
#     #             cafe.meal,
#     #             cafe.visited,
#     #             cafe.recommend,
#     #             cafe.comment,
#     #         ]
#     #     )
#     list_of_rows = get_tables(Cafe, "Cafe")
#     # reusable
#     return render_template('cafes.html', db_name="Cafe", cafes=list_of_rows, logged_in=current_user.is_authenticated)

# @app.route('/streetfoodstores')
# def streetfoodstores():
#
#     list_of_rows = get_tables(StreetfoodStore, "StreetfoodStore")
#     # reusable
#     return render_template('cafes.html', db_name="StreetfoodStore", cafes=list_of_rows, logged_in=current_user.is_authenticated)
#
# @app.route('/icestores')
# def icestores():
#
#     list_of_rows = get_tables(IceStore, "IceStore")
#     # reusable
#     return render_template('cafes.html', db_name="IceStore", cafes=list_of_rows, logged_in=current_user.is_authenticated)
#
# @app.route('/breakfaststores')
# def breakfaststores():
#
#     list_of_rows = get_tables(BreakfastStore, "BreakfastStore")
#     # reusable
#     return render_template('cafes.html', db_name="BreakfastStore", cafes=list_of_rows, logged_in=current_user.is_authenticated)

# -------- User database actions -------- #

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():

        # get the login information
        name = login_form.name.data
        password = login_form.password.data

        user = db.session.query(User).filter_by(name=name).first()

        # use flash message to check if email is in database or not
        if not user:
            flash("使用者名稱不存在，請再試一次。")
        else:
            # if check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                # flask.Flask("Logged in successfully.")
                logged_in = True
                return redirect(url_for("home"))
            else:
                flash("密碼錯誤，請再試一次。")

    return render_template("login.html", form=login_form, logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
