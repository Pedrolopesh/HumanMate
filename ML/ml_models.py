# ml_models.py
import pandas as pd
from db import conn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

"""
MÓDULO DE MACHINE LEARNING (CLÁSSICO) - HUMANMATE
-------------------------------------------------
Objetivo: Treinar um modelo supervisionado para prever riscos de Burnout/Sobrecarga.
Algoritmo: Random Forest Classifier (escolhido pela robustez com dados não-lineares).
Input: Métricas de comportamento digital (teclado, mouse, tela).
Output: Classificação Binária (0 = Risco Baixo, 1 = Risco Elevado).
"""


def carregar_dataset():
    """
    Carrega e unifica dados passivos (monitoramento) e ativos (diários).
    Realiza um JOIN SQL para alinhar as métricas de comportamento com o relato do usuário.
    """
    print("🔄 Carregando dataset do Banco de Dados...")
    query = """
        SELECT 
            m.EMAIL, m.DATA_REG,
            m.VELOCIDADE_DIGITACAO, m.TEMPO_PAUSA, m.TEMPO_TELA_LIGADA,
            m.TEMPO_INTERACAO, m.TEMPO_MOUSE,
            d.ENERGIA, d.ESTRESSE, d.SOBRECARGA, d.HUMOR
        FROM METRICAS_USUARIO m
        JOIN DIARIOS d ON d.EMAIL = m.EMAIL AND d.DATA_REG = m.DATA_REG
    """
    # Lê direto via Pandas (Requisito: Integração com Banco de Dados)
    df = pd.read_sql(query, conn)
    return df


def treinar_modelo_sobrecarga():
    df = carregar_dataset()

    if df.empty:
        print("⚠️ Atenção: Dataset vazio. Execute o simulador de dados primeiro.")
        return

    # Feature Engineering: Criamos um target "Risco de Sobrecarga"
    # Consideramos risco se o usuário reportou Estresse Alto (>=4) OU Sobrecarga explícita.
    df["risco_sobrecarga"] = ((df["ESTRESSE"] >= 4) | (
        df["SOBRECARGA"] == 1)).astype(int)

    # Seleção de Features (X) baseada em comportamento digital
    features = [
        "VELOCIDADE_DIGITACAO", "TEMPO_PAUSA", "TEMPO_TELA_LIGADA",
        "TEMPO_INTERACAO", "TEMPO_MOUSE", "ENERGIA"
    ]

    X = df[features]
    y = df["risco_sobrecarga"]

    # Divisão Treino/Teste com estratificação para manter proporção das classes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Normalização (Essencial para performance do modelo)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Treinamento do Modelo Random Forest
    print("🤖 Treinando Random Forest para detecção de Burnout...")
    model = RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Avaliação
    y_pred = model.predict(X_test_scaled)
    print("\n===== Relatório de Performance (Burnout) =====")
    print(classification_report(y_test, y_pred))

    # Persistência dos Artefatos (para uso no App em tempo real)
    joblib.dump(model, "modelo_sobrecarga.pkl")
    joblib.dump(scaler, "scaler_sobrecarga.pkl")
    print("✅ Modelo e Scaler salvos com sucesso.")


if __name__ == "__main__":
    treinar_modelo_sobrecarga()
