from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

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

player_positions = db.Table('player_positions',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('position_id', db.Integer, db.ForeignKey('position.id'), primary_key=True)
)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	number = db.Column(db.Integer, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	positions = db.relationship('Position', secondary=player_positions, backref=db.backref('players', lazy='dynamic'))
	def __repr__(self):
		return 'Player {}'.format(self.name + " #" + str(self.number))

class Position(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	position_name = db.Column(db.String(120), index=True, unique=True)
	num_players = db.Column(db.Integer)

	def update_num_players(self):
		self.num_players = Position.query.all().players.count()
		db.session.commit()

	def __repr__(self):
		return 'Position {}'.format(self.position_name)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))