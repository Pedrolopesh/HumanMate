# nn_humor.py
import pandas as pd
from db import conn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow.keras import layers, models
import joblib

def carregar_dataset_humor():
    query = """
        SELECT 
            m.EMAIL,
            m.DATA_REG,
            m.VELOCIDADE_DIGITACAO,
            m.TEMPO_PAUSA,
            m.TEMPO_TELA_LIGADA,
            m.TEMPO_INTERACAO,
            m.TEMPO_MOUSE,
            d.ENERGIA,
            d.ESTRESSE,
            d.SOBRECARGA,
            d.HUMOR
        FROM METRICAS_USUARIO m
        JOIN DIARIOS d
          ON d.EMAIL = m.EMAIL
         AND d.DATA_REG = m.DATA_REG
    """
    df = pd.read_sql(query, conn)
    return df

def treinar_rede_neural_humor():
    df = carregar_dataset_humor()

    features = [
        "VELOCIDADE_DIGITACAO",
        "TEMPO_PAUSA",
        "TEMPO_TELA_LIGADA",
        "TEMPO_INTERACAO",
        "TEMPO_MOUSE",
        "ENERGIA",
        "ESTRESSE",
    ]

    X = df[features].values

    # Codificar HUMOR para inteiros
    le = LabelEncoder()
    y = le.fit_transform(df["HUMOR"])  # 0..N-1

    # Treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Escalonar
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    num_classes = len(le.classes_)

    # Modelo simples
    model = models.Sequential([
        layers.Input(shape=(X_train_scaled.shape[1],)),
        layers.Dense(32, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    history = model.fit(
        X_train_scaled,
        y_train,
        validation_split=0.2,
        epochs=30,
        batch_size=16,
        verbose=1
    )

    loss, acc = model.evaluate(X_test_scaled, y_test, verbose=0)
    print(f"\n✅ Acurácia da rede neural na classificação de HUMOR: {acc:.2%}")

    # Salvar tudo
    model.save("modelo_humor_nn.h5")
    joblib.dump(scaler, "scaler_humor.pkl")
    joblib.dump(le, "label_encoder_humor.pkl")

    print("✅ Rede neural salva em 'modelo_humor_nn.h5'")
    print("✅ Scaler salvo em 'scaler_humor.pkl'")
    print("✅ LabelEncoder salvo em 'label_encoder_humor.pkl'")

if __name__ == "__main__":
    treinar_rede_neural_humor()
