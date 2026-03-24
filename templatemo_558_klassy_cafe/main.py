from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from post_templates import templates


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'


class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    map_url: Mapped[str] = db.Column(db.String(100), nullable=False)
    img_url: Mapped[str] = db.Column(db.String(100), nullable=False)
    location: Mapped[str] = db.Column(db.String(100), nullable=False)
    has_sockets: Mapped[int] = db.Column(db.Integer, nullable=False)
    has_toilet: Mapped[int] = db.Column(db.Integer, nullable=False)
    has_wifi: Mapped[int] = db.Column(db.Integer, nullable=False)
    can_take_calls: Mapped[int] = db.Column(db.Integer, nullable=False)
    seats: Mapped[str] = db.Column(db.String(100), nullable=False)
    coffee_price: Mapped[str] = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(Cafe))
    posts = result.scalars().all()
    print(templates)
    return render_template("index.html", cafes=posts, templates=templates)


@app.route("/add_post", methods=["POST"])
def add_post():
    if request.method == "POST":
        p_name = request.form["name"]
        p_map_url = request.form["map_url"]
        p_img_url = request.form["img_url"]
        p_location = request.form["location"]
        p_has_sockets = request.form["has_sockets"]
        p_has_wifi = request.form["has_wifi"]
        p_can_take_calls = request.form["can_take_calls"]
        p_has_seats = request.form["seats"]
        p_has_toilet = request.form["has_toilet"]
        p_coffee_price = request.form["coffee_price"]

        new_cafe = Cafe(
            name=p_name,
            map_url=p_map_url,
            img_url=p_img_url,
            location=p_location,
            has_sockets=p_has_sockets,
            has_wifi=p_has_wifi,
            can_take_calls=p_can_take_calls,
            seats=p_has_seats,
            has_toilet=p_has_toilet,
            coffee_price=p_coffee_price
        )
        db.session.add(new_cafe)
        db.session.commit()
    return redirect(url_for("get_all_posts"))



@app.route("/delete_post/<int:cafe_id>")
def delete_post(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))



if __name__ == '__main__':
    app.run(debug=True)