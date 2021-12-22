from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth =  Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Autenticado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='error')
        else:
            flash('O email não existe.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('O email ja foi cadastrado.', category='error')

        if len(email) < 4 :
            flash('O email precisa ser maior que 3 caracteres.', category='error')
        elif len(username) < 2:
            flash('O nome de usuário precisa ser maior que 1 caractere.', category='error')
        elif password1 != password2:
            flash('As senhas não coincidem. ', category='error')
        elif len(password1) < 4:
            flash('A senha precisa ter pelo menos 4 caracteres.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return  render_template('sign_up.html', user=current_user)

@login_required
@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))