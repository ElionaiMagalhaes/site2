import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime


# Funções para abrir as janelas de funcionalidades
# Função para cadastrar um livro no banco de dados
def cadastrar_livro():
    # Conectar ao banco de dados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Inserir os dados do livro na tabela
    cursor.execute('''
    INSERT INTO livros (titulo, autor, categoria, disponibilidade) VALUES (?, ?, ?, ?)
    ''', (titulo_entry.get(), autor_entry.get(), categoria_entry.get(), True))

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

    # Limpar os campos após o cadastro
    titulo_entry.delete(0, tk.END)
    autor_entry.delete(0, tk.END)
    categoria_entry.delete(0, tk.END)

    # Exibir uma mensagem de confirmação
    messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")

# Função para abrir a janela de cadastro de livros
def abrir_janela_cadastro_livros():
    janela_livros = tk.Toplevel()
    janela_livros.title("Cadastro de Livros")
    janela_livros.geometry("400x300")

    # Label e campo para o título do livro
    tk.Label(janela_livros, text="Título:").pack(pady=5)
    global titulo_entry
    titulo_entry = tk.Entry(janela_livros, width=40)
    titulo_entry.pack(pady=5)

    # Label e campo para o autor do livro
    tk.Label(janela_livros, text="Autor:").pack(pady=5)
    global autor_entry
    autor_entry = tk.Entry(janela_livros, width=40)
    autor_entry.pack(pady=5)

    # Label e campo para a categoria do livro
    tk.Label(janela_livros, text="Categoria:").pack(pady=5)
    global categoria_entry
    categoria_entry = tk.Entry(janela_livros, width=40)
    categoria_entry.pack(pady=5)

    # Botão para salvar o livro
    ttk.Button(janela_livros, text="Cadastrar Livro", command=cadastrar_livro).pack(pady=20)



#########################################################################################################
# Função para cadastrar um usuário no banco de dados
def cadastrar_usuario():
    # Conectar ao banco de dados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Inserir os dados do usuário na tabela
    cursor.execute('''
    INSERT INTO usuarios (nome, matricula, email, telefone) VALUES (?, ?, ?, ?)
    ''', (nome_entry.get(), matricula_entry.get(), email_entry.get(), telefone_entry.get()))

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

    # Limpar os campos após o cadastro
    nome_entry.delete(0, tk.END)
    matricula_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)

    # Exibir uma mensagem de confirmação
    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

# Função para abrir a janela de cadastro de usuários
def abrir_janela_cadastro_usuarios():
    janela_usuarios = tk.Toplevel()
    janela_usuarios.title("Cadastro de Usuários")
    janela_usuarios.geometry("400x400")

    # Label e campo para o nome do usuário
    tk.Label(janela_usuarios, text="Nome:").pack(pady=5)
    global nome_entry
    nome_entry = tk.Entry(janela_usuarios, width=40)
    nome_entry.pack(pady=5)

    # Label e campo para a matrícula do usuário
    tk.Label(janela_usuarios, text="Matrícula:").pack(pady=5)
    global matricula_entry
    matricula_entry = tk.Entry(janela_usuarios, width=40)
    matricula_entry.pack(pady=5)

    # Label e campo para o email do usuário
    tk.Label(janela_usuarios, text="E-mail:").pack(pady=5)
    global email_entry
    email_entry = tk.Entry(janela_usuarios, width=40)
    email_entry.pack(pady=5)

    # Label e campo para o telefone do usuário
    tk.Label(janela_usuarios, text="Telefone:").pack(pady=5)
    global telefone_entry
    telefone_entry = tk.Entry(janela_usuarios, width=40)
    telefone_entry.pack(pady=5)

    # Botão para salvar o usuário
    ttk.Button(janela_usuarios, text="Cadastrar Usuário", command=cadastrar_usuario).pack(pady=20)




#######################################################################################################
# Função para registrar o empréstimo
def registrar_emprestimo():
    # Verificar se há um livro e um usuário selecionado
    if not livro_selecionado.get() or not usuario_selecionado.get():
        messagebox.showwarning("Erro", "Você deve selecionar um livro e um usuário.")
        return

    # Conectar ao banco de dados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Atualizar a disponibilidade do livro para False (indisponível)
    cursor.execute('''
    UPDATE livros SET disponibilidade = ? WHERE titulo = ?
    ''', (False, livro_selecionado.get()))

    # Inserir o registro de empréstimo
    cursor.execute('''
    INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, data_devolucao_prevista, multa)
    VALUES ((SELECT id_livro FROM livros WHERE titulo = ?), (SELECT id_usuario FROM usuarios WHERE nome = ?), ?, ?, 0)
    ''', (livro_selecionado.get(), usuario_selecionado.get(), data_emprestimo_entry.get(), data_devolucao_entry.get()))

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

    # Limpar as seleções
    livro_selecionado.set("")
    usuario_selecionado.set("")

    # Exibir uma mensagem de sucesso
    messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")






