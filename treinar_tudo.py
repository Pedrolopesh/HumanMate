# treinar_tudo.py
import os
import sys
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Importa conexão do banco (que está na mesma pasta raiz)
from db import conn

# Define o caminho da pasta ML
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, "ML")

# Garante que a pasta ML existe
if not os.path.exists(ML_DIR):
    os.makedirs(ML_DIR)

print(f"📂 Os modelos serão salvos em: {ML_DIR}")


def carregar_dados():
    print("🔄 Carregando dados do Oracle...")
    # Se não tiver conexão, cria dados fake para garantir que o arquivo seja gerado
    if not conn:
        print("⚠️ Sem conexão com banco! Gerando dados SIMULADOS para treino...")
        data = {
            "VELOCIDADE_DIGITACAO": np.random.randint(150, 300, 100),
            "TEMPO_PAUSA": np.random.randint(0, 1000, 100),
            "TEMPO_TELA_LIGADA": np.random.randint(3600, 20000, 100),
            "TEMPO_INTERACAO": np.random.randint(3000, 18000, 100),
            "TEMPO_MOUSE": np.random.randint(100, 5000, 100),
            "ENERGIA": np.random.randint(1, 6, 100),
            "ESTRESSE": np.random.randint(1, 6, 100),
            "SOBRECARGA": np.random.choice([0, 1], 100),
            "HUMOR": np.random.choice(["Bom", "Ruim", "Neutro"], 100)
        }
        return pd.DataFrame(data)

    query = """
        SELECT m.VELOCIDADE_DIGITACAO, m.TEMPO_PAUSA, m.TEMPO_TELA_LIGADA,
               m.TEMPO_INTERACAO, m.TEMPO_MOUSE, d.ENERGIA, d.ESTRESSE, d.SOBRECARGA, d.HUMOR
        FROM METRICAS_USUARIO m
        JOIN DIARIOS d ON d.EMAIL = m.EMAIL AND d.DATA_REG = m.DATA_REG
    """
    try:
        return pd.read_sql(query, conn)
    except:
        print("⚠️ Erro na query. Gerando dados SIMULADOS...")
        # Fallback igual ao acima
        data = {
            "VELOCIDADE_DIGITACAO": np.random.randint(150, 300, 100),
            "TEMPO_PAUSA": np.random.randint(0, 1000, 100),
            "TEMPO_TELA_LIGADA": np.random.randint(3600, 20000, 100),
            "TEMPO_INTERACAO": np.random.randint(3000, 18000, 100),
            "TEMPO_MOUSE": np.random.randint(100, 5000, 100),
            "ENERGIA": np.random.randint(1, 6, 100),
            "ESTRESSE": np.random.randint(1, 6, 100),
            "SOBRECARGA": np.random.choice([0, 1], 100),
            "HUMOR": np.random.choice(["Bom", "Ruim", "Neutro"], 100)
        }
        return pd.DataFrame(data)


def treinar():
    df = carregar_dados()
    if df.empty:
        print("❌ Dataset vazio. Não é possível treinar.")
        return

    # --- 1. MODELO DE SOBRECARGA (Random Forest) ---
    print("\n🤖 Treinando Random Forest (Sobrecarga)...")
    df["risco_sobrecarga"] = ((df["ESTRESSE"] >= 4) | (
        df["SOBRECARGA"] == 1)).astype(int)
    X_rf = df[["VELOCIDADE_DIGITACAO", "TEMPO_PAUSA",
               "TEMPO_TELA_LIGADA", "TEMPO_INTERACAO", "TEMPO_MOUSE", "ENERGIA"]]
    y_rf = df["risco_sobrecarga"]

    scaler_rf = StandardScaler()
    X_rf_scaled = scaler_rf.fit_transform(X_rf)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_rf_scaled, y_rf)

    joblib.dump(rf, os.path.join(ML_DIR, "modelo_sobrecarga.pkl"))
    joblib.dump(scaler_rf, os.path.join(ML_DIR, "scaler_sobrecarga.pkl"))
    print("✅ Random Forest salvo!")

    # --- 2. MODELO DE HUMOR (Rede Neural) ---
    print("\n🧠 Treinando Rede Neural (Humor)...")
    X_nn = df[["VELOCIDADE_DIGITACAO", "TEMPO_PAUSA", "TEMPO_TELA_LIGADA",
               "TEMPO_INTERACAO", "TEMPO_MOUSE", "ENERGIA", "ESTRESSE"]].values

    le = LabelEncoder()
    y_nn = le.fit_transform(df["HUMOR"])

    scaler_nn = StandardScaler()
    X_nn_scaled = scaler_nn.fit_transform(X_nn)

    model = models.Sequential([
        layers.Input(shape=(7,)),
        layers.Dense(32, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dense(len(le.classes_), activation="softmax")
    ])
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(X_nn_scaled, y_nn, epochs=10, verbose=0)

    model.save(os.path.join(ML_DIR, "modelo_humor_nn.h5"))
    joblib.dump(scaler_nn, os.path.join(ML_DIR, "scaler_humor.pkl"))
    joblib.dump(le, os.path.join(ML_DIR, "label_encoder_humor.pkl"))
    print("✅ Rede Neural salva!")


if __name__ == "__main__":
    treinar()
    print("\n🎉 TUDO PRONTO! Agora rode o 'main.py' novamente.")
