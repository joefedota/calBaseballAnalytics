from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#Entity diagram found at https://ondras.zarovi.cz/sql/demo/ load with keyword CalBaseballERD
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	number = db.Column(db.Integer, index=True)
	position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return 'Player {}'.format(self.name + " #" + str(self.number))

class Position(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	position_name = db.Column(db.String(120), index=True)
	players = db.relationship('Player', backref="position", lazy="dynamic")

	def __repr__(self):
		return 'Position {}'.format(self.position_name)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))