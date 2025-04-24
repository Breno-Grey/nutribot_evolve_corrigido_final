"""
Repositório de refeições para o NutriBot Evolve.
Responsável por operações de banco de dados relacionadas a refeições.
"""

import sys
import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import db_manager

class MealRepository:
    """Classe para gerenciar operações de banco de dados relacionadas a refeições."""
    
    @staticmethod
    def add_meal(user_id, meal_type, description, calories, protein, carbs, fat, meal_date=None):
        """
        Adiciona uma nova refeição ao banco de dados.
        
        Args:
            user_id (int): ID do usuário no Telegram
            meal_type (str): Tipo de refeição (café da manhã, almoço, etc.)
            description (str): Descrição da refeição
            calories (float): Calorias totais
            protein (float): Proteínas em gramas
            carbs (float): Carboidratos em gramas
            fat (float): Gorduras em gramas
            meal_date (datetime.date, optional): Data da refeição (padrão: data atual)
            
        Returns:
            int: ID do registro inserido ou None em caso de erro
        """
        now = datetime.datetime.now()
        if meal_date is None:
            meal_date = now.date()
        
        data = {
            'user_id': user_id,
            'meal_type': meal_type,
            'description': description,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'meal_date': meal_date,
            'created_at': now
        }
        
        return db_manager.insert('meals', data)
    
    @staticmethod
    def get_meals_by_user_and_date(user_id, date=None):
        """
        Busca refeições de um usuário em uma data específica.
        
        Args:
            user_id (int): ID do usuário no Telegram
            date (datetime.date, optional): Data das refeições (padrão: data atual)
            
        Returns:
            list: Lista de refeições
        """
        if date is None:
            date = datetime.datetime.now().date()
        
        query = "SELECT * FROM meals WHERE user_id = ? AND meal_date = ? ORDER BY created_at"
        return db_manager.fetch_all(query, (user_id, date))
    
    @staticmethod
    def get_meals_by_user_and_date_range(user_id, start_date, end_date):
        """
        Busca refeições de um usuário em um intervalo de datas.
        
        Args:
            user_id (int): ID do usuário no Telegram
            start_date (datetime.date): Data inicial
            end_date (datetime.date): Data final
            
        Returns:
            list: Lista de refeições
        """
        query = """
        SELECT * FROM meals 
        WHERE user_id = ? AND meal_date BETWEEN ? AND ? 
        ORDER BY meal_date, created_at
        """
        return db_manager.fetch_all(query, (user_id, start_date, end_date))
    
    @staticmethod
    def get_daily_totals(user_id, date=None):
        """
        Calcula os totais diários de calorias e macronutrientes.
        
        Args:
            user_id (int): ID do usuário no Telegram
            date (datetime.date, optional): Data (padrão: data atual)
            
        Returns:
            dict: Totais diários
        """
        if date is None:
            date = datetime.datetime.now().date()
        
        query = """
        SELECT 
            SUM(calories) as total_calories,
            SUM(protein) as total_protein,
            SUM(carbs) as total_carbs,
            SUM(fat) as total_fat
        FROM meals 
        WHERE user_id = ? AND meal_date = ?
        """
        
        result = db_manager.fetch_one(query, (user_id, date))
        
        if result:
            return {
                'calories': result['total_calories'] or 0,
                'protein': result['total_protein'] or 0,
                'carbs': result['total_carbs'] or 0,
                'fat': result['total_fat'] or 0
            }
        else:
            return {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }
    
    @staticmethod
    def update_meal(meal_id, data):
        """
        Atualiza os dados de uma refeição.
        
        Args:
            meal_id (int): ID da refeição
            data (dict): Dicionário com os campos a serem atualizados
            
        Returns:
            int: Número de registros atualizados
        """
        condition = {'id': meal_id}
        return db_manager.update('meals', data, condition)
    
    @staticmethod
    def delete_meal(meal_id):
        """
        Remove uma refeição do banco de dados.
        
        Args:
            meal_id (int): ID da refeição
            
        Returns:
            int: Número de registros removidos
        """
        condition = {'id': meal_id}
        return db_manager.delete('meals', condition)
    
    @staticmethod
    def get_meal_types_for_user(user_id, date=None):
        """
        Retorna os tipos de refeições registradas por um usuário em uma data.
        
        Args:
            user_id (int): ID do usuário no Telegram
            date (datetime.date, optional): Data (padrão: data atual)
            
        Returns:
            list: Lista de tipos de refeições
        """
        if date is None:
            date = datetime.datetime.now().date()
        
        query = """
        SELECT DISTINCT meal_type 
        FROM meals 
        WHERE user_id = ? AND meal_date = ?
        """
        
        results = db_manager.fetch_all(query, (user_id, date))
        return [result['meal_type'] for result in results]
