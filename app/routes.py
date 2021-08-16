import os
from app import app

from app import db

from app.models import *

from flask_login import (current_user,login_required,
							login_user,logout_user)

from flask import (render_template,abort, redirect,
					 url_for, request,current_app, flash)
				
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/')
def index():
	return render_template('index.html')
	

@app.route('/home')	
@login_required
def home():
	return render_template('home.html')

@app.route('/find',methods=['POST','GET'])
@login_required
def find():
	results=None
	if request.form:
		query = request.form.get('query')
		results = User.query.filter(User.username.contains(query)).all()
		
	return render_template('find.html',results=results)

@app.route('/login',methods=['POST','GET'])	
def login():
	if request.form:
		username = request.form.get('username')
		password = request.form.get('password')
		remember = True if request.form.get('remember') else False
		user = User.query.filter_by(username=username).first()
		if user and check_password_hash(user.password, password):
			login_user(user)
			return redirect(url_for('home'))
		else:
			flash('Incorrect login details')
			
	
	return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])	
def sign_up():
	if request.form:
		username = request.form.get('username')
		name = request.form.get('name')
		password = request.form.get('password')
		user = User.query.filter_by(username=username).first()
		if user:
			flash(f'There is already a user with username: {username}')
			return redirect(url_for('login'))
		
		new_user = User(username=username,name=name, password=generate_password_hash(password, method='sha256'))
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template('signup.html')


@app.route('/message/<string:username>',methods=['POST','GET'])	
def message(username):
	user = User.query.filter_by(username=username).first()
	if user == current_user or user is None:
		flash('That person doesn\'t exist or it\'s you')
		return redirect(url_for('find'))

	if request.form:
		content = request.form.get('content')
		db.session.add(Message(body=content,fromid=current_user.id,toid=user.id))
		db.session.commit()
	messages = current_user.get_msgsent()+current_user.get_msgrecvd()
	messages.sort()
	return render_template('message.html',messages=messages)


@app.route('/logout')	
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))