from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask_wtf.csrf import CsrfProtect
from flask.ext.bcrypt import Bcrypt

from forms import LoginForm, RegisterForm
import db
import config

app = Flask(__name__)
app.secret_key = config.flask_secret_key

CsrfProtect(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

snippet_types = ['sql', 'ruby', 'python', 'bash', 'js']


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.get_user(username=request.form['username'])

            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                print user
                login_user(user)

                flash('You were logged in. Go Crazy.')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('index'))
            else:
                error = 'Invalid username or password.'
        else:
            error = 'Form Invalid'
    return render_template('login.html', form=form, error=error)


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
def load_user(username):
    return db.get_user(username=username)


@app.route("/")
@login_required
def index():
    snippets = db.get_snippets()
    return render_template("index.html", snippets=snippets, snippet_types=snippet_types)


@login_required
@app.route("/snippet/", methods=["POST"])
def snippet_add():
    try:
        title = request.form["title"].strip()
        snippet_text = request.form["snippet_text"].strip()
        snippet_type = request.form["snippet_type"].strip()
        tags = request.form["tags"].strip()
        desc = request.form["desc"].strip()
        who = current_user.username  # request.form["who"].strip()

        if len(title) == 0 or len(snippet_text) == 0:
            flash("Title and Sql are required fields", "error")
            return redirect(url_for("index"))

        db.insert_snippet(title, snippet_text, snippet_type, tags, desc, who)
        flash("snippet Added!", "success")
        return redirect(url_for("index"))

    except Exception as e:
        print e
        flash("Fatal error. Contact Administrator", "error")
        return redirect(url_for("index"))


@login_required
@app.route("/snippet/<snippet_id>/", methods=["GET", "DELETE"])
def snippet_view(snippet_id):
    snippet = db.get_snippet_details(snippet_id)

    return render_template("view_snippet.html", snippet=snippet)


@login_required
@app.route("/snippet/<snippet_id>/addComment", methods=["POST"])
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


@login_required
@app.route("/snippet/<snippet_id>/edit/", methods=["GET", "POST"])
def snippet_edit(snippet_id):
    if request.method == "GET":
        snippet = db.get_snippet_details(snippet_id)
        return render_template("edit_snippet.html", snippet=snippet)
    elif request.method == "POST":
        try:
            snippet_id = request.form["id"].strip()
            title = request.form["title"].strip()
            snippet_text = request.form["snippet_text"].strip()
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
            return redirect(url_for("index"))


@login_required
@app.route("/snippet/<snippet_id>/delete/", methods=["GET", "POST"])
def query_delete(snippet_id):
    if request.method == "GET":
        snippet = db.get_query_details(snippet_id)
        return render_template("delete_snippet.html", snippet=snippet)
    elif request.method == "POST":
        db.delete_query(snippet_id)
        flash("Delete Successful", "success")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=config.flask_debug, port=config.flask_port, host="0.0.0.0")
