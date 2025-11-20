# nn_humor.py
import pandas as pd
import numpy as np
from db import conn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import joblib

"""
MÓDULO DE REDES NEURAIS (DEEP LEARNING) - HUMANMATE
---------------------------------------------------
Objetivo: Classificar o humor do usuário baseado em padrões complexos de uso.
Tecnologia: TensorFlow/Keras (Requisito obrigatório: Redes Neurais).
Arquitetura: MLP (Multilayer Perceptron) com Camadas Densas e Dropout.
"""


def carregar_dataset_humor():
    query = """
        SELECT 
            m.VELOCIDADE_DIGITACAO, m.TEMPO_PAUSA, m.TEMPO_TELA_LIGADA,
            m.TEMPO_INTERACAO, m.TEMPO_MOUSE, d.ENERGIA, d.ESTRESSE, d.HUMOR
        FROM METRICAS_USUARIO m
        JOIN DIARIOS d ON d.EMAIL = m.EMAIL AND d.DATA_REG = m.DATA_REG
    """
    return pd.read_sql(query, conn)


def treinar_rede_neural_humor():
    print("🧠 Iniciando treinamento da Rede Neural de Humor...")
    df = carregar_dataset_humor()

    if df.empty:
        print("⚠️ Dataset vazio.")
        return

    features = ["VELOCIDADE_DIGITACAO", "TEMPO_PAUSA", "TEMPO_TELA_LIGADA",
                "TEMPO_INTERACAO", "TEMPO_MOUSE", "ENERGIA", "ESTRESSE"]

    X = df[features].values

    # Codificação do Target (Humor é categórico: "Feliz", "Neutro", "Triste")
    le = LabelEncoder()
    y = le.fit_transform(df["HUMOR"])

    # Divisão e Escalonamento
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    num_classes = len(le.classes_)

    # --- ARQUITETURA DA REDE NEURAL ---
    # Input Layer: Recebe as 7 features
    # Hidden Layer 1: 32 neurônios (ReLU)
    # Dropout: Desliga 20% dos neurônios aleatoriamente para evitar overfitting
    # Hidden Layer 2: 16 neurônios (ReLU)
    # Output Layer: Softmax (Probabilidade para cada classe de humor)
    model = models.Sequential([
        layers.Input(shape=(X_train_scaled.shape[1],)),
        layers.Dense(32, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(16, activation="relu"),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    print("⚙️ Treinando épocas...")
    history = model.fit(X_train_scaled, y_train,
                        validation_split=0.2, epochs=40, batch_size=16, verbose=0)

    loss, acc = model.evaluate(X_test_scaled, y_test, verbose=0)
    print(f"\n✅ Acurácia da Rede Neural (Teste): {acc:.2%}")

    # Exportação dos modelos para inferência no App
    model.save("modelo_humor_nn.h5")
    joblib.dump(scaler, "scaler_humor.pkl")
    joblib.dump(le, "label_encoder_humor.pkl")
    print("✅ Artefatos da Rede Neural exportados com sucesso.")


if __name__ == "__main__":
    treinar_rede_neural_humor()
