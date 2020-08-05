from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Player, Position
from app.forms import LoginForm, RegistrationForm, PositionForm, PlayerForm, PositionAdd
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = current_user
	return render_template("index.html", title="Home", user=user)

@app.route('/positions', methods=['GET', 'POST'])
@login_required
def positions():
	form = PositionForm()
	if form.validate_on_submit():
		position = Position(position_name=form.position_name.data)
		db.session.add(position)
		db.session.commit()
		flash('Position successfully added')
	positions = Position.query.all()
	return render_template("positions.html", title="Positions", positions=positions, form=form)

@app.route('/players', methods=['GET', 'POST'])
@login_required
def players():
	form = PlayerForm()
	form2 = PositionAdd()
	if form.validate_on_submit():
		player = Player(name=form.name.data, number=form.number.data)
		db.session.add(player)
		db.session.commit()
		flash('Player successfully added')
	if form2.validate_on_submit():
		player = Player.query.filter_by(name=form2.player.data).first()
		position = Position.query.filter_by(position_name=form2.position.data).first()
		player.positions.append(position)
		db.session.commit()
		flash('Position added to player')
	players = Player.query.all()
	return render_template("players.html", title="Players", players=players, form=form, form2=form2)

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template("login.html", title="Login", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))