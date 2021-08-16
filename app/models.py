from app import db,login_manager

from flask_login import UserMixin

from datetime import datetime

from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body=db.Column(db.String(250))
	fromid = db.Column(db.Integer, db.ForeignKey('user.id'))
	toid = db.Column(db.Integer, db.ForeignKey('user.id'))
	from_ = db.relationship('User', foreign_keys=[fromid])
	to_ = db.relationship('User', foreign_keys=[toid])
	time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

	def __lt__(self,other):
		return self.time < other.time
	def __gt__(self,other):
		return self.time > other.time
	def __ge__(self,other):
		return self.time >= other.time
	def __le__(self,other):
		return self.time <= other.time

	def  __repr__(self):
		return f'<Message, from_: {self.from_} ,to_:{self.to_} body: {self.body}>'

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(500))
	name = db.Column(db.Text(1000))
	#querying messages 
	def get_msgsent(self):
		return Message.query.filter(Message.fromid==self.id).all()

	def get_msgrecvd(self):
		return Message.query.filter(Message.toid==self.id).all()

	def send_message(self,body,to):
		msg = Message(body=body,toid=to.id,fromid=self.id)
		db.session.add(msg)
		db.session.commit()


	def  __repr__(self):
		return f'<user, username: {self.username}>'