####################################################################################################3
# Função para abrir a janela de registro de empréstimos
def abrir_janela_emprestimos():
    janela_emprestimos = tk.Toplevel()
    janela_emprestimos.title("Registro de Empréstimos")
    janela_emprestimos.geometry("400x400")

    # Conectar ao banco de dados para obter livros disponíveis e usuários
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Obter os livros disponíveis
    cursor.execute("SELECT titulo FROM livros WHERE disponibilidade = 1")
    livros = [row[0] for row in cursor.fetchall()]

    # Obter os usuários
    cursor.execute("SELECT nome FROM usuarios")
    usuarios = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Seleção de Livro
    tk.Label(janela_emprestimos, text="Selecione um Livro:").pack(pady=5)
    global livro_selecionado
    livro_selecionado = tk.StringVar()
    ttk.Combobox(janela_emprestimos, textvariable=livro_selecionado, values=livros, state="readonly").pack(pady=5)

    # Seleção de Usuário
    tk.Label(janela_emprestimos, text="Selecione um Usuário:").pack(pady=5)
    global usuario_selecionado
    usuario_selecionado = tk.StringVar()
    ttk.Combobox(janela_emprestimos, textvariable=usuario_selecionado, values=usuarios, state="readonly").pack(pady=5)

    # Data de Empréstimo
    tk.Label(janela_emprestimos, text="Data de Empréstimo:").pack(pady=5)
    global data_emprestimo_entry
    data_emprestimo_entry = DateEntry(janela_emprestimos, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_emprestimo_entry.pack(pady=5)

    # Data de Devolução Prevista
    tk.Label(janela_emprestimos, text="Data de Devolução Prevista:").pack(pady=5)
    global data_devolucao_entry
    data_devolucao_entry = DateEntry(janela_emprestimos, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_devolucao_entry.pack(pady=5)

    # Botão para salvar o empréstimo
    ttk.Button(janela_emprestimos, text="Registrar Empréstimo", command=registrar_emprestimo).pack(pady=20)








# Função para registrar a devolução de um livro
def registrar_devolucao():
    if not livro_devolucao_selecionado.get():
        messagebox.showwarning("Erro", "Você deve selecionar um livro para devolução.")
        return

    # Conectar ao banco de dados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Obter as informações do empréstimo selecionado
    cursor.execute('''
    SELECT data_devolucao_prevista FROM emprestimos
    WHERE id_livro = (SELECT id_livro FROM livros WHERE titulo = ?) AND data_devolucao_real IS NULL
    ''', (livro_devolucao_selecionado.get(),))
    resultado = cursor.fetchone()

    if not resultado:
        messagebox.showwarning("Erro", "Nenhum empréstimo ativo encontrado para o livro selecionado.")
        conn.close()
        return

    # Corrigir a conversão de data para o formato correto
    data_devolucao_prevista = datetime.strptime(resultado[0], "%d/%m/%y")

    # Calcular multa se a devolução estiver atrasada
    data_devolucao_real = datetime.strptime(data_devolucao_entry.get(), "%d-%m-%Y")
    dias_atraso = (data_devolucao_real - data_devolucao_prevista).days
    multa = max(dias_atraso * 2, 0)  # Exemplo: R$2 por dia de atraso

    # Atualizar o registro de empréstimo com a data de devolução real e multa
    cursor.execute('''
    UPDATE emprestimos
    SET data_devolucao_real = ?, multa = ?
    WHERE id_livro = (SELECT id_livro FROM livros WHERE titulo = ?) AND data_devolucao_real IS NULL
    ''', (data_devolucao_real.strftime("%Y-%m-%d"), multa, livro_devolucao_selecionado.get()))

    # Atualizar a disponibilidade do livro
    cursor.execute('''
    UPDATE livros
    SET disponibilidade = 1
    WHERE titulo = ?
    ''', (livro_devolucao_selecionado.get(),))

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

    # Limpar a seleção
    livro_devolucao_selecionado.set("")
    messagebox.showinfo("Sucesso", f"Devolução registrada com sucesso! Multa: R${multa:.2f}")






# Função para abrir a janela de devolução de livros
# def abrir_janela_devolucao():
#     janela_devolucao = tk.Toplevel()
#     janela_devolucao.title("Devolução de Livros")
#     janela_devolucao.geometry("400x300")

#     # Conectar ao banco de dados para obter livros emprestados
#     conn = sqlite3.connect('db/biblioteca.db')
#     cursor = conn.cursor()

#     # Obter os livros que estão emprestados (data_devolucao_real ainda nula)
#     cursor.execute('''
#     SELECT titulo FROM livros
#     WHERE id_livro IN (SELECT id_livro FROM emprestimos WHERE data_devolucao_real IS NULL)
#     ''')
#     livros_emprestados = [row[0] for row in cursor.fetchall()]

#     conn.close()

#     # Seleção de Livro para Devolução
#     tk.Label(janela_devolucao, text="Selecione um Livro:").pack(pady=5)
#     global livro_devolucao_selecionado
#     livro_devolucao_selecionado = tk.StringVar()
#     ttk.Combobox(janela_devolucao, textvariable=livro_devolucao_selecionado, values=livros_emprestados, state="readonly").pack(pady=5)

#     # Data de Devolução Real
#     tk.Label(janela_devolucao, text="Data de Devolução (dd/mm/yyyy):").pack(pady=5)
#     global data_devolucao_entry
#     data_devolucao_entry = tk.Entry(janela_devolucao, width=40)
#     data_devolucao_entry.pack(pady=5)

#     # Botão para registrar a devolução
#     ttk.Button(janela_devolucao, text="Registrar Devolução", command=registrar_devolucao).pack(pady=20)









######################################################################################################
def abrir_janela_devolucao():
    
    janela_devolucao = tk.Toplevel()
    janela_devolucao.title("Devolução de Livros")
    janela_devolucao.geometry("400x300")

    # Conectar ao banco de dados para obter livros emprestados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Obter os livros que estão emprestados (data_devolucao_real ainda nula)
    cursor.execute('''
    SELECT titulo FROM livros
    WHERE id_livro IN (SELECT id_livro FROM emprestimos WHERE data_devolucao_real IS NULL)
    ''')
    livros_emprestados = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Seleção de Livro para Devolução
    tk.Label(janela_devolucao, text="Selecione um Livro:").pack(pady=5)
    global livro_devolucao_selecionado
    livro_devolucao_selecionado = tk.StringVar()
    ttk.Combobox(janela_devolucao, textvariable=livro_devolucao_selecionado, values=livros_emprestados, state="readonly").pack(pady=5)

    # Data de Devolução Real
    tk.Label(janela_devolucao, text="Data de Devolução (yyyy-mm-dd):").pack(pady=5)
    global data_devolucao_entry
    data_devolucao_entry = tk.Entry(janela_devolucao, width=40)
    data_devolucao_entry.pack(pady=5)

    # Botão para registrar a devolução
    ttk.Button(janela_devolucao, text="Registrar Devolução", command=registrar_devolucao).pack(pady=20)

# Aqui você define o botão após a função já estar definida
    btn_devolucao = ttk.Button(root, text="Devolução de Livros", command=abrir_janela_devolucao)
    btn_devolucao.pack(pady=10)









##################################################################################################
# Criação da janela principal
root = tk.Tk()
root.title("Sistema de Controle de Empréstimo de Livros")
root.geometry("400x300")

# Criação de um label de título
titulo = tk.Label(root, text="Bem-vindo ao Sistema de Biblioteca", font=("Helvetica", 16))
titulo.pack(pady=20)

# Botão para Cadastro de Livros
btn_cadastro_livros = ttk.Button(root, text="Cadastro de Livros", command=abrir_janela_cadastro_livros)
btn_cadastro_livros.pack(pady=10)

# Botão para Cadastro de Usuários
btn_cadastro_usuarios = ttk.Button(root, text="Cadastro de Usuários", command=abrir_janela_cadastro_usuarios)
btn_cadastro_usuarios.pack(pady=10)

# Botão para Registro de Empréstimos
btn_emprestimos = ttk.Button(root, text="Registro de Empréstimos", command=abrir_janela_emprestimos)
btn_emprestimos.pack(pady=10)

# Botão para Devolução de Livros
btn_devolucao = ttk.Button(root, text="Devolução de Livros", command=abrir_janela_devolucao)
btn_devolucao.pack(pady=10)

# Rodar o loop principal do Tkinter
root.mainloop()