# relatorio.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from app.db import conn
from wellbeing import calcular_indice_bem_estar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def carregar_dataset_completo(email):
    query = """
        SELECT 
            TO_CHAR(d.DATA_REG, 'YYYY-MM-DD HH24:MI:SS') AS DATA_HORA,
            d.HUMOR,
            d.FOCO_HORAS,
            d.SOBRECARGA,
            d.DORMIU_BEM,
            d.ENERGIA,
            d.ESTRESSE,
            m.VELOCIDADE_DIGITACAO,
            m.TEMPO_PAUSA,
            m.TEMPO_TELA_LIGADA,
            m.TEMPO_INTERACAO,
            m.TEMPO_MOUSE
        FROM DIARIOS d
        LEFT JOIN METRICAS_USUARIO m
          ON m.EMAIL = d.EMAIL
         AND m.DATA_REG = d.DATA_REG
        WHERE d.EMAIL = :email
        ORDER BY d.DATA_REG
    """
    return pd.read_sql(query, conn, params={"email": email})


def gerar_graficos(df, email):
    df["DATA"] = pd.to_datetime(df["DATA_HORA"])

    # --- Gráfico 1: Humor x Data ---
    plt.figure(figsize=(10, 4))
    plt.plot(df["DATA"], df["ENERGIA"], label="Energia")
    plt.plot(df["DATA"], df["ESTRESSE"], label="Estresse")
    plt.legend()
    plt.title(f"Humor & Energia ao longo do tempo - {email}")
    plt.ylabel("Escala 1 a 5")
    plt.grid()
    plt.savefig("grafico_humor_energia.png")
    plt.close()

    # --- Gráfico 2: Tempo de tela x Dia ---
    plt.figure(figsize=(10, 4))
    plt.plot(df["DATA"], df["TEMPO_TELA_LIGADA"]/3600, label="Tela Ligada (horas)")
    plt.title("Uso de Tela por Dia")
    plt.grid()
    plt.savefig("grafico_tela.png")
    plt.close()

    # --- Gráfico 3: Índice de Bem-Estar ---
    ibes = []
    for i, row in df.iterrows():
        ibes.append(calcular_indice_bem_estar(
            row["HUMOR"], row["ENERGIA"], row["ESTRESSE"],
            row["TEMPO_PAUSA"] or 0,
            row["TEMPO_TELA_LIGADA"] or 0,
            row["TEMPO_INTERACAO"] or 0,
            row["TEMPO_MOUSE"] or 0,
        ))
    df["IBE"] = ibes

    plt.figure(figsize=(10, 4))
    plt.plot(df["DATA"], df["IBE"], marker="o", label="Índice Bem-Estar")
    plt.title("Índice de Bem-Estar ao longo do tempo")
    plt.grid()
    plt.savefig("grafico_ibe.png")
    plt.close()

    return df


def gerar_relatorio_pdf(email):
    df = carregar_dataset_completo(email)
    df = gerar_graficos(df, email)

    pdf = canvas.Canvas("relatorio_humanmate.pdf", pagesize=A4)
    w, h = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, h - 50, f"Relatório HumanMate - {email}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, h - 90, "◼ Gráfico: Energia x Estresse")
    pdf.drawImage("grafico_humor_energia.png", 30, h - 350, width=500, height=220)

    pdf.showPage()
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, h - 90, "◼ Tempo de Tela")
    pdf.drawImage("grafico_tela.png", 30, h - 350, width=500, height=220)

    pdf.showPage()
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, h - 90, "◼ Índice de Bem-Estar")
    pdf.drawImage("grafico_ibe.png", 30, h - 350, width=500, height=220)

    media_ibe = round(df["IBE"].mean(), 2)
    pdf.drawString(30, 200, f"Média geral do Índice de Bem-Estar: {media_ibe}")

    pdf.drawString(30, 170,
                   "Insight: Valores abaixo de 60 indicam risco leve; abaixo de 50 = risco elevado.")

    pdf.save()

    print("📄 Relatório gerado: relatorio_humanmate.pdf")
