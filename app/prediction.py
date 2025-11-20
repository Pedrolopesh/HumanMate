# app/prediction.py
import joblib
import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import load_model

# --- CONFIGURAÇÃO DE CAMINHOS ---
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)
PATH_ML = os.path.join(root_dir, "ML")
# --------------------------------


def carregar_artefatos():
    try:
        path_rf = os.path.join(PATH_ML, "modelo_sobrecarga.pkl")
        path_scaler_rf = os.path.join(PATH_ML, "scaler_sobrecarga.pkl")
        path_nn = os.path.join(PATH_ML, "modelo_humor_nn.h5")
        path_scaler_nn = os.path.join(PATH_ML, "scaler_humor.pkl")
        path_le = os.path.join(PATH_ML, "label_encoder_humor.pkl")

        rf_model = joblib.load(path_rf)
        scaler_sobrecarga = joblib.load(path_scaler_rf)
        # Carrega NN com custom_objects para evitar erro de compilador, se houver
        nn_model = load_model(path_nn, compile=False)
        scaler_humor = joblib.load(path_scaler_nn)
        le_humor = joblib.load(path_le)

        return rf_model, scaler_sobrecarga, nn_model, scaler_humor, le_humor
    except Exception as e:
        print(f"⚠️ Erro ao carregar modelos: {e}")
        return None, None, None, None, None


def analisar_risco_tempo_real(dados_dict):
    rf, sc_rf, nn, sc_nn, le_nn = carregar_artefatos()

    if not rf:
        return "⚠️ Erro: Modelos de IA não foram carregados corretamente."

    # --- 1. ANÁLISE DE BURNOUT (Random Forest) ---
    features_rf = np.array([[
        dados_dict['velocidade_digitacao'],
        dados_dict['tempo_pausa'],
        dados_dict['tempo_tela_ligada'],
        dados_dict['tempo_interacao'],
        dados_dict['tempo_mouse'],
        dados_dict['energia']
    ]])

    features_rf_scaled = sc_rf.transform(features_rf)

    # PROTEÇÃO CONTRA MODELO DE CLASSE ÚNICA
    # Se o modelo treinou apenas com dados "Sem Risco", ele não sabe prever probabilidade de risco.
    try:
        proba_array = rf.predict_proba(features_rf_scaled)

        if proba_array.shape[1] > 1:
            # Caso normal: tem probabilidade para 0 e 1
            prob_burnout = proba_array[0][1]
            risco_burnout = 1 if prob_burnout > 0.5 else 0
        else:
            # Caso raro: modelo só conhece uma classe
            classe_unica = rf.classes_[0]  # Pode ser 0 ou 1
            if classe_unica == 1:
                prob_burnout = 1.0
                risco_burnout = 1
            else:
                prob_burnout = 0.0
                risco_burnout = 0

    except Exception as e:
        return f"⚠️ Erro na predição de Burnout: {e}"

    # --- 2. ANÁLISE DE HUMOR (Rede Neural) ---
    try:
        features_nn = np.array([[
            dados_dict['velocidade_digitacao'],
            dados_dict['tempo_pausa'],
            dados_dict['tempo_tela_ligada'],
            dados_dict['tempo_interacao'],
            dados_dict['tempo_mouse'],
            dados_dict['energia'],
            dados_dict['estresse']
        ]])

        features_nn_scaled = sc_nn.transform(features_nn)
        pred_nn = nn.predict(features_nn_scaled, verbose=0)

        # Pega o índice da maior probabilidade
        classe_humor_idx = np.argmax(pred_nn)

        # Garante que o índice existe no LabelEncoder
        if classe_humor_idx < len(le_nn.classes_):
            humor_previsto = le_nn.inverse_transform([classe_humor_idx])[0]
        else:
            humor_previsto = "Indefinido"

    except Exception as e:
        humor_previsto = "Erro na análise"

    # --- 3. RELATÓRIO FINAL ---
    insights = "\n🧠 === ANÁLISE DA INTELIGÊNCIA ARTIFICIAL ===\n"

    if risco_burnout == 1:
        insights += f"🔴 ALERTA DE SOBRECARGA: Risco elevado ({prob_burnout*100:.1f}%).\n"
        insights += "   👉 Recomendação: O sistema sugere uma pausa imediata.\n"
    else:
        insights += f"🟢 Risco de Sobrecarga Baixo ({prob_burnout*100:.1f}%). Ritmo saudável.\n"

    insights += f"🔮 Previsão de Humor baseada no uso: '{humor_previsto}'\n"

    declarado = dados_dict.get('humor_declarado', 'N/A')
    if humor_previsto != declarado:
        insights += f"   (Nota: Divergência detectada. Você sente '{declarado}', mas seus padrões indicam '{humor_previsto}')"

    return insights
