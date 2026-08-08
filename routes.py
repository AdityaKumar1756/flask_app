from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Article

main = Blueprint("main", __name__)

@main.route("/")
def index():
    articles = Article.query.filter_by(is_published=True).order_by(
        Article.published_at.desc()
    ).all()
    return render_template("index.html", articles=articles)

@main.route("/articles/<slug>")
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template("article.html", article=article)

@main.route("/articles/new", methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        slug = title.lower().replace(" ", "-")
        body = request.form["body"]
        
        article = Article(
            title=title, slug=slug, body=body,
            author_id=current_user.id, is_published=True
        )
        db.session.add(article)
        db.session.commit()
        flash("Article published!", "success")
        return redirect(url_for("main.article_detail", slug=article.slug))
    
    return render_template("create_article.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Invalid credentials", "error")
    return render_template("login.html")