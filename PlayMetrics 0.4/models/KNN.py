import pandas as pd
import numpy as np
import pickle
import os

# ---------------- CARGAR MODELO ----------------
ruta_pkl = os.path.join(os.path.dirname(__file__), 'knn_modelo.pkl')
with open(ruta_pkl, 'rb') as f:
    knn_data = pickle.load(f)

df_pm = knn_data['dataframe']
global_tag_weights = knn_data['pesos_tags']

LOG_PRICE_MAX = np.log10(1000 + 1)
LOG_LANGS_MAX = np.log10(103 + 1)
EDAD_MAX = 21

def normalizar_entrada_log(valor, log_max):
    return (np.log10(max(0, valor) + 1) / log_max) * 10

def normalizar_entrada_lineal(valor, v_min, v_max):
    if v_max == v_min: return 5.0
    return ((valor - v_min) / (v_max - v_min)) * 10

def recomendar_juegos(precio, lenguajes, edad_minima, plataformas, mes_lanzamiento, tags, k=5):
    df = df_pm.copy()
    
    tags_usuario = {t.lower() for t in tags}
    
    def calcular_weighted_score(juego_tags):
        interseccion = tags_usuario & juego_tags
        return sum(global_tag_weights.get(t, 1.0) for t in interseccion)

    df['weighted_tag_score'] = df['_tags_set'].apply(calcular_weighted_score)
    df['tags_coincidentes'] = df['_tags_set'].apply(lambda s: len(tags_usuario & s))
    
    # ---------------- NORMALIZACIONES ----------------
    u_price_norm = normalizar_entrada_log(precio, LOG_PRICE_MAX)
    u_lang_norm  = normalizar_entrada_log(lenguajes, LOG_LANGS_MAX)
    u_age_norm   = normalizar_entrada_lineal(edad_minima, 0, EDAD_MAX)
    u_month_norm = normalizar_entrada_lineal(mes_lanzamiento, 1, 12)
    u_win, u_mac, u_lin = (1 if p in [pl.lower() for pl in plataformas] else 0 for p in ['windows', 'mac', 'linux'])

    # ---------------- CALCULOS DE DISTANCIAS ----------------
    dist_price = (df['price_norm'] - u_price_norm)**2
    dist_lang  = (df['languages_norm'] - u_lang_norm)**2
    dist_age   = (normalizar_entrada_lineal(df['required_age'], 0, EDAD_MAX) - u_age_norm)**2
    dist_month = (normalizar_entrada_lineal(df['release_month'], 1, 12) - u_month_norm)**2
    dist_plat  = ((df['windows'] - u_win)*10)**2 + ((df['mac'] - u_mac)*10)**2 + ((df['linux'] - u_lin)*10)**2
    
    df['distancia'] = np.sqrt(dist_price + dist_lang + dist_age + dist_month + dist_plat)

    # ---------------- ORDEN DE IMPORTANCIA ----------------
    resultado = df.sort_values(
        by=['weighted_tag_score', 'distancia', 'success_score'],
        ascending=[False, True, False]
    ).head(k)

    columnas_finales = ['name', 'tags_coincidentes', 'weighted_tag_score', 'windows', 'mac', 'linux', 'success_score']
    
    # ---------------- LISTA QUE SE ENVIA AL FRONTEND ----------------
    return resultado[columnas_finales].to_dict(orient='records')