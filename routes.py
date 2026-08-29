# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User, Article

from flask import session # used for collecting the list of nums
import time #performance

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

@main.route("/submit-number", methods=["GET" , "POST"])
def submit_number():
    
    def longestIncSubseq(lst):
        # [1, 3, 12, 10, 2, 4, 5, 6, 11]
        # base case is that there is nothing in the list itself
        # for some list s[1, ... i], when we encounter s[j],
        
        endlis = [1] * len(lst)
        endlis_i = [-1] * len(lst)
        for i in range(len(lst)):
            m = 0
            mi = -1
            for j in range(i):
                if lst[j] < lst[i] and endlis[j] > m:
                    m = endlis[j]
                    mi = j
            endlis[i] = 1 + m
            endlis_i[i] = mi 
        
        # return max(endlis)
        res = []
        
        m = 0
        mi = -1
        for i in range(len(lst)):
            if endlis[i] > m:
                m = endlis[i]
                mi = i
        
        i = mi
        while (i > -1):
            res.append(lst[i])
            i = endlis_i[i]
        
        res.reverse()   
        return res
        
    def naiveImp(lst):
        res = []
        if lst:
            res.append(lst[0])
        else:
            flash("where's the number sir")
        
        for i in range(1, len(lst)):
            if lst[i] > res[len(res) - 1]:
                res.append(lst[i])
                
        return res
    
    if request.method == "POST":
        number = request.form.get("user_number", type=int)

        if "numbers" not in session:
            session["numbers"] = []
            
        if number != None:
            flash(f"got a number!! it is {number}")
            #session["numbers"].append(number)
            
            numbers = session["numbers"]
            numbers.append(number)
            session["numbers"] = numbers
            flash(f"current list: {session['numbers']}")
            
            start = time.perf_counter()
            flash(f"current books in order (ideal list): {longestIncSubseq(session['numbers'])}")
            elapsed = time.perf_counter() - start
            flash(f"time taken: {elapsed}s")
            
            start = time.perf_counter()
            flash(f"current books in order (not ideal list): {naiveImp(session['numbers'])}")
            elapsed = time.perf_counter() - start
            flash(f"time taken: {elapsed}s")
        else:
            flash("Please enter a valid number.", "error")
            
    return render_template("submit_number.html")