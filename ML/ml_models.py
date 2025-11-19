# ml_models.py
import pandas as pd
from db import conn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def carregar_dataset():
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

def treinar_modelo_sobrecarga():
    df = carregar_dataset()

    # Cria um alvo binário de risco de sobrecarga
    df["risco_sobrecarga"] = (
        (df["ESTRESSE"] >= 4) | (df["SOBRECARGA"] == 1)
    ).astype(int)

    features = [
        "VELOCIDADE_DIGITACAO",
        "TEMPO_PAUSA",
        "TEMPO_TELA_LIGADA",
        "TEMPO_INTERACAO",
        "TEMPO_MOUSE",
        "ENERGIA",
    ]

    X = df[features]
    y = df["risco_sobrecarga"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    print("\n===== Relatório do Modelo de Risco de Sobrecarga =====")
    print(classification_report(y_test, y_pred))

    # Salva o modelo e o scaler
    joblib.dump(model, "modelo_sobrecarga.pkl")
    joblib.dump(scaler, "scaler_sobrecarga.pkl")
    print("✅ Modelo de risco de sobrecarga salvo em 'modelo_sobrecarga.pkl'")
    print("✅ Scaler salvo em 'scaler_sobrecarga.pkl'")

if __name__ == "__main__":
    treinar_modelo_sobrecarga()
