from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
import pandas as pd
import ast
import os
import json
from datetime import datetime
from . import db
from .models import Prediccion
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
    LISTA_GENEROS    = obtener_valores_unicos('genres')
    LISTA_TAGS       = obtener_valores_unicos('tags')

except Exception as e:
    LISTA_CATEGORIAS, LISTA_GENEROS, LISTA_TAGS = [], [], []


# ── Vistas principales ────────────────────────────────────────

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


# ── API: hacer predicción ─────────────────────────────────────

@views.route('/api/hacer_prediccion', methods=['POST'])
@login_required
def hacer_prediccion():
    datos_usuario = request.get_json()

    precio         = datos_usuario.get('price', 0.0)
    lenguajes      = datos_usuario.get('num_languages', 1)
    edad_minima    = datos_usuario.get('min_age', 0)
    plataformas    = datos_usuario.get('platforms', [])
    mes            = datos_usuario.get('release_month', 1)
    tags_combinados = datos_usuario.get('combined_tags', [])

    juegos_similares = recomendar_juegos(
        precio=precio,
        lenguajes=lenguajes,
        edad_minima=edad_minima,
        plataformas=plataformas,
        mes_lanzamiento=mes,
        tags=tags_combinados,
        k=5
    )

    resultados_lgbm = predecir_exito(
        precio=precio,
        lenguajes=lenguajes,
        edad_minima=edad_minima,
        plataformas=plataformas,
        mes_lanzamiento=mes,
        tags=tags_combinados
    )

    return jsonify({
        "status": "success",
        "lgbm": resultados_lgbm,
        "knn":  juegos_similares
    })


# ── API: guardar proyecto ─────────────────────────────────────

@views.route('/api/guardar_proyecto', methods=['POST'])
@login_required
def guardar_proyecto():
    # Límite de 10 proyectos por usuario
    total = Prediccion.query.filter_by(user_id=current_user.id).count()
    if total >= 10:
        return jsonify({
            "status": "error",
            "mensaje": "Has alcanzado el límite de 10 proyectos guardados."
        }), 400

    datos = request.get_json()

    nombre       = datos.get('nombre', '').strip()
    precio       = datos.get('precio', 0.0)
    edad_minima  = datos.get('edad_minima', 0)
    mes          = datos.get('mes_lanzamiento', 1)
    tags         = datos.get('tags_combinados', [])
    probabilidad = datos.get('probabilidad', 0.0)

    if not nombre:
        return jsonify({"status": "error", "mensaje": "El nombre del proyecto es obligatorio."}), 400

    nueva = Prediccion(
        user_id               = current_user.id,
        nombre                = nombre,
        precio                = precio,
        edad_minima           = edad_minima,
        mes_de_lanzamiento    = mes,
        caracteristicas_y_genero = json.dumps(tags, ensure_ascii=False),
        probabilidad          = probabilidad,
        fecha_guardado        = datetime.utcnow()
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify({
        "status":  "success",
        "mensaje": "Proyecto guardado correctamente.",
        "id":      nueva.id
    })


# ── API: borrar proyecto ──────────────────────────────────────

@views.route('/api/borrar_proyecto/<int:proyecto_id>', methods=['DELETE'])
@login_required
def borrar_proyecto(proyecto_id):
    proyecto = Prediccion.query.filter_by(
        id=proyecto_id,
        user_id=current_user.id   # solo el dueño puede borrar
    ).first()

    if not proyecto:
        return jsonify({"status": "error", "mensaje": "Proyecto no encontrado."}), 404

    db.session.delete(proyecto)
    db.session.commit()

    return jsonify({"status": "success", "mensaje": "Proyecto eliminado."})


# ── API: descargar proyecto ───────────────────────────────────

@views.route('/api/descargar_proyecto/<int:proyecto_id>')
@login_required
def descargar_proyecto(proyecto_id):
    proyecto = Prediccion.query.filter_by(
        id=proyecto_id,
        user_id=current_user.id
    ).first()

    if not proyecto:
        flash("Proyecto no encontrado.", "error")
        return redirect(url_for('auth.user_profile'))

    # Construir contenido del archivo de texto
    try:
        tags = json.loads(proyecto.caracteristicas_y_genero or '[]')
        tags_str = ', '.join(tags) if tags else 'Sin tags'
    except Exception:
        tags_str = proyecto.caracteristicas_y_genero or 'Sin tags'

    meses = {
        1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
        5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto',
        9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'
    }
    mes_str = meses.get(proyecto.mes_de_lanzamiento, str(proyecto.mes_de_lanzamiento))

    contenido = f"""
╔══════════════════════════════════════════╗
         PLAYMETRICS — REPORTE DE PROYECTO
╚══════════════════════════════════════════╝

Nombre del proyecto : {proyecto.nombre}
Fecha de guardado   : {proyecto.fecha_guardado.strftime('%d/%m/%Y %H:%M')}

── Parámetros ─────────────────────────────
Precio              : ${proyecto.precio:.2f} USD
Edad mínima         : {proyecto.edad_minima} años
Mes de lanzamiento  : {mes_str}

── Tags / Características ─────────────────
{tags_str}

── Resultado del modelo ───────────────────
Probabilidad de éxito: {proyecto.probabilidad:.1f}%

══════════════════════════════════════════
  PlayMetrics © {datetime.utcnow().year} — playmetrics.com
══════════════════════════════════════════
""".strip()

    nombre_archivo = f"PlayMetrics_{proyecto.nombre.replace(' ', '_')}.txt"

    response = make_response(contenido)
    response.headers['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response