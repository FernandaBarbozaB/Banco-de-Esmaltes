import sqlite3

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

print("Esmalte cadastrado com sucesso!")
