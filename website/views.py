from flask import Blueprint, render_template, request, jsonify
from flask.helpers import flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from flask import session    
from .models import User, Chat
from . import db
import json
import sqlite3 as sql

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return  render_template('home.html', user=current_user)

@views.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def selfProfile(name):

    return render_template('profile.html', user=current_user)

@views.route('/chat/', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        message = request.form.get('ckeditor')
        message_user = current_user.username
        
        new_message = Chat(message=message, message_user=message_user)
        db.session.add(new_message)
        db.session.commit()
    

    con = sql.connect('website/database.db')
            
    con.row_factory = sql.Row
            
    cur = con.cursor()
    cur.execute('SELECT message, message_user  FROM chat')
            
    rowsMensagem = cur.fetchall();    
        
    return render_template('chat.html', rowsMensagem=rowsMensagem, user=current_user)

@views.route('/donate/', methods=['GET', 'POST'])
def donate():
    return render_template('donate.html', user=current_user)