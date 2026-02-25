from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


# Solicitud de recoleccion de datos
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Usted se Loggeo con éxito!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrecta, Pruebe de nuevo', category='error')
        else:
            flash('El email no existe.', category='error')

    return render_template('login.html', user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = User.query.filter_by(email=email).first()

        #Mensajes para los usuarios registrados/por registrar, metodo flash
        if existing_user:
            flash('El email ya existe.', category='error')
        elif len(email) < 4:
            flash('El correo debe ser mayor a 3 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('El primer nombre debe ser mayor a 1 caracter.', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden.', category='error')
        elif len(password1) < 7:
            flash('La contraseña debe ser mayor a 7 caracteres.', category='error')
        else:
            # Añade el usuario a la BD
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Cuenta creada con éxito!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sing_up.html', user=current_user)
