"""
Utilitário para cálculo de calorias e macronutrientes para o NutriBot Evolve.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar config
sys.path.append(str(Path(__file__).parent.parent))
import config

class CalorieCalculator:
    """Classe para calcular necessidades calóricas e macronutrientes."""
    
    @staticmethod
    def calculate_bmr(weight, height, age, gender):
        """
        Calcula a Taxa Metabólica Basal (TMB) usando a fórmula de Harris-Benedict.
        
        Args:
            weight (float): Peso em kg
            height (float): Altura em cm
            age (int): Idade em anos
            gender (str): Gênero ('masculino' ou 'feminino')
            
        Returns:
            float: Taxa Metabólica Basal em calorias
        """
        if gender.lower() == 'masculino':
            bmr = (config.MALE_BMR_CONSTANT + 
                  (config.MALE_WEIGHT_MULTIPLIER * weight) + 
                  (config.MALE_HEIGHT_MULTIPLIER * height) - 
                  (config.MALE_AGE_MULTIPLIER * age))
        else:  # feminino
            bmr = (config.FEMALE_BMR_CONSTANT + 
                  (config.FEMALE_WEIGHT_MULTIPLIER * weight) + 
                  (config.FEMALE_HEIGHT_MULTIPLIER * height) - 
                  (config.FEMALE_AGE_MULTIPLIER * age))
        
        return round(bmr, 2)
    
    @staticmethod
    def calculate_tdee(bmr, activity_level):
        """
        Calcula o Gasto Energético Total Diário (TDEE).
        
        Args:
            bmr (float): Taxa Metabólica Basal
            activity_level (str): Nível de atividade física
            
        Returns:
            float: TDEE em calorias
        """
        multiplier = config.ACTIVITY_LEVELS.get(activity_level.lower(), 1.2)
        return round(bmr * multiplier, 2)
    
    @staticmethod
    def adjust_calories_for_goal(tdee, goal):
        """
        Ajusta as calorias diárias com base no objetivo.
        
        Args:
            tdee (float): Gasto Energético Total Diário
            goal (str): Objetivo ('emagrecer', 'manter' ou 'ganhar_massa')
            
        Returns:
            float: Calorias diárias ajustadas
        """
        adjustment = config.GOAL_ADJUSTMENTS.get(goal.lower(), 0)
        return round(tdee + adjustment, 2)
    
    @staticmethod
    def calculate_macros(calories, diet_type):
        """
        Calcula a distribuição de macronutrientes com base no tipo de dieta.
        
        Args:
            calories (float): Calorias diárias
            diet_type (str): Tipo de dieta
            
        Returns:
            dict: Dicionário com gramas de proteínas, carboidratos e gorduras
        """
        diet_info = config.DIET_TYPES.get(diet_type.lower(), config.DIET_TYPES['flexivel'])
        
        # Cálculo de macros em gramas
        # 1g de proteína = 4 calorias
        # 1g de carboidrato = 4 calorias
        # 1g de gordura = 9 calorias
        protein_calories = calories * (diet_info['protein_percent'] / 100)
        carbs_calories = calories * (diet_info['carbs_percent'] / 100)
        fat_calories = calories * (diet_info['fat_percent'] / 100)
        
        protein_grams = round(protein_calories / 4, 2)
        carbs_grams = round(carbs_calories / 4, 2)
        fat_grams = round(fat_calories / 9, 2)
        
        return {
            'protein': protein_grams,
            'carbs': carbs_grams,
            'fat': fat_grams
        }
    
    @staticmethod
    def calculate_daily_calories(weight, height, age, gender, activity_level, goal, diet_type):
        """
        Calcula as calorias diárias e macronutrientes com base nos dados do usuário.
        
        Args:
            weight (float): Peso em kg
            height (float): Altura em cm
            age (int): Idade em anos
            gender (str): Gênero ('masculino' ou 'feminino')
            activity_level (str): Nível de atividade física
            goal (str): Objetivo ('emagrecer', 'manter' ou 'ganhar_massa')
            diet_type (str): Tipo de dieta
            
        Returns:
            dict: Dicionário com calorias diárias e macronutrientes
        """
        bmr = CalorieCalculator.calculate_bmr(weight, height, age, gender)
        tdee = CalorieCalculator.calculate_tdee(bmr, activity_level)
        daily_calories = CalorieCalculator.adjust_calories_for_goal(tdee, goal)
        macros = CalorieCalculator.calculate_macros(daily_calories, diet_type)
        
        return {
            'bmr': bmr,
            'tdee': tdee,
            'daily_calories': daily_calories,
            'macros': macros
        }
