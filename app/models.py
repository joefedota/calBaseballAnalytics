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

class PitcherRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
	auto_pitch_type = db.Column(db.String(64))
	pitch_call = db.Column(db.String(64))
	rel_speed = db.Column(db.Float)
	vert_rel_angle = db.Column(db.Float)
	horz_rel_angle = db.Column(db.Float)
	spin_rate = db.Column(db.Float)
	spin_axis = db.Column(db.Float)
	tilt = db.Column(db.Float)
	rel_height = db.Column(db.Float)
	rel_side = db.Column(db.Float)
	extension = db.Column(db.Float)
	vert_break = db.Column(db.Float)
	induced_vert_break = db.Column(db.Float)
	horz_break = db.Column(db.Float)
	plate_loc_size = db.Column(db.Float)
	plate_loc_height = db.Column(db.Float)
	vert_appr_angle = db.Column(db.Float)
	horz_appr_angle = db.Column(db.Float)

class BatterRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
	exit_speed = db.Column(db.Float)
	angle = db.Column(db.Float)
	direction = db.Column(db.Float)
	hit_spin_rate = db.Column(db.Float)
	distance = db.Column(db.Float)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))