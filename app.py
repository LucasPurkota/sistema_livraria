import sqlite3
import csv
import os
import shutil
from datetime import datetime

class GerenciadorLivraria:
    def __init__(self):
        self.diretorio_base = "meu_sistema_livraria"
        self.diretorio_backups = os.path.join(self.diretorio_base, "backups")
        self.diretorio_data = os.path.join(self.diretorio_base, "data")
        self.diretorio_exports = os.path.join(self.diretorio_base, "exports")
        self.arquivo_db = os.path.join(self.diretorio_data, "livraria.db")
        
        self.criar_diretorios()
        self.criar_tabela()
    
    def criar_diretorios(self):
        try:
            os.makedirs(self.diretorio_backups, exist_ok=True)
            os.makedirs(self.diretorio_data, exist_ok=True)
            os.makedirs(self.diretorio_exports, exist_ok=True)
        except Exception as e:
            print(f"Erro ao criar diretórios: {e}")
    
    def criar_tabela(self):
        try:
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER,
                    preco REAL
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
    
    def fazer_backup(self):
        try:
            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_backup = f"backup_livraria_{data_atual}.db"
            caminho_backup = os.path.join(self.diretorio_backups, nome_backup)
            
            shutil.copy2(self.arquivo_db, caminho_backup)
            print(f"Backup criado: {nome_backup}")
            
            self.limpar_backups_antigos()
            
        except Exception as e:
            print(f"Erro ao fazer backup: {e}")
    
    def limpar_backups_antigos(self):
        try:
            arquivos = os.listdir(self.diretorio_backups)
            arquivos_backup = [f for f in arquivos if f.startswith("backup_livraria") and f.endswith(".db")]
            
            if len(arquivos_backup) > 5:
                arquivos_backup.sort()
                arquivos_para_remover = arquivos_backup[:-5]
                
                for arquivo in arquivos_para_remover:
                    caminho_arquivo = os.path.join(self.diretorio_backups, arquivo)
                    os.remove(caminho_arquivo)
                    print(f"Backup antigo removido: {arquivo}")
                    
        except Exception as e:
            print(f"Erro ao limpar backups antigos: {e}")
    
    def adicionar_livro(self):
        try:
            
            titulo = input("Digite o título do livro: ")
            autor = input("Digite o autor do livro: ")
            
            while True:
                try:
                    ano = int(input("Digite o ano de publicação: "))
                    break
                except ValueError:
                    print("Ano deve ser um número inteiro!")
            
            while True:
                try:
                    preco = float(input("Digite o preço do livro: "))
                    break
                except ValueError:
                    print("Preço deve ser um número!")
            
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (titulo, autor, ano, preco))
            conn.commit()
            conn.close()
            
            print("Livro adicionado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao adicionar livro: {e}")
    
    def exibir_livros(self):
        try:
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros')
            livros = cursor.fetchall()
            conn.close()
            
            if not livros:
                print("Nenhum livro cadastrado.")
                return
            
            print("\n--- LIVROS CADASTRADOS ---")
            print("ID | Título | Autor | Ano | Preço")
            print("-" * 60)
            for livro in livros:
                print(f"{livro[0]} | {livro[1]} | {livro[2]} | {livro[3]} | R$ {livro[4]:.2f}")
            
            print("-" * 60)
                
        except Exception as e:
            print(f"Erro ao exibir livros: {e}")
    
    def atualizar_preco(self):
        try:
            self.exibir_livros()
            id_livro = input("Digite o ID do livro para atualizar o preço: ")
            
            while True:
                try:
                    novo_preco = float(input("Digite o novo preço: "))
                    break
                except ValueError:
                    print("Preço deve ser um número!")
            
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', (novo_preco, id_livro))
            
            if cursor.rowcount > 0:
                print("Preço atualizado com sucesso!")
            else:
                print("Livro não encontrado!")
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao atualizar preço: {e}")
    
    def remover_livro(self):
        try:
            self.exibir_livros()
            id_livro = input("Digite o ID do livro para remover: ")
            
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            
            if cursor.rowcount > 0:
                print("Livro removido com sucesso!")
            else:
                print("Livro não encontrado!")
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao remover livro: {e}")
    
    def buscar_por_autor(self):
        try:
            autor = input("Digite o nome do autor: ")
            
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros WHERE autor LIKE ?', (f'%{autor}%',))
            livros = cursor.fetchall()
            conn.close()
            
            if not livros:
                print(f"Nenhum livro encontrado para o autor: {autor}")
                return
            
            print(f"\n--- LIVROS DO AUTOR: {autor.upper()} ---")
            print("ID | Título | Autor | Ano | Preço")
            print("-" * 60)
            for livro in livros:
                print(f"{livro[0]} | {livro[1]} | {livro[2]} | {livro[3]} | R$ {livro[4]:.2f}")
            
            print("-" * 60)
                
        except Exception as e:
            print(f"Erro ao buscar por autor: {e}")
    
    def exportar_csv(self):
        try:
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM livros')
            livros = cursor.fetchall()
            conn.close()
            
            if not livros:
                print("Nenhum livro para exportar.")
                return
            
            caminho_csv = os.path.join(self.diretorio_exports, "livros_exportados.csv")
            
            with open(caminho_csv, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(['ID', 'Título', 'Autor', 'Ano', 'Preço'])
                writer.writerows(livros)
            
            print(f"Dados exportados para: {caminho_csv}")
            
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
    
    def importar_csv(self):
        try:
            arquivo_csv = input("Digite o caminho do arquivo CSV para importar: ")
            caminho_csv = os.path.join(self.diretorio_exports, arquivo_csv)
            
            if not os.path.exists(caminho_csv):
                print("Arquivo CSV não encontrado!")
                return
            
            conn = sqlite3.connect(self.arquivo_db)
            cursor = conn.cursor()
            
            with open(caminho_csv, 'r', encoding='utf-8') as arquivo:
                reader = csv.reader(arquivo)
                next(reader)
                
                livros_importados = 0
                for linha in reader:
                    if len(linha) >= 5:
                        cursor.execute('''
                            INSERT OR IGNORE INTO livros (id, titulo, autor, ano_publicacao, preco)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (linha[0], linha[1], linha[2], linha[3], linha[4]))
                        livros_importados += 1
            
            conn.commit()
            conn.close()
            
            print(f"{livros_importados} livros importados com sucesso!")
            
        except Exception as e:
            print(f"Erro ao importar CSV: {e}")
    
    def menu(self):
        while True:
            print("\n=== SISTEMA DE GERENCIAMENTO DE LIVRARIA ===")
            print("1. Adicionar novo livro")
            print("2. Exibir todos os livros")
            print("3. Atualizar preço de um livro")
            print("4. Remover um livro")
            print("5. Buscar livros por autor")
            print("6. Exportar dados para CSV")
            print("7. Importar dados de CSV")
            print("8. Fazer backup do banco de dados")
            print("9. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.adicionar_livro()
                input("Pressione Enter para continuar...")
            elif opcao == '2':
                self.exibir_livros()
                input("Pressione Enter para continuar...")
            elif opcao == '3':
                self.atualizar_preco()
                input("Pressione Enter para continuar...")
            elif opcao == '4':
                self.remover_livro()
                input("Pressione Enter para continuar...")
            elif opcao == '5':
                self.buscar_por_autor()
                input("Pressione Enter para continuar...")
            elif opcao == '6':
                self.exportar_csv()
                input("Pressione Enter para continuar...")
            elif opcao == '7':
                self.importar_csv()
                input("Pressione Enter para continuar...")
            elif opcao == '8':
                self.fazer_backup()
                input("Pressione Enter para continuar...")
            elif opcao == '9':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    sistema = GerenciadorLivraria()
    sistema.menu()