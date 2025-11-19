from app.relatorio import gerar_relatorio_pdf
from db import conexao, conn, cursor
from monitor import perguntas_diarias, listar_perguntas_diarias, capturar_metricas_usuario, listar_metricas_usuario, \
    listar_tudo_usuario
from users import cadastrar_usuario, login_usuario

def resetar_banco():
    if not conexao:
        print("❌ Sem conexão com o banco.")
        return

    print("\n⚠️ ATENÇÃO: Esta ação irá apagar TODOS os dados do sistema.")
    print("⚠️ Isso inclui usuários, registros diários e métricas.")

    confirm = input("Digite 'SIM' para confirmar: ").strip().upper()
    if confirm != "SIM":
        print("❌ Operação cancelada.")
        return

    try:
        cursor.execute("DELETE FROM METRICAS_USUARIO")
        cursor.execute("DELETE FROM DIARIOS")
        cursor.execute("DELETE FROM USUARIOS")
        conn.commit()

        print("🔥 Todas as tabelas foram limpas com sucesso!")
    except Exception as e:
        print("⚠️ Erro ao limpar o banco:", e)


usuarios = []  # cada usuário será um dict

# =========================
# Sessão do usuário
# =========================
usuario_logado = None
diarios = []  # registros diários de bem-estar e produtividade

def menu_principal():
    global usuario_logado

    while True:
        print("\n=============================================")
        print("            HUMANMATE - MENU INICIAL         ")
        print("=============================================")

        # =======================
        # Menu quando NÃO logado
        # =======================
        if usuario_logado is None:
            print("[1] Cadastrar usuário")
            print("[2] Fazer login")
            print("[0] Sair")
            escolha = input("Escolha: ").strip()

            if escolha == "1":
                cadastrar_usuario()

            elif escolha == "2":
                usuario = login_usuario()
                if usuario:
                    usuario_logado = usuario

            elif escolha == "0":
                print("Encerrando o sistema... Até mais! 👋")
                break

            else:
                print("❌ Opção inválida. Tente novamente.")

        # =======================
        # Menu quando LOGADO
        # =======================
        else:
            print(f"Usuário logado: {usuario_logado['email']}")
            print("[3] Realizar perguntas diárias")
            print("[4] Ver respostas registradas")
            print("[5] Ver histórico completo")
            print("[6] Limpar dados de teste")
            print("[7] Gerar relatório detalhado")
            print("[0] Logout")
            print("[9] Sair do sistema")

            escolha = input("Escolha: ").strip()

            if escolha == "3":
                registro = perguntas_diarias(usuario_logado)
                diarios.append(registro)
                capturar_metricas_usuario(usuario_logado)

            elif escolha == "4":
                listar_perguntas_diarias(usuario_logado['email'])
                listar_metricas_usuario(usuario_logado['email'])

            elif escolha == "5":
                listar_tudo_usuario(usuario_logado['email'])

            elif escolha == "6":
                resetar_banco()

            elif escolha == "7":
                gerar_relatorio_pdf(usuario_logado["email"])

            elif escolha == "0":
                print(f"🔒 Logout efetuado para {usuario_logado['email']}")
                usuario_logado = None

            elif escolha == "9":
                print("Encerrando o sistema... Até mais! 👋")
                break

            else:
                print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
