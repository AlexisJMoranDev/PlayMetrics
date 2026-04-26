from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import pandas as pd
import ast
import os
from models.KNN import recomendar_juegos
from models.LightGBM import predecir_exito

views = Blueprint('views', __name__)

ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'tags.csv')

try:
    df_tags = pd.read_csv(ruta_csv)

    def obtener_valores_unicos(columna):
        elementos_unicos = set()
        for fila in df_tags[columna].dropna():
            try:
                lista_elementos = ast.literal_eval(fila)
                for elemento in lista_elementos:
                    elementos_unicos.add(elemento)
            except (ValueError, SyntaxError):
                continue
        return sorted(list(elementos_unicos))

    LISTA_CATEGORIAS = obtener_valores_unicos('categories')
    LISTA_GENEROS = obtener_valores_unicos('genres')
    LISTA_TAGS = obtener_valores_unicos('tags')

except Exception as e:
    LISTA_CATEGORIAS, LISTA_GENEROS, LISTA_TAGS = [], [], []

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/predict')
@login_required
def predict():
    return render_template(
        "predict.html", 
        user=current_user,
        lista_categorias=LISTA_CATEGORIAS,
        lista_generos=LISTA_GENEROS,
        lista_tags=LISTA_TAGS
    )

@views.route('/user')
@login_required
def user_profile():
    return render_template("user.html", user=current_user)


@views.route('/api/hacer_prediccion', methods=['POST'])
@login_required
def hacer_prediccion():
    datos_usuario = request.get_json()

    precio = datos_usuario.get('price', 0.0)
    lenguajes = datos_usuario.get('num_languages', 1)
    edad_minima = datos_usuario.get('min_age', 0)
    plataformas = datos_usuario.get('platforms', [])
    mes = datos_usuario.get('release_month', 1)
    tags_combinados = datos_usuario.get('combined_tags', [])

    # ------------------ MODELO KNN ------------------
    juegos_similares = recomendar_juegos(
        precio=precio,
        lenguajes=lenguajes,
        edad_minima=edad_minima,
        plataformas=plataformas,
        mes_lanzamiento=mes,
        tags=tags_combinados,
        k=5
    )

    # ------------------ MODELO LightGBM ------------------
    resultados_lgbm = predecir_exito(
        precio=precio,
        lenguajes=lenguajes,
        edad_minima=edad_minima,
        plataformas=plataformas,
        mes_lanzamiento=mes,
        tags=tags_combinados
    )

    # ------------------ INFORMACION PARA EL FRONT ------------------
    return jsonify({
        "status": "success",
        "lgbm": resultados_lgbm,     
        "knn": juegos_similares      
    })