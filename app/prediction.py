# app/prediction.py
import joblib
import numpy as np
import pandas as pd
import os
import warnings
from tensorflow.keras.models import load_model

# --- CONFIGURAÇÃO DE CAMINHOS ---
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
PATH_ML = os.path.join(root_dir, "ML")
# --------------------------------


def padronizar_feature_dict(d):
    return {k.upper(): v for k, v in d.items()}


def carregar_artefatos():
    try:
        rf_model = joblib.load(os.path.join(PATH_ML, "modelo_sobrecarga.pkl"))
        scaler_sobrecarga = joblib.load(os.path.join(PATH_ML, "scaler_sobrecarga.pkl"))
        nn_model = load_model(os.path.join(PATH_ML, "modelo_humor_nn.h5"), compile=False)
        scaler_humor = joblib.load(os.path.join(PATH_ML, "scaler_humor.pkl"))
        le_humor = joblib.load(os.path.join(PATH_ML, "label_encoder_humor.pkl"))
        return rf_model, scaler_sobrecarga, nn_model, scaler_humor, le_humor
    except:
        return None, None, None, None, None



def scaler_aceita_dataframe(scaler):
    """
    Detecta automaticamente se o scaler foi treinado com DataFrame ou NumPy.
    """
    try:
        return hasattr(scaler, "feature_names_in_")
    except:
        return False



def analisar_risco_tempo_real(dados_dict):

    rf, sc_rf, nn, sc_nn, le_nn = carregar_artefatos()
    if not rf:
        return "⚠️ IA indisponível no momento (Verifique os arquivos .pkl)."

    dados_upper = padronizar_feature_dict(dados_dict)

    FEATURES_RF = [
        "VELOCIDADE_DIGITACAO", "TEMPO_PAUSA", "TEMPO_TELA_LIGADA",
        "TEMPO_INTERACAO", "TEMPO_MOUSE", "ENERGIA"
    ]

    # ============================================================
    # RANDOM FOREST — transformação sem warnings
    # ============================================================
    x_rf = [[dados_upper[f] for f in FEATURES_RF]]

    if scaler_aceita_dataframe(sc_rf):
        df_rf = pd.DataFrame([dados_upper], columns=FEATURES_RF)
        x_rf_scaled = sc_rf.transform(df_rf)
    else:
        x_rf_scaled = sc_rf.transform(x_rf)

    proba = rf.predict_proba(x_rf_scaled)
    if proba.shape[1] > 1:
        prob_burnout = proba[0][1]
        risco_burnout = 1 if prob_burnout > 0.5 else 0
    else:
        risco_burnout = rf.classes_[0]
        prob_burnout = float(risco_burnout)


    # ============================================================
    # REDE NEURAL — transformação sem warnings
    # ============================================================
    FEATURES_NN = FEATURES_RF + ["ESTRESSE"]

    x_nn = [[dados_upper[f] for f in FEATURES_NN]]

    if scaler_aceita_dataframe(sc_nn):
        df_nn = pd.DataFrame([dados_upper], columns=FEATURES_NN)
        x_nn_scaled = sc_nn.transform(df_nn)
    else:
        x_nn_scaled = sc_nn.transform(x_nn)

    # Suprimir aviso do softmax 1x1
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pred = nn.predict(x_nn_scaled, verbose=0)

    if pred.shape[1] == 1:
        idx = 1 if pred[0][0] >= 0.5 else 0
    else:
        idx = int(np.argmax(pred[0]))

    try:
        humor_previsto = le_nn.inverse_transform([idx])[0]
    except:
        humor_previsto = "Indefinido"


    # ==========================================================
    # RELATÓRIO FINAL
    # ==========================================================
    out = "\n🧠 === ANÁLISE DA INTELIGÊNCIA ARTIFICIAL ===\n"

    if risco_burnout == 1:
        out += f"🔴 RISCO ELEVADO de sobrecarga ({prob_burnout*100:.1f}%).\n"
    else:
        out += f"🟢 Risco de sobrecarga baixo ({prob_burnout*100:.1f}%).\n"

    out += f"🔮 Previsão de humor: {humor_previsto}\n"

    return out
