import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================
# CORES DO PROGRAMA
# ==========================================

ROSA_ESCURO = "#C2185B"
ROSA = "#E91E63"
ROSA_CLARO = "#FCE4EC"
ROSA_BEM_CLARO = "#FFF5F8"
BRANCO = "#FFFFFF"
TEXTO = "#4A1F2F"


# ==========================================
# BANCO DE DADOS
# ==========================================

def conectar_banco():
    return sqlite3.connect("esmaltes.db")


# ==========================================
# ATUALIZAR A TABELA
# ==========================================

def atualizar_lista():
    # Apaga os dados que estão aparecendo na tabela
    for item in tabela.get_children():
        tabela.delete(item)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cor, marca
        FROM esmaltes
        ORDER BY id
    """)

    esmaltes = cursor.fetchall()

    conexao.close()

    # Coloca os esmaltes na tabela
    for esmalte in esmaltes:
        tabela.insert("", tk.END, values=esmalte)


# ==========================================
# CADASTRAR ESMALTE
# ==========================================

def cadastrar_esmalte():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastrar esmalte")
    janela_cadastro.geometry("400x350")
    janela_cadastro.configure(bg=ROSA_BEM_CLARO)
    janela_cadastro.resizable(False, False)

    titulo = tk.Label(
        janela_cadastro,
        text="💅 Cadastrar esmalte",
        font=("Arial", 20, "bold"),
        bg=ROSA_BEM_CLARO,
        fg=ROSA_ESCURO
    )
    titulo.pack(pady=20)

    # Nome
    tk.Label(
        janela_cadastro,
        text="Nome:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_nome = tk.Entry(
        janela_cadastro,
        font=("Arial", 12),
        width=30
    )
    entrada_nome.pack(pady=5)

    # Cor
    tk.Label(
        janela_cadastro,
        text="Cor:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_cor = tk.Entry(
        janela_cadastro,
        font=("Arial", 12),
        width=30
    )
    entrada_cor.pack(pady=5)

    # Marca
    tk.Label(
        janela_cadastro,
        text="Marca:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_marca = tk.Entry(
        janela_cadastro,
        font=("Arial", 12),
        width=30
    )
    entrada_marca.pack(pady=5)

    def salvar():
        nome = entrada_nome.get().strip()
        cor = entrada_cor.get().strip()
        marca = entrada_marca.get().strip()

        # Verifica se os campos estão preenchidos
        if nome == "" or cor == "" or marca == "":
            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos!"
            )
            return

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO esmaltes (nome, cor, marca)
            VALUES (?, ?, ?)
        """, (nome, cor, marca))

        conexao.commit()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Esmalte cadastrado com sucesso! 💗"
        )

        atualizar_lista()
        janela_cadastro.destroy()

    tk.Button(
        janela_cadastro,
        text="💗 Cadastrar",
        font=("Arial", 12, "bold"),
        bg=ROSA,
        fg=BRANCO,
        activebackground=ROSA_ESCURO,
        activeforeground=BRANCO,
        relief="flat",
        padx=20,
        pady=8,
        command=salvar
    ).pack(pady=20)


# ==========================================
# PROCURAR POR COR
# ==========================================

