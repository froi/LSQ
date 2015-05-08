from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask_wtf.csrf import CsrfProtect
from flask.ext.bcrypt import Bcrypt

from forms import LoginForm, RegisterForm, SnippetForm
import db
import config

app = Flask(__name__)
app.secret_key = config.flask_secret_key

CsrfProtect(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.get_user(username=request.form['username'])

            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):

                login_user(user)

                flash('You were logged in. Go Crazy.', 'success')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('home'))
            else:
                flash('Invalid username or password.', 'error')
        else:
            flash('Form Invalid', 'error')
    return render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = None
    if form.validate_on_submit():
        user = db.add_user(
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data),
            email=form.email.data
        )
        login_user(user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id=user_id)


@app.route("/")
def index():
    return redirect(url_for('home'))


@app.route("/home", methods=["GET"])
@login_required
def home():
    form = SnippetForm(request.form)
    snippets = db.get_snippets()
    return render_template("home.html", snippets=snippets, form=form)


@login_required
@app.route("/snippet/", methods=["POST"])
def snippet_add():
    try:
        title = request.form["title"].strip()
        snippet_text = request.form["code"].strip()
        snippet_type = request.form["snippet_type"].strip()
        tags = request.form["tags"].strip()
        desc = request.form["desc"].strip()
        who = current_user.username  # request.form["who"].strip()

        if len(title) == 0 or len(snippet_text) == 0:
            flash("Title and Sql are required fields", "error")
            return redirect(url_for("home"))

        db.insert_snippet(title, snippet_text, snippet_type, tags, desc, who)
        flash("snippet Added!", "success")
        return redirect(url_for("home"))

    except Exception as e:
        print e
        flash("Fatal error. Contact Administrator", "error")
        return redirect(url_for("home"))


@app.route("/snippet/<snippet_id>/", methods=["GET", "DELETE"])
@login_required
def snippet_view(snippet_id):
    snippet = db.get_snippet_details(snippet_id)

    return render_template("view_snippet.html", snippet=snippet)


@app.route("/snippet/<snippet_id>/addComment", methods=["POST"])
@login_required
def add_comment(snippet_id):
    snippet = db.get_snippet_details(snippet_id)
    try:
        comment_text = request.form["comment"].strip()

        comment = db.insert_comment(comment_text, current_user.username)

        snippet.comments.append(comment)

        snippet.save()

        flash("Comment added.", "success")
    except Exception as e:
        print e
        flash("Error adding comment to snippet.", "error")

    return redirect(url_for("snippet_view", snippet_id=snippet_id))


@app.route("/snippet/<snippet_id>/edit/", methods=["GET", "POST"])
@login_required
def snippet_edit(snippet_id):
    form = SnippetForm(request.form)
    if request.method == "GET":
        snippet = db.get_snippet_details(snippet_id)
        return render_template("edit_snippet.html", snippet=snippet, form=form)
    elif request.method == "POST":
        try:
            snippet_id = request.form["id"].strip()
            title = request.form["title"].strip()
            snippet_text = request.form["code"].strip()
            snippet_type = request.form["snippet_type"].strip()
            tags = request.form["tags"].strip()
            desc = request.form["desc"].strip()
            who = current_user.username  # request.form["who"].strip()

            if len(title) == 0 or len(snippet_text) == 0:
                flash("Title and Sql are required fields", "error")
                return redirect(url_for("snippet_edit", snippet_id=snippet_id))

            db.update_snippet(snippet_id, title, snippet_text, snippet_type, tags, desc, who)
            flash("Snippet Modified!", "success")
            return redirect(url_for("snippet_view", snippet_id=snippet_id))

        except Exception as e:
            print e
            flash("Fatal error. Contact Administrator", "error")
            return redirect(url_for("home"))


@app.route("/snippet/<snippet_id>/delete/", methods=["GET", "POST"])
@login_required
def snippet_delete(snippet_id):
    if request.method == "GET":
        snippet = db.get_snippet_details(snippet_id)
        return render_template("delete_snippet.html", snippet=snippet)
    elif request.method == "POST":
        db.delete_snippet(snippet_id)
        flash("Delete Successful", "success")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=config.flask_debug, port=config.flask_port, host="0.0.0.0")
