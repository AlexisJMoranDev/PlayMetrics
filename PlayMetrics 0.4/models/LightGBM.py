import pandas as pd
import numpy as np
import os
import joblib
import re

dir_path = os.path.dirname(__file__)

model_success = joblib.load(os.path.join(dir_path, 'model_success.pkl'))
model_owners = joblib.load(os.path.join(dir_path, 'model_owners.pkl'))
mlb = joblib.load(os.path.join(dir_path, 'mlb_tags.pkl'))

expected_columns = model_success.feature_name_

LOG_PRICE_MAX  = np.log10(1000 + 1)
LOG_LANGS_MAX  = np.log10(103  + 1)

def limpiar_nombre_feature(nombre):
    nombre = str(nombre).lower()
    nombre = nombre.replace(" ", "_")
    nombre = re.sub(r'[^a-z0-9_]', '', nombre)
    return nombre

def success_a_probabilidad(score):
    score_min, score_max = 1, 8
    prob = ((score - score_min) / (score_max - score_min)) * 100
    return round(float(np.clip(prob, 0, 100)), 1)

def nivel_exito(prob):
    if prob >= 75: return "Probabilidad alta"
    if prob >= 50: return "Probabilidad media"
    return "Probabilidad baja"

def predecir_exito(precio, lenguajes, edad_minima, plataformas, mes_lanzamiento, tags):
    plats = [p.lower() for p in plataformas]

    fila_numerica = {
        'price_norm':     (np.log10(max(0, precio)    + 1) / LOG_PRICE_MAX) * 10,
        'languages_norm': (np.log10(max(0, lenguajes) + 1) / LOG_LANGS_MAX) * 10,
        'required_age':   edad_minima,
        'release_month':  mes_lanzamiento,
        'windows':        1 if 'windows' in plats else 0,
        'mac':            1 if 'mac'     in plats else 0,
        'linux':          1 if 'linux'   in plats else 0,
    }
    
    tags_limpios = [t.lower().strip() for t in tags]
    tags_encoded_u = mlb.transform([tags_limpios])
    tag_cols_u = [f"tag_{limpiar_nombre_feature(t)}" for t in mlb.classes_]
    tags_df_u = pd.DataFrame(tags_encoded_u.toarray(), columns=tag_cols_u)

    X_input = pd.concat([pd.DataFrame([fila_numerica]), tags_df_u], axis=1)
    X_input.columns = [limpiar_nombre_feature(c) for c in X_input.columns]
    
    X_input = X_input.reindex(columns=expected_columns, fill_value=0)

    score_pred = float(model_success.predict(X_input)[0])
    owners_log = float(model_owners.predict(X_input)[0])
    
    usuarios = max(0, int((10 ** owners_log) - 1))
    prob = success_a_probabilidad(score_pred)
    nivel = nivel_exito(prob)

    # ----------- DICCIONARIO PARA LA API -----------
    return {
        'probabilidad_exito': prob,
        'nivel':              nivel,
        'usuarios_estimados': usuarios,
        'success_score_raw':  score_pred,
        'owners_log_raw':     owners_log,
    }