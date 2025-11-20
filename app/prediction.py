# prediction.py
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# Caminhos dos arquivos (ajuste se necessário dependendo da sua estrutura de pastas)
PATH_ML = "../ML/"  # Ou onde quer que você tenha salvo os .pkl e .h5


def carregar_artefatos():
    """Carrega os modelos treinados apenas uma vez para não pesar na memória."""
    try:
        # Modelo Clássico (Burnout)
        rf_model = joblib.load(f"{PATH_ML}modelo_sobrecarga.pkl")
        scaler_sobrecarga = joblib.load(f"{PATH_ML}scaler_sobrecarga.pkl")

        # Rede Neural (Humor)
        nn_model = load_model(f"{PATH_ML}modelo_humor_nn.h5")
        scaler_humor = joblib.load(f"{PATH_ML}scaler_humor.pkl")
        le_humor = joblib.load(f"{PATH_ML}label_encoder_humor.pkl")

        return rf_model, scaler_sobrecarga, nn_model, scaler_humor, le_humor
    except Exception as e:
        print(f"⚠️ Erro ao carregar modelos de IA: {e}")
        return None, None, None, None, None


def analisar_risco_tempo_real(dados_dict):
    """
    Recebe o dicionário de dados recém-coletado em monitor.py
    Retorna mensagens de insight geradas pela IA.
    """
    rf, sc_rf, nn, sc_nn, le_nn = carregar_artefatos()

    if not rf:
        return "⚠️ IA Indisponível (Modelos não encontrados)"

    # 1. Preparar dados para o Modelo de Sobrecarga (Random Forest)
    # Ordem das features deve ser EXATAMENTE a mesma do treinamento:
    # [VELOCIDADE_DIGITACAO, TEMPO_PAUSA, TEMPO_TELA_LIGADA, TEMPO_INTERACAO, TEMPO_MOUSE, ENERGIA]

    features_rf = np.array([[
        dados_dict['velocidade_digitacao'],
        dados_dict['tempo_pausa'],
        dados_dict['tempo_tela_ligada'],
        dados_dict['tempo_interacao'],
        dados_dict['tempo_mouse'],
        dados_dict['energia']
    ]])

    features_rf_scaled = sc_rf.transform(features_rf)
    risco_burnout = rf.predict(features_rf_scaled)[0]
    prob_burnout = rf.predict_proba(features_rf_scaled)[
        0][1]  # Probabilidade da classe 1

    # 2. Preparar dados para a Rede Neural (Humor)
    # Features: [VELOCIDADE, PAUSA, TELA, INTERACAO, MOUSE, ENERGIA, ESTRESSE]
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
    classe_humor_idx = np.argmax(pred_nn)
    humor_previsto = le_nn.inverse_transform([classe_humor_idx])[0]

    # 3. Gerar Relatório de Insights
    insights = "\n🧠 === ANÁLISE DA INTELIGÊNCIA ARTIFICIAL ===\n"

    # Insight de Burnout
    if risco_burnout == 1:
        insights += f"🔴 ALERTA DE SOBRECARGA: O modelo detectou {prob_burnout*100:.1f}% de chance de Burnout.\n"
        insights += "   👉 Recomendação: Faça uma pausa longa imediatamente. Saia da tela.\n"
    else:
        insights += f"🟢 Risco de Sobrecarga Baixo ({prob_burnout*100:.1f}%). Continue mantendo o equilíbrio.\n"

    # Insight de Humor (Rede Neural)
    insights += f"🔮 A Rede Neural analisou seus padrões de uso e previu seu humor como: '{humor_previsto}'\n"

    if humor_previsto != dados_dict['humor_declarado']:
        insights += f"   (Interessante: Você disse que estava '{dados_dict['humor_declarado']}', mas seu comportamento diz outra coisa.)"

    return insights
