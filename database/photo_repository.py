"""
Repositório de fotos para o NutriBot Evolve.
Responsável por operações de banco de dados relacionadas a fotos corporais.
"""

import sys
import datetime
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import db_manager

class PhotoRepository:
    """Classe para gerenciar operações de banco de dados relacionadas a fotos corporais."""
    
    @staticmethod
    def add_photo(user_id, photo_path, description=None, photo_date=None):
        """
        Adiciona uma nova foto ao banco de dados.
        
        Args:
            user_id (int): ID do usuário no Telegram
            photo_path (str): Caminho para o arquivo da foto
            description (str, optional): Descrição ou comentários
            photo_date (datetime.date, optional): Data da foto (padrão: data atual)
            
        Returns:
            int: ID do registro inserido ou None em caso de erro
        """
        now = datetime.datetime.now()
        if photo_date is None:
            photo_date = now.date()
        
        data = {
            'user_id': user_id,
            'photo_path': photo_path,
            'description': description,
            'photo_date': photo_date,
            'created_at': now
        }
        
        return db_manager.insert('photos', data)
    
    @staticmethod
    def get_photos_by_user(user_id, limit=10):
        """
        Busca fotos de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            limit (int, optional): Limite de fotos a retornar
            
        Returns:
            list: Lista de fotos
        """
        query = "SELECT * FROM photos WHERE user_id = ? ORDER BY photo_date DESC, created_at DESC LIMIT ?"
        return db_manager.fetch_all(query, (user_id, limit))
    
    @staticmethod
    def get_latest_photo(user_id):
        """
        Busca a foto mais recente de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            dict: Dados da foto ou None se não encontrada
        """
        query = "SELECT * FROM photos WHERE user_id = ? ORDER BY photo_date DESC, created_at DESC LIMIT 1"
        return db_manager.fetch_one(query, (user_id,))
    
    @staticmethod
    def get_photo_by_id(photo_id):
        """
        Busca uma foto pelo ID.
        
        Args:
            photo_id (int): ID da foto
            
        Returns:
            dict: Dados da foto ou None se não encontrada
        """
        query = "SELECT * FROM photos WHERE id = ?"
        return db_manager.fetch_one(query, (photo_id,))
    
    @staticmethod
    def update_photo(photo_id, data):
        """
        Atualiza os dados de uma foto.
        
        Args:
            photo_id (int): ID da foto
            data (dict): Dicionário com os campos a serem atualizados
            
        Returns:
            int: Número de registros atualizados
        """
        condition = {'id': photo_id}
        return db_manager.update('photos', data, condition)
    
    @staticmethod
    def delete_photo(photo_id):
        """
        Remove uma foto do banco de dados.
        
        Args:
            photo_id (int): ID da foto
            
        Returns:
            int: Número de registros removidos
        """
        # Primeiro, obtém o caminho do arquivo
        photo = PhotoRepository.get_photo_by_id(photo_id)
        if photo and photo['photo_path']:
            # Tenta remover o arquivo físico
            try:
                if os.path.exists(photo['photo_path']):
                    os.remove(photo['photo_path'])
            except Exception as e:
                print(f"Erro ao remover arquivo de foto: {e}")
        
        # Remove o registro do banco de dados
        condition = {'id': photo_id}
        return db_manager.delete('photos', condition)
    
    @staticmethod
    def get_photo_count_by_user(user_id):
        """
        Conta o número de fotos de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            int: Número de fotos
        """
        query = "SELECT COUNT(*) as count FROM photos WHERE user_id = ?"
        result = db_manager.fetch_one(query, (user_id,))
        return result['count'] if result else 0
