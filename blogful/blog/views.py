# Future proof integer division for python 2.  Needs to be called on top.
from __future__ import division 

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash



from blog import app
from .database import session, Entry, User



### Check URL arguments for 'page' and 'limit'.  If not set, uses defaults.
#
#
def check_url_args(ref_url):
    PAGINATE_BY = 10
    DEFAULT_PAGE = 1
    RANGE_LIMIT = 25

    #
    # Request would not work without setting a request context in this 
    # function's local scope
    #
    # app.test_request_context/push will set context to the referring url.
    ###
    ctx = app.test_request_context(ref_url)
    ctx.push

    if request.args.get('page'):
        if request.args.get('page').isdigit():
            page = int(request.args.get('page'))
            if page < 1:
                page = DEFAULT_PAGE
    else:
        page = 1

    try:
        limit = int(request.args.get('limit'))
        if limit in range(1,RANGE_LIMIT):
            limit = limit
        else:
            limit = PAGINATE_BY
    except:
        limit = PAGINATE_BY
    return page, limit



@app.route("/")
@app.route("/page/")
def entries():

    page, limit = check_url_args(request.url)

    count = session.query(Entry).count()
    # PYTHON 3 INT DIVISION 
    total_pages = (count - 1) // limit + 1
    if page > total_pages:
        page = total_pages

    # Zero-indexed page
    page_index = page - 1

    start = page_index * limit
    end = start + limit

    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    print(total_pages)

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next = has_next,
        has_prev = has_prev,
        total_pages = total_pages,
        page = page,
        limit=limit)

### View, add, edit, and delete entries
#
#
@app.route("/entry/<int:id>")
def view_entry(id, page=1, limit=10):
    # For the love of god, fix the formatting on this template!

    page, limit = check_url_args(request.url)

    entry = session.query(Entry).get(id)
    author_name = session.query(User.name).\
        filter(User.id == entry.author_id).first()[0]

    return render_template("view_entry.html",
        entry = entry,
        id = id,
        page = page,
        limit = limit,
        author_name = author_name,
        author_id = entry.author_id)


@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")


@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post(page=1, limit=10):

    page, limit = check_url_args(request.url)

    if request.form["submit"] == "True":
        entry = Entry(
            title=request.form["title"],
            content=request.form["content"],
            author_id=current_user.get_id())
        page = 1
        session.add(entry)
        session.commit()
        flash("Entry succesfully added!", "success")
        return redirect(url_for("view_entry",
            page=page,
            limit=limit,
            id=entry.id))


@app.route("/entry/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id, page = 1, limit =10):

    page, limit = check_url_args(request.url)

    entry = session.query(Entry).get(id)

    if entry.author_id == int(current_user.get_id()):
        return render_template("edit_entry.html",
            id=id,
            entry_title=entry.title,
            entry_content=entry.content)
    else:
        flash("Current user not the author of this entry.", "danger")
        return redirect(url_for("view_entry",
            id=id,
            page=page,
            limit=limit))


@app.route("/entry/<int:id>/edit", methods=["POST"])
@login_required
def edit_entry_post(id, page = 1, limit = 10):

    page, limit = check_url_args(request.url)

    entry = session.query(Entry).get(id)
    if entry.author_id == int(current_user.get_id()):
        edit_entry = request.form["edit"]
        if edit_entry == "True":
            entry.title = request.form["title"]
            entry.content = request.form["content"]
            session.commit()
            flash("Entry successfully edited.", "success")
            return redirect(url_for("view_entry", id=id, page=page, limit=limit))
        else:
            return redirect(url_for("view_entry", id=id, page=page, limit=limit))
    else:
        flash("Current user not the author of this entry.", "danger")
        return redirect(url_for("view_entry",
            id=id,
            page=page,
            limit=limit))


@app.route("/entry/<int:id>/delete", methods=["GET"])
@login_required
def delete_entry_get(id, page = 1, limit = 10):

    page, limit = check_url_args(request.url)

    entry = session.query(Entry).get(id)

    if entry.author_id == int(current_user.get_id()):
        return render_template("delete_entry.html",
            entry = entry,
            id = id)
    else:
        flash("Current user not the author of this entry.", "danger")
        return redirect(url_for("view_entry",
            id=id,
            page=page,
            limit=limit))


@app.route("/entry/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry_post(id, page =1, limit = 10):

    page, limit = check_url_args(request.url)

    entry = session.query(Entry).get(id)
    if entry.author_id == int(current_user.get_id()):
        delete_entry=request.form["delete"]
        if delete_entry == "True":
            session.delete(entry)
            session.commit()
            flash("Entry deleted.", "warning")
            return redirect(url_for("entries", page=page, limit=limit))
        else:
            return redirect(url_for("view_entry",
                id=id,
                page=page,
                limit=limit))
    else:
        flash("Current user not the author of this entry.", "danger")
        return redirect(url_for("view_entry",
            id=id,
            page=page,
            limit=limit))


### Login / Logout / Registration
#
#
@app.route("/login", methods=["GET"])
def login_get():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect user or password.", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    flash("User {} has successfully logged in.".format(
        user.name), "success")
    return redirect(request.args.get('next') or url_for("entries"))


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("entries"))


@app.route("/registration", methods=["GET"])
def registration_get():
    if current_user.is_authenticated:
        username=current_user.name
        flash(
            "User \'{}\' is already logged in. Please logout to register.".format(username),
            "danger")
        return redirect(url_for("entries"))
    else:
        return render_template("registration.html")

@app.route("/registration", methods=["POST"])
def registration_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]
    user = session.query(User).filter_by(email=email).first()
    if request.form["submit"] == "True":
        if not user:
            if password == password2:
                passwordhash = generate_password_hash(password, 
                                    method="pbkdf2:sha256",
                                    salt_length=10000)
                if len(password) >= 8:
                    newuser = User(
                        name=name,
                        email=email,
                        password=passwordhash)
                    session.add(newuser)
                    session.commit()
                    login_user(newuser)
                    flash("User {} added and logged in.".format(name), "success")
                    return redirect(url_for("entries"))
                else:
                    flash("Password needs to be at least 8 characters.", "danger")
                    return redirect(url_for("registration_get"))
            else:
                flash("Passwords don't match.".format(
                    password, password2), "danger")
                return redirect(url_for("registration_get"))
        else:
            flash("User already exists.", "danger")
            return redirect(url_for("registration_get"))
    else:
        return redirect(url_for("entries"))

