from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User, Player, Position

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class PositionForm(FlaskForm):
	position_name = StringField('Position Name', validators=[DataRequired()])
	submit = SubmitField('Add Position')

class PlayerForm(FlaskForm):
	name = StringField('Player Name', validators=[DataRequired()])
	number = IntegerField('Jersey Number', validators=[DataRequired()])
	submit = SubmitField('Add Player')

class PositionAdd(FlaskForm):
	player = StringField('Player Name', validators=[DataRequired()])
	position = StringField('Position', validators=[DataRequired()])
	submit = SubmitField('Add Position to Player')