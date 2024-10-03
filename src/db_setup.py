import sqlite3

def criar_banco():
    # Conectar ou criar o banco de dados
    conn = sqlite3.connect('db/biblioteca.db')
    cursor = conn.cursor()

    # Criação da tabela de livros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        categoria TEXT,
        disponibilidade BOOLEAN NOT NULL
    )
    ''')

    # Criação da tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        matricula TEXT UNIQUE NOT NULL,
        email TEXT,
        telefone TEXT
    )
    ''')

    # Criação da tabela de empréstimos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprestimos (
        id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_livro INTEGER,
        id_usuario INTEGER,
        data_emprestimo TEXT NOT NULL,
        data_devolucao_prevista TEXT NOT NULL,
        data_devolucao_real TEXT,
        multa REAL DEFAULT 0,
        FOREIGN KEY(id_livro) REFERENCES livros(id_livro),
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
    )
    ''')

    # Confirmar as mudanças
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()