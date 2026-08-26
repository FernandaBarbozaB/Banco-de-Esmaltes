import sqlite3


def cadastrar_esmalte():
    nome = input("Nome do esmalte: ")
    cor = input("Cor: ")
    marca = input("Marca: ")

    conexao = sqlite3.connect("esmaltes.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO esmaltes (nome, cor, marca)
        VALUES (?, ?, ?)
    """, (nome, cor, marca))

    conexao.commit()
    conexao.close()

    print("\nEsmalte cadastrado com sucesso!")


def listar_esmaltes():
    conexao = sqlite3.connect("esmaltes.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM esmaltes")

    esmaltes = cursor.fetchall()

    if len(esmaltes) == 0:
        print("\nNenhum esmalte cadastrado.")

    else:
        print("\n========== ESMALTES ==========")

        for esmalte in esmaltes:
            print(
                "ID:", esmalte[0],
                "| Nome:", esmalte[1],
                "| Cor:", esmalte[2],
                "| Marca:", esmalte[3]
            )

    conexao.close()


def procurar_por_cor():
    cor = input("Qual cor você quer procurar? ")

    conexao = sqlite3.connect("esmaltes.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM esmaltes
        WHERE cor = ?
    """, (cor,))

    esmaltes = cursor.fetchall()

    if len(esmaltes) == 0:
        print("\nNenhum esmalte encontrado.")

    else:
        print("\n========== RESULTADOS ==========")

        for esmalte in esmaltes:
            print(
                "ID:", esmalte[0],
                "| Nome:", esmalte[1],
                "| Cor:", esmalte[2],
                "| Marca:", esmalte[3]
            )

    conexao.close()


def alterar_esmalte():
    id_esmalte = input("Digite o ID do esmalte que deseja alterar: ")

    conexao = sqlite3.connect("esmaltes.db")
    cursor = conexao.cursor()

    # Primeiro verificamos se o esmalte existe
    cursor.execute("""
        SELECT * FROM esmaltes
        WHERE id = ?
    """, (id_esmalte,))

    esmalte = cursor.fetchone()

    if esmalte is None:
        print("\nNenhum esmalte encontrado com esse ID.")
        conexao.close()
        return

    print("\nEsmalte atual:")
    print(
        "Nome:", esmalte[1],
        "| Cor:", esmalte[2],
        "| Marca:", esmalte[3]
    )

    nome = input("Novo nome: ")
    cor = input("Nova cor: ")
    marca = input("Nova marca: ")

    cursor.execute("""
        UPDATE esmaltes
        SET nome = ?, cor = ?, marca = ?
        WHERE id = ?
    """, (nome, cor, marca, id_esmalte))

    conexao.commit()
    conexao.close()

    print("\nEsmalte alterado com sucesso!")


def excluir_esmalte():
    id_esmalte = input("Digite o ID do esmalte que deseja excluir: ")

    conexao = sqlite3.connect("esmaltes.db")
    cursor = conexao.cursor()

    # Verificamos se o esmalte existe
    cursor.execute("""
        SELECT * FROM esmaltes
        WHERE id = ?
    """, (id_esmalte,))

    esmalte = cursor.fetchone()

    if esmalte is None:
        print("\nNenhum esmalte encontrado com esse ID.")
        conexao.close()
        return

    print("\nVocê escolheu:")
    print(
        "ID:", esmalte[0],
        "| Nome:", esmalte[1],
        "| Cor:", esmalte[2],
        "| Marca:", esmalte[3]
    )

    confirmacao = input("\nTem certeza que deseja excluir? (s/n): ")

    if confirmacao.lower() == "s":

        cursor.execute("""
            DELETE FROM esmaltes
            WHERE id = ?
        """, (id_esmalte,))

        conexao.commit()

        print("\nEsmalte excluído com sucesso!")

    else:
        print("\nExclusão cancelada.")

    conexao.close()


# ==============================
# MENU PRINCIPAL
# ==============================

while True:

    print("""
========================================
          💅 BANCO DE ESMALTES
========================================

1 - Cadastrar esmalte
2 - Listar esmaltes
3 - Procurar por cor
4 - Alterar esmalte
5 - Excluir esmalte
0 - Sair

========================================
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_esmalte()

    elif opcao == "2":
        listar_esmaltes()

    elif opcao == "3":
        procurar_por_cor()

    elif opcao == "4":
        alterar_esmalte()

    elif opcao == "5":
        excluir_esmalte()

    elif opcao == "0":
        print("\nAté logo! 💅")
        break

    else:
        print("\nOpção inválida! Escolha uma opção do menu.")