def procurar_por_cor():
    cor = entrada_pesquisa.get().strip()

    if cor == "":
        messagebox.showwarning(
            "Atenção",
            "Digite uma cor para pesquisar."
        )
        return

    # Limpa a tabela
    for item in tabela.get_children():
        tabela.delete(item)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cor, marca
        FROM esmaltes
        WHERE cor LIKE ?
        ORDER BY id
    """, ("%" + cor + "%",))

    esmaltes = cursor.fetchall()

    conexao.close()

    for esmalte in esmaltes:
        tabela.insert("", tk.END, values=esmalte)

    if len(esmaltes) == 0:
        messagebox.showinfo(
            "Pesquisa",
            "Nenhum esmalte encontrado. 💅"
        )


# ==========================================
# ALTERAR ESMALTE
# ==========================================

def alterar_esmalte():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione um esmalte na tabela primeiro."
        )
        return

    dados = tabela.item(selecionado[0], "values")

    id_esmalte = dados[0]
    nome_atual = dados[1]
    cor_atual = dados[2]
    marca_atual = dados[3]

    janela_alterar = tk.Toplevel(janela)
    janela_alterar.title("Alterar esmalte")
    janela_alterar.geometry("400x350")
    janela_alterar.configure(bg=ROSA_BEM_CLARO)
    janela_alterar.resizable(False, False)

    tk.Label(
        janela_alterar,
        text="✏️ Alterar esmalte",
        font=("Arial", 20, "bold"),
        bg=ROSA_BEM_CLARO,
        fg=ROSA_ESCURO
    ).pack(pady=20)

    # Nome
    tk.Label(
        janela_alterar,
        text="Nome:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_nome = tk.Entry(
        janela_alterar,
        font=("Arial", 12),
        width=30
    )
    entrada_nome.insert(0, nome_atual)
    entrada_nome.pack(pady=5)

    # Cor
    tk.Label(
        janela_alterar,
        text="Cor:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_cor = tk.Entry(
        janela_alterar,
        font=("Arial", 12),
        width=30
    )
    entrada_cor.insert(0, cor_atual)
    entrada_cor.pack(pady=5)

    # Marca
    tk.Label(
        janela_alterar,
        text="Marca:",
        font=("Arial", 12),
        bg=ROSA_BEM_CLARO,
        fg=TEXTO
    ).pack()

    entrada_marca = tk.Entry(
        janela_alterar,
        font=("Arial", 12),
        width=30
    )
    entrada_marca.insert(0, marca_atual)
    entrada_marca.pack(pady=5)

    def salvar_alteracao():
        novo_nome = entrada_nome.get().strip()
        nova_cor = entrada_cor.get().strip()
        nova_marca = entrada_marca.get().strip()

        if novo_nome == "" or nova_cor == "" or nova_marca == "":
            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos!"
            )
            return

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE esmaltes
            SET nome = ?, cor = ?, marca = ?
            WHERE id = ?
        """, (
            novo_nome,
            nova_cor,
            nova_marca,
            id_esmalte
        ))

        conexao.commit()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Esmalte alterado com sucesso! 💗"
        )

        atualizar_lista()
        janela_alterar.destroy()

    tk.Button(
        janela_alterar,
        text="💗 Salvar alteração",
        font=("Arial", 12, "bold"),
        bg=ROSA,
        fg=BRANCO,
        activebackground=ROSA_ESCURO,
        activeforeground=BRANCO,
        relief="flat",
        padx=20,
        pady=8,
        command=salvar_alteracao
    ).pack(pady=20)


# ==========================================
# EXCLUIR ESMALTE
# ==========================================

