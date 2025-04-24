"""
Repositório de usuários para o NutriBot Evolve.
Responsável por operações de banco de dados relacionadas a usuários.
"""

import sys
import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import db_manager

class UserRepository:
    """Classe para gerenciar operações de banco de dados relacionadas a usuários."""
    
    @staticmethod
    def create_user(user_id, username=None, full_name=None):
        """
        Cria um novo usuário no banco de dados.
        
        Args:
            user_id (int): ID do usuário no Telegram
            username (str, optional): Nome de usuário no Telegram
            full_name (str, optional): Nome completo do usuário
            
        Returns:
            int: ID do registro inserido ou None em caso de erro
        """
        now = datetime.datetime.now()
        data = {
            'user_id': user_id,
            'username': username,
            'full_name': full_name,
            'created_at': now,
            'updated_at': now
        }
        
        return db_manager.insert('users', data)
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Busca um usuário pelo ID do Telegram.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            dict: Dados do usuário ou None se não encontrado
        """
        query = "SELECT * FROM users WHERE user_id = ?"
        return db_manager.fetch_one(query, (user_id,))
    
    @staticmethod
    def update_user(user_id, data):
        """
        Atualiza os dados de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            data (dict): Dicionário com os campos a serem atualizados
            
        Returns:
            int: Número de registros atualizados
        """
        # Adiciona timestamp de atualização
        data['updated_at'] = datetime.datetime.now()
        
        condition = {'user_id': user_id}
        return db_manager.update('users', data, condition)
    
    @staticmethod
    def update_onboarding_status(user_id, is_complete):
        """
        Atualiza o status de onboarding de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            is_complete (bool): Status de conclusão do onboarding
            
        Returns:
            int: Número de registros atualizados
        """
        data = {
            'onboarding_complete': 1 if is_complete else 0,
            'updated_at': datetime.datetime.now()
        }
        
        condition = {'user_id': user_id}
        return db_manager.update('users', data, condition)
    
    @staticmethod
    def set_user_premium_status(user_id, is_premium):
        """
        Define o status premium de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            is_premium (bool): Status premium
            
        Returns:
            int: Número de registros atualizados
        """
        data = {
            'is_premium': 1 if is_premium else 0,
            'updated_at': datetime.datetime.now()
        }
        
        condition = {'user_id': user_id}
        return db_manager.update('users', data, condition)
    
    @staticmethod
    def get_all_users():
        """
        Retorna todos os usuários cadastrados.
        
        Returns:
            list: Lista de usuários
        """
        query = "SELECT * FROM users"
        return db_manager.fetch_all(query)
    
    @staticmethod
    def get_premium_users():
        """
        Retorna todos os usuários premium.
        
        Returns:
            list: Lista de usuários premium
        """
        query = "SELECT * FROM users WHERE is_premium = 1"
        return db_manager.fetch_all(query)
    
    @staticmethod
    def get_users_with_complete_onboarding():
        """
        Retorna todos os usuários que completaram o onboarding.
        
        Returns:
            list: Lista de usuários com onboarding completo
        """
        query = "SELECT * FROM users WHERE onboarding_complete = 1"
        return db_manager.fetch_all(query)
    
    @staticmethod
    def delete_user(user_id):
        """
        Remove um usuário do banco de dados.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            int: Número de registros removidos
        """
        condition = {'user_id': user_id}
        return db_manager.delete('users', condition)
