from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "IAMSECRET"
db = SQLAlchemy(app)


class Recivers(db.Model):
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    name = db.Column(db.String)
    items = db.Column(db.Text)
    date = db.Column(db.String)
    manager = db.Column(db.String)
    fees = db.Column(db.String)
    return_date = db.Column(db.String)
    return_to = db.Column(db.String)
    fees_status = db.Column(db.String)
    returning_date = db.Column(db.String)


class Users(db.Model):
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    role = db.Column(db.String)
    password = db.Column(db.String)


@app.before_request
def before_request():
    # new_user = Users(phone="9325837420", email="pratikdeshmukhlobhi@gmail.com", firstname="Pratik", lastname="Deshmukh", role="Super Admin", password="hello")
    # db.session.add(new_user)
    # db.session.commit()
    g.user = None
    if 'user_id' in session:
        user = Users.query.filter_by(id=session["user_id"]).first()
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    args = request.args.to_dict(flat=False)
    if "error" in args:
        error = args["error"][0]
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).all()
        print(user)
        if len(user) > 0:
            user = user[0]
            print(user)
            if user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                error = "Invalid User Password!"
        else:
            error = "You do not have accesss. Please contact To Admin!"
        return redirect(url_for('login', error=error))
    if "user_id" in session:
        return redirect(url_for("index"))
    else:
        return render_template('auth/login.html', error=error)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    else:
        data = request.form.to_dict(flat=True)
        new_reciver = Recivers(name=data["name"], items=data["items"], date=data["date"], manager=data["manager"],
                               fees=data["fees"], return_date=data["return-date"], return_to=data["return-to"], fees_status=data["fees-status"], returning_date=data["returning-date"])
        db.session.add(new_reciver)
        db.session.commit()
        return redirect(url_for('index'))


@app.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        reciver = Recivers.query.filter_by(id=id).first()
        return render_template("edit.html", reciver=reciver, user=g.user)
    else:
        data = request.form.to_dict(flat=True)
        reciver = Recivers.query.filter_by(id=id).first()
        reciver.name = data["name"]
        reciver.items = data["items"]
        reciver.date = data["date"]
        reciver.manager = data["manager"]
        reciver.fees = data["fees"]
        reciver.return_date = data["return-date"]
        reciver.return_to = data["return-to"]
        reciver.fees_status = data["fees-status"]
        reciver.returning_date = data["returning-date"]
        db.session.commit()
        return redirect(url_for("index"))


@app.errorhandler(404)
def invalid_route(e):
    return render_template("errors/404-error.html")


@app.route("/")
def index():
    if g.user:
        recivers = Recivers.query.all()
        return render_template("index.html", recivers=recivers, user=g.user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route("/users")
def users():
    if g.user:
        users = Users.query.all()
        return render_template("users/index.html", users=users, user=g.user)
    else:
        return redirect(url_for('login'))


@app.route("/user/new", methods=["GET", "POST"])
def new_user():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template("users/new.html", user=g.user)
    else:
        data = request.form.to_dict(flat=True)
        new_user = Users(firstname=data["firstname"], lastname=data["lastname"],
                         phone=data["mobile"], email=data["email"], role=data["role"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))


if __name__ == "__main__":
    app.run()