def excluir_esmalte():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione um esmalte na tabela primeiro."
        )
        return

    dados = tabela.item(selecionado[0], "values")

    id_esmalte = dados[0]
    nome = dados[1]

    resposta = messagebox.askyesno(
        "Confirmar exclusão",
        f"Tem certeza que deseja excluir:\n\n{nome}?"
    )

    if resposta:

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM esmaltes
            WHERE id = ?
        """, (id_esmalte,))

        conexao.commit()
        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Esmalte excluído com sucesso! 💗"
        )

        atualizar_lista()


# ==========================================
# LIMPAR PESQUISA
# ==========================================

def limpar_pesquisa():
    entrada_pesquisa.delete(0, tk.END)
    atualizar_lista()


# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()

janela.title("💅 Banco de Esmaltes")
janela.geometry("900x600")
janela.configure(bg=ROSA_BEM_CLARO)


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    janela,
    text="💅 Banco de Esmaltes 💅",
    font=("Arial", 26, "bold"),
    bg=ROSA_BEM_CLARO,
    fg=ROSA_ESCURO
)

titulo.pack(pady=(25, 5))


subtitulo = tk.Label(
    janela,
    text="Sua coleção de esmaltes organizada e linda! 🌸",
    font=("Arial", 11),
    bg=ROSA_BEM_CLARO,
    fg=TEXTO
)

subtitulo.pack(pady=(0, 20))


# ==========================================
# ÁREA DE BOTÕES
# ==========================================

frame_botoes = tk.Frame(
    janela,
    bg=ROSA_BEM_CLARO
)

frame_botoes.pack(pady=5)


botao_cadastrar = tk.Button(
    frame_botoes,
    text="💗 Cadastrar",
    font=("Arial", 11, "bold"),
    bg=ROSA,
    fg=BRANCO,
    activebackground=ROSA_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=15,
    pady=8,
    command=cadastrar_esmalte
)

botao_cadastrar.grid(row=0, column=0, padx=5)


botao_alterar = tk.Button(
    frame_botoes,
    text="✏️ Alterar",
    font=("Arial", 11, "bold"),
    bg=ROSA,
    fg=BRANCO,
    activebackground=ROSA_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=15,
    pady=8,
    command=alterar_esmalte
)

botao_alterar.grid(row=0, column=1, padx=5)


botao_excluir = tk.Button(
    frame_botoes,
    text="🗑️ Excluir",
    font=("Arial", 11, "bold"),
    bg=ROSA,
    fg=BRANCO,
    activebackground=ROSA_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=15,
    pady=8,
    command=excluir_esmalte
)

botao_excluir.grid(row=0, column=2, padx=5)


botao_atualizar = tk.Button(
    frame_botoes,
    text="🔄 Atualizar",
    font=("Arial", 11, "bold"),
    bg=ROSA,
    fg=BRANCO,
    activebackground=ROSA_ESCURO,
    activeforeground=BRANCO,
    relief="flat",
    padx=15,
    pady=8,
    command=atualizar_lista
)

botao_atualizar.grid(row=0, column=3, padx=5)


# ==========================================
# ÁREA DE PESQUISA
# ==========================================

frame_pesquisa = tk.Frame(
    janela,
    bg=ROSA_BEM_CLARO
)

frame_pesquisa.pack(pady=20)


tk.Label(
    frame_pesquisa,
    text="🔎 Procurar por cor:",
    font=("Arial", 11, "bold"),
    bg=ROSA_BEM_CLARO,
    fg=TEXTO
).grid(row=0, column=0, padx=5)


entrada_pesquisa = tk.Entry(
    frame_pesquisa,
    font=("Arial", 11),
    width=25
)

entrada_pesquisa.grid(row=0, column=1, padx=5)


tk.Button(
    frame_pesquisa,
    text="Pesquisar",
    font=("Arial", 10, "bold"),
    bg=ROSA_ESCURO,
    fg=BRANCO,
    activebackground=ROSA,
    activeforeground=BRANCO,
    relief="flat",
    padx=12,
    pady=5,
    command=procurar_por_cor
).grid(row=0, column=2, padx=5)


tk.Button(
    frame_pesquisa,
    text="Limpar",
    font=("Arial", 10),
    bg=BRANCO,
    fg=ROSA_ESCURO,
    relief="solid",
    padx=12,
    pady=5,
    command=limpar_pesquisa
).grid(row=0, column=3, padx=5)


# ==========================================
# TABELA
# ==========================================

frame_tabela = tk.Frame(
    janela,
    bg=ROSA_BEM_CLARO
)

frame_tabela.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


colunas = ("id", "nome", "cor", "marca")

tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas,
    show="headings"
)


tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome")
tabela.heading("cor", text="Cor")
tabela.heading("marca", text="Marca")


tabela.column("id", width=60, anchor="center")
tabela.column("nome", width=250)
tabela.column("cor", width=180)
tabela.column("marca", width=180)


tabela.pack(
    side="left",
    fill="both",
    expand=True
)


# Barra de rolagem

barra = ttk.Scrollbar(
    frame_tabela,
    orient="vertical",
    command=tabela.yview
)

barra.pack(
    side="right",
    fill="y"
)

tabela.configure(
    yscrollcommand=barra.set
)


# ==========================================
# RODAPÉ
# ==========================================

rodape = tk.Label(
    janela,
    text="Feito com Python + SQLite 💗",
    font=("Arial", 10),
    bg=ROSA_BEM_CLARO,
    fg=ROSA_ESCURO
)

rodape.pack(pady=10)


# ==========================================
# INICIA A LISTA
# ==========================================

atualizar_lista()


# ==========================================
# MANTÉM A JANELA ABERTA
# ==========================================

janela.mainloop()
