"""
Gerenciador de banco de dados para o NutriBot Evolve.
Responsável por criar e gerenciar a conexão com o banco de dados SQLite.
"""

import sqlite3
import os
import sys
import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path para importar config
sys.path.append(str(Path(__file__).parent.parent))
import config

class DatabaseManager:
    """Classe para gerenciar conexões e operações do banco de dados."""
    
    def __init__(self):
        """Inicializa o gerenciador de banco de dados."""
        # Obtém o caminho absoluto para o banco de dados
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.DATABASE_PATH)
        self.conn = None
        self.cursor = None
        
        # Garante que o diretório do banco de dados existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Inicializa o banco de dados
        self.initialize_database()
    
    def connect(self):
        """Estabelece conexão com o banco de dados."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
        self.cursor = self.conn.cursor()
        return self.conn
    
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def initialize_database(self):
        """Cria as tabelas do banco de dados se não existirem."""
        try:
            conn = self.connect()
            
            # Tabela de usuários
            conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                age INTEGER,
                weight REAL,
                height REAL,
                gender TEXT,
                activity_level TEXT,
                goal TEXT,
                diet_type TEXT,
                daily_calories REAL,
                is_premium BOOLEAN DEFAULT 0,
                onboarding_complete BOOLEAN DEFAULT 0,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            ''')
            
            # Tabela de refeições
            conn.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                meal_type TEXT,
                description TEXT,
                calories REAL,
                protein REAL,
                carbs REAL,
                fat REAL,
                meal_date DATE,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            
            # Tabela de fotos
            conn.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                photo_path TEXT,
                description TEXT,
                photo_date DATE,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            
            # Tabela de lembretes
            conn.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                reminder_type TEXT,
                reminder_time TIME,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            
            # Tabela de relatórios
            conn.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                report_type TEXT,
                start_date DATE,
                end_date DATE,
                report_data TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            
            # Tabela de estados de conversação (para gerenciar o fluxo de onboarding)
            conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_states (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                state TEXT,
                context TEXT,
                updated_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            ''')
            
            conn.commit()
            print("Banco de dados inicializado com sucesso.")
            
        except sqlite3.Error as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
        finally:
            self.close()
    
    def execute_query(self, query, params=None):
        """Executa uma consulta SQL e retorna os resultados."""
        try:
            conn = self.connect()
            if params:
                result = self.cursor.execute(query, params)
            else:
                result = self.cursor.execute(query)
            
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"Erro ao executar consulta: {e}")
            return None
        finally:
            self.close()
    
    def fetch_one(self, query, params=None):
        """Executa uma consulta e retorna um único resultado."""
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar resultado: {e}")
            return None
        finally:
            self.close()
    
    def fetch_all(self, query, params=None):
        """Executa uma consulta e retorna todos os resultados."""
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar resultados: {e}")
            return []
        finally:
            self.close()
    
    def insert(self, table, data):
        """Insere dados em uma tabela e retorna o ID do registro inserido."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            conn = self.connect()
            self.cursor.execute(query, values)
            conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")
            return None
        finally:
            self.close()
    
    def update(self, table, data, condition):
        """Atualiza registros em uma tabela."""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in condition.keys()])
        
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = tuple(list(data.values()) + list(condition.values()))
        
        try:
            conn = self.connect()
            self.cursor.execute(query, values)
            conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao atualizar dados: {e}")
            return 0
        finally:
            self.close()
    
    def delete(self, table, condition):
        """Remove registros de uma tabela."""
        where_clause = ' AND '.join([f"{key} = ?" for key in condition.keys()])
        values = tuple(condition.values())
        
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        try:
            conn = self.connect()
            self.cursor.execute(query, values)
            conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao remover dados: {e}")
            return 0
        finally:
            self.close()


# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()
