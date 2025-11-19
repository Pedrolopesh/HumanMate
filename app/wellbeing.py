# wellbeing.py
from utils import formatar_tempo

def calcular_indice_bem_estar(
    humor: str,
    energia: int,
    estresse: int,
    pausas: int,
    tela: int,
    interacao: int,
    mouse: int
):
    # -----------------------------
    # 1) Normalização das entradas
    # -----------------------------

    # Humor → nota 0–100
    mapa_humor = {
        "Muito Bom": 100,
        "Bom": 80,
        "Neutro": 60,
        "Ruim": 40,
        "Muito Ruim": 20
    }
    humor_score = mapa_humor.get(humor, 60)

    # Energia (1 a 5) → 20, 40, 60, 80, 100
    energia_score = (energia - 1) * 20 + 20

    # Estresse → invertido (1 = bom, 5 = ruim)
    estresse_score = 100 - ((estresse - 1) * 20)

    # Pausas → tempo ideal seria ~10 min/hora → escala simples
    pausas_score = max(0, min(100, 100 - abs(pausas - 600) * 0.05))

    # Tela ligada → ideal ~6h
    tela_score = max(0, min(100, 100 - abs(tela - 21600) * 0.003))

    # Interação com mouse → indica engajamento saudável
    mouse_score = max(0, min(100, mouse * 0.02))

    # -----------------------------
    # 2) Cálculo do índice final
    # -----------------------------
    indice = (
        humor_score * 0.30 +
        energia_score * 0.20 +
        estresse_score * 0.20 +
        pausas_score * 0.10 +
        tela_score * 0.10 +
        mouse_score * 0.10
    )

    return round(indice, 2)
