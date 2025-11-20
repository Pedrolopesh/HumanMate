from datetime import date, datetime

from app.wellbeing import calcular_indice_bem_estar
from utils import read_choice, read_decimal, read_yesno, formatar_tempo
from db import conexao, conn, cursor
from utils import read_decimal

def perguntas_diarias(usuario):
    print("\n===============================================")
    print(f" Perguntas Diárias - Usuário: {usuario['email']} ")
    print("===============================================")

    humor = read_choice(
        ["Muito Bom", "Bom", "Neutro", "Ruim", "Muito Ruim"],
        "Como está seu humor hoje? "
    )

    foco_horas = read_decimal("Quantas horas produtivas você teve hoje? (ex: 2,5): ", positivo=True)
    sobrecarga = read_yesno("Você se sentiu sobrecarregado hoje?", False)
    dormiu_bem = read_yesno("Você dormiu bem? ", False)

    try:
        energia = int(input("Nível de energia (1 a 5): ").strip())
        if energia not in range(1, 6):
            raise ValueError
    except:
        print("Valor inválido. Definindo energia = 3.")
        energia = 3

    try:
        estresse = int(input("Nível de estresse (1 a 5): ").strip())
        if estresse not in range(1, 6):
            raise ValueError
    except:
        print("Valor inválido. Definindo estresse = 3.")
        estresse = 3

    registro = {
        "email": usuario["email"],
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "humor": humor,
        "foco_horas": float(foco_horas),
        "sobrecarga": sobrecarga,
        "dormiu_bem": dormiu_bem,
        "energia": energia,
        "estresse": estresse,
    }

    if conexao:
        try:
            sql = """
                INSERT INTO DIARIOS (
                    EMAIL,
                    DATA_REG,
                    HUMOR,
                    FOCO_HORAS,
                    SOBRECARGA,
                    DORMIU_BEM,
                    ENERGIA,
                    ESTRESSE,
                    CREATED_AT
                )
                VALUES (
                    :email,
                    TO_DATE(:data_hora, 'YYYY-MM-DD HH24:MI:SS'),
                    :humor,
                    :foco_horas,
                    :sobrecarga,
                    :dormiu_bem,
                    :energia,
                    :estresse,
                    TO_DATE(:data_hora, 'YYYY-MM-DD HH24:MI:SS')
                )
            """

            cursor.execute(sql, registro)
            conn.commit()

            print("📊 Respostas diárias armazenadas com sucesso!")
        except Exception as e:
            print("⚠️ Erro ao salvar no banco:", e)

    return registro

def listar_perguntas_diarias(email):
    print("\n===============================================")
    print(f" Histórico diário de: {email} ")
    print("===============================================")

    if not conexao:
        print("❌ Sem conexão com o banco. Não é possível consultar.")
        return

    try:
        sql = """
            SELECT 
                TO_CHAR(DATA_REG, 'YYYY-MM-DD'),
                HUMOR,
                FOCO_HORAS,
                SOBRECARGA,
                DORMIU_BEM,
                ENERGIA,
                ESTRESSE
            FROM DIARIOS
            WHERE EMAIL = :email
            ORDER BY DATA_REG DESC
        """

        cursor.execute(sql, {"email": email})
        rows = cursor.fetchall()

        if not rows:
            print("(Nenhum registro encontrado para este usuário.)")
            return

        for row in rows:
            data_reg, humor, foco, sobrecarga, dormiu, energia, estresse = row
            print("-------------------------------------------")
            print(f"Data: {data_reg}")
            print(f"Humor: {humor}")
            print(f"Foco (horas): {foco}")
            print(f"Sobrecarga: {'Sim' if sobrecarga == 1 else 'Não'}")
            print(f"Dormiu bem: {'Sim' if dormiu == 1 else 'Não'}")
            print(f"Energia: {energia}")
            print(f"Estresse: {estresse}")

    except Exception as e:
        print("⚠️ Erro ao consultar dados:", e)

import random
from datetime import date
from db import conexao, conn, cursor

