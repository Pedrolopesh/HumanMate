from datetime import date

from datetime import date

from app.db import conexao, conn, cursor
from utils import read_nonempty, read_choice, read_date

def cadastrar_usuario():
    print("\n==============================")
    print("      Cadastro de Usuário     ")
    print("==============================")

    email = read_nonempty("Email: ")
    senha = read_nonempty("Senha: ")
    sexo = read_choice(["Feminino", "Masculino"], "Sexo: ")
    data_nasc = read_date("Data de nascimento")
    cargo = read_nonempty("Cargo do usuário: ")

    if not conexao:
        print("❌ Sem conexão com o banco. Não é possível cadastrar agora.")
        return None

    # ================================
    # 1) Verificar se já existe no banco
    # ================================
    try:
        cursor.execute("SELECT 1 FROM USUARIOS WHERE EMAIL = :email", {"email": email})
        ja_existe = cursor.fetchone()

        if ja_existe:
            print("⚠️ Já existe um usuário cadastrado com esse email.")
            return None
    except Exception as e:
        print("⚠️ Erro ao verificar usuário no banco:", e)
        return None

    # ================================
    # 2) Inserir novo usuário
    # ================================
    try:
        sql = """
            INSERT INTO USUARIOS (
                EMAIL, SENHA, SEXO, DATA_NASCIMENTO, CARGO, CREATED_AT
            )
            VALUES (
                :email, :senha, :sexo,
                TO_DATE(:data_nasc, 'YYYY-MM-DD'),
                :cargo,
                TO_DATE(:created_at, 'YYYY-MM-DD')
            )
        """

        cursor.execute(sql, {
            "email": email,
            "senha": senha,
            "sexo": sexo,
            "data_nasc": data_nasc.isoformat(),
            "cargo": cargo,
            "created_at": date.today().isoformat()
        })

        conn.commit()
        print("✅ Usuário cadastrado com sucesso no banco!")

        return {
            "email": email,
            "senha": senha,
            "sexo": sexo,
            "data_nascimento": data_nasc.isoformat(),
            "cargo": cargo
        }

    except Exception as e:
        print("❌ Erro ao salvar usuário no banco:", e)
        return None

def login_usuario():
    print("\n==============================")
    print("         Login do Usuário     ")
    print("==============================")

    if not conexao:
        print("❌ Sem conexão com o banco. Não é possível realizar login.")
        return None

    email = read_nonempty("Email: ")
    senha = read_nonempty("Senha: ")

    try:
        sql = """
            SELECT EMAIL, SENHA, SEXO, DATA_NASCIMENTO, CARGO
            FROM USUARIOS
            WHERE EMAIL = :email
        """
        cursor.execute(sql, {"email": email})
        row = cursor.fetchone()

        # Caso não encontre o usuário
        if not row:
            print("❌ Usuário não encontrado.")
            return None

        email_db, senha_db, sexo_db, data_nasc_db, cargo_db = row

        # Validar senha
        if senha != senha_db:
            print("❌ Senha incorreta.")
            return None

        # Login OK → montar o dicionário
        usuario = {
            "email": email_db,
            "senha": senha_db,
            "sexo": sexo_db,
            "data_nascimento": (
                data_nasc_db.strftime("%Y-%m-%d")
                if hasattr(data_nasc_db, "strftime")
                else data_nasc_db
            ),
            "cargo": cargo_db,
        }

        print("✅ Login realizado com sucesso!")
        return usuario

    except Exception as e:
        print("⚠️ Erro ao fazer login no banco:", e)
        return None
