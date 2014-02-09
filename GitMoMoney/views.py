from GitMoMoney import app
from flask import render_template
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm, ChangePassForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/accounts/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = False
    if request.method == 'POST' and form.validate():
        m = hashlib.md5()
        m.update(form.password.data)
        user = database.get_user(username=form.username.data, password=m.hexdigest())
        if user is not None:
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        else:
            error=True
    return render_template("accounts/login.html", form=form, error=error)

@app.route("/accounts/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))

@app.route("/accounts/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    username_error = False
    if request.method == 'POST' and form.validate():
        try:
            m = hashlib.md5()
            m.update(form.password.data)
            user = database.insert_user(form.username.data, form.email.data, m.hexdigest())
            if user is not None:
                login_user(user)
            #flash("Successfully Registered!")
            return redirect(request.args.get("next") or url_for("index"))
        except Exception:
            username_error = True
    return render_template("accounts/register.html", form=form, username_error=username_error)
