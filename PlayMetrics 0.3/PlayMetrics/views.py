from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

# Enlace a la pagina del modelo de predicción
@views.route('/predict')
@login_required
def predict():
    return render_template("predict.html", user=current_user)