def capturar_metricas_usuario(usuario):
    print("\n===============================================")
    print("  HumanMate Agent - Monitoramento Inteligente   ")
    print("===============================================")
    print("📡 O agente de IA está analisando suas atividades do dia...")
    print("⏳ Capturando métricas comportamentais...")

    # ================================
    # 1) Geração aleatória dos dados
    # ================================

    velocidade_digitacao = random.randint(150, 350)   # palavras por minuto
    tempo_pausa = random.randint(60, 900)             # 1 min a 15 min
    tempo_tela_ligada = random.randint(3600, 28800)   # 1h a 8h em segundos
    tempo_interacao = random.randint(1800, 21600)     # 30 min a 6h
    tempo_mouse = random.randint(300, 7200)           # 5 min a 2h

    print("\n🤖 O agente de IA registrou automaticamente:")
    print(f"• Velocidade de digitação: {velocidade_digitacao} ppm")
    print(f"• Tempo total de pausas: {tempo_pausa} segundos")
    print(f"• Tempo de tela ligada: {tempo_tela_ligada} segundos")
    print(f"• Tempo interagindo com o computador: {tempo_interacao} segundos")
    print(f"• Tempo mexendo o mouse: {tempo_mouse} segundos")

    print("\n📊 Esses dados serão usados para análises de:")
    print("   → produtividade")
    print("   → sobrecarga mental")
    print("   → padrões de trabalho")
    print("   → indicadores preditivos (Machine Learning)")
    print("===============================================\n")

    # Registro em formato dict
    registro = {
        "email": usuario["email"],
        "data": date.today().isoformat(),
        "velocidade_digitacao": velocidade_digitacao,
        "tempo_pausa": tempo_pausa,
        "tempo_tela_ligada": tempo_tela_ligada,
        "tempo_interacao": tempo_interacao,
        "tempo_mouse": tempo_mouse,
        "created_at": date.today().isoformat()
    }

    # =============================
    # 2) Salvar no banco Oracle
    # =============================
    if conexao:
        try:
            sql = """
                INSERT INTO METRICAS_USUARIO (
                    EMAIL,
                    DATA_REG,
                    VELOCIDADE_DIGITACAO,
                    TEMPO_PAUSA,
                    TEMPO_TELA_LIGADA,
                    TEMPO_INTERACAO,
                    TEMPO_MOUSE,
                    CREATED_AT
                )
                VALUES (
                    :email,
                    TO_DATE(:data_reg, 'YYYY-MM-DD'),
                    :velocidade_digitacao,
                    :tempo_pausa,
                    :tempo_tela_ligada,
                    :tempo_interacao,
                    :tempo_mouse,
                    TO_DATE(:created_at, 'YYYY-MM-DD')
                )
            """

            cursor.execute(sql, {
                "email": usuario["email"],
                "data_reg": date.today().isoformat(),
                "velocidade_digitacao": velocidade_digitacao,
                "tempo_pausa": tempo_pausa,
                "tempo_tela_ligada": tempo_tela_ligada,
                "tempo_interacao": tempo_interacao,
                "tempo_mouse": tempo_mouse,
                "created_at": date.today().isoformat()
            })

            conn.commit()
            print("🧠 Métricas comportamentais registradas com sucesso!\n")

        except Exception as e:
            print("⚠️ Erro ao salvar métricas no banco:", e)
    else:
        print("⚠️ Sem conexão com o banco. Métricas não foram registradas.")

    return registro

# metrics.py
from db import conexao, cursor
# metrics.py
from db import conexao, cursor

def listar_metricas_usuario(email: str):
    print("\n===============================================")
    print(f" Métricas registradas - Usuário: {email} ")
    print("===============================================")

    if not conexao:
        print("❌ Sem conexão com o banco. Não é possível consultar.")
        return

    try:
        sql = """
            SELECT 
                TO_CHAR(DATA_REG, 'YYYY-MM-DD'),
                VELOCIDADE_DIGITACAO,
                TEMPO_PAUSA,
                TEMPO_TELA_LIGADA,
                TEMPO_INTERACAO,
                TEMPO_MOUSE
            FROM METRICAS_USUARIO
            WHERE EMAIL = :email
            ORDER BY DATA_REG DESC
        """

        cursor.execute(sql, {"email": email})
        rows = cursor.fetchall()

        if not rows:
            print("(Nenhuma métrica registrada para este usuário.)")
            return

        for r in rows:
            data_reg, vel, pausa, tela, interacao, mouse = r
            print("-------------------------------------------")
            print(f"Data: {data_reg}")
            print(f"Velocidade digitação (ppm): {vel}")
            print(f"Tempo de pausas (s): {pausa}")
            print(f"Tempo tela ligada (s): {tela}")
            print(f"Tempo interação (s): {interacao}")
            print(f"Tempo mouse (s): {mouse}")

    except Exception as e:
        print("⚠️ Erro ao consultar métricas:", e)

def listar_tudo_usuario(email):
    print("\n============================================================")
    print(f" Histórico completo do usuário: {email} ")
    print("============================================================")

    if not conexao:
        print("❌ Sem conexão com o banco.")
        return

    try:
        sql = """
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
            ORDER BY d.DATA_REG DESC
        """

        cursor.execute(sql, {"email": email})
        rows = cursor.fetchall()

        if not rows:
            print("(Nenhum registro encontrado.)")
            return

        for r in rows:
            (
                data_hora, humor, foco, sobrecarga, dormiu, energia, estresse,
                vel, pausa, tela, interacao, mouse
            ) = r

            print("\n===================================================")
            print(f"📅 Registro de {data_hora}")
            print("---------------------------------------------------")
            print(f"Humor: {humor}")
            print(f"Foco (horas): {foco}")
            print(f"Sobrecarga: {'Sim' if sobrecarga == 1 else 'Não'}")
            print(f"Dormiu bem: {'Sim' if dormiu == 1 else 'Não'}")
            print(f"Nível de energia: {energia}")
            print(f"Nível de estresse: {estresse}")

            print("\n🖥️  Métricas comportamentais do agente de IA")
            print("---------------------------------------------------")
            print(f"Velocidade de digitação: {vel or '–'} ppm (palavras por minuto)")
            print(f"Tempo de pausas: {pausa or '–'}s ({formatar_tempo(pausa)})")
            print(f"Tempo de tela ligada: {tela or '–'}s ({formatar_tempo(tela)})")
            print(f"Tempo de interação: {interacao or '–'}s ({formatar_tempo(interacao)})")
            print(f"Tempo mexendo o mouse: {mouse or '–'}s ({formatar_tempo(mouse)})")

            ibe = calcular_indice_bem_estar(
                humor=r['humor'],
                energia=r['energia'],
                estresse=r['estresse'],
                pausas=pausa,
                tela=tela,
                interacao=interacao,
                mouse=mouse
            )
            print(f"Índice de Bem-Estar: {ibe}/100")

    except Exception as e:
        print("⚠️ Erro ao consultar dados:", e)