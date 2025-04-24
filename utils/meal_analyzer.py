"""
Analisador de refeições para o NutriBot Evolve.
Responsável por processar texto natural e identificar alimentos e valores nutricionais.
"""

import sys
import re
import json
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
import config

class MealAnalyzer:
    """Classe para analisar texto natural e identificar alimentos e valores nutricionais."""
    
    def __init__(self):
        """Inicializa o analisador de refeições."""
        # Carrega o banco de dados de alimentos
        self.food_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         'resources', 'food_database.json')
        self.food_database = self._load_food_database()
    
    def _load_food_database(self):
        """
        Carrega o banco de dados de alimentos.
        
        Returns:
            dict: Banco de dados de alimentos
        """
        # Verifica se o arquivo existe
        if not os.path.exists(self.food_db_path):
            # Cria um banco de dados básico se não existir
            self._create_basic_food_database()
        
        try:
            with open(self.food_db_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Erro ao carregar banco de dados de alimentos: {e}")
            return {}
    
    def _create_basic_food_database(self):
        """Cria um banco de dados básico de alimentos."""
        # Diretório de recursos
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        
        # Banco de dados básico de alimentos
        basic_food_db = {
            "arroz": {
                "calorias": 130,
                "proteinas": 2.7,
                "carboidratos": 28.2,
                "gorduras": 0.3,
                "porcao": 100,
                "unidade": "g"
            },
            "feijão": {
                "calorias": 77,
                "proteinas": 5.0,
                "carboidratos": 13.6,
                "gorduras": 0.5,
                "porcao": 100,
                "unidade": "g"
            },
            "frango": {
                "calorias": 165,
                "proteinas": 31.0,
                "carboidratos": 0.0,
                "gorduras": 3.6,
                "porcao": 100,
                "unidade": "g"
            },
            "carne": {
                "calorias": 250,
                "proteinas": 26.0,
                "carboidratos": 0.0,
                "gorduras": 17.0,
                "porcao": 100,
                "unidade": "g"
            },
            "peixe": {
                "calorias": 140,
                "proteinas": 20.0,
                "carboidratos": 0.0,
                "gorduras": 6.0,
                "porcao": 100,
                "unidade": "g"
            },
            "ovo": {
                "calorias": 155,
                "proteinas": 13.0,
                "carboidratos": 1.1,
                "gorduras": 11.0,
                "porcao": 100,
                "unidade": "g"
            },
            "leite": {
                "calorias": 42,
                "proteinas": 3.4,
                "carboidratos": 5.0,
                "gorduras": 1.0,
                "porcao": 100,
                "unidade": "ml"
            },
            "pão": {
                "calorias": 265,
                "proteinas": 9.0,
                "carboidratos": 49.0,
                "gorduras": 3.2,
                "porcao": 100,
                "unidade": "g"
            },
            "maçã": {
                "calorias": 52,
                "proteinas": 0.3,
                "carboidratos": 14.0,
                "gorduras": 0.2,
                "porcao": 100,
                "unidade": "g"
            },
            "banana": {
                "calorias": 89,
                "proteinas": 1.1,
                "carboidratos": 22.8,
                "gorduras": 0.3,
                "porcao": 100,
                "unidade": "g"
            },
            "laranja": {
                "calorias": 47,
                "proteinas": 0.9,
                "carboidratos": 11.8,
                "gorduras": 0.1,
                "porcao": 100,
                "unidade": "g"
            },
            "alface": {
                "calorias": 15,
                "proteinas": 1.4,
                "carboidratos": 2.9,
                "gorduras": 0.2,
                "porcao": 100,
                "unidade": "g"
            },
            "tomate": {
                "calorias": 18,
                "proteinas": 0.9,
                "carboidratos": 3.9,
                "gorduras": 0.2,
                "porcao": 100,
                "unidade": "g"
            },
            "cenoura": {
                "calorias": 41,
                "proteinas": 0.9,
                "carboidratos": 9.6,
                "gorduras": 0.2,
                "porcao": 100,
                "unidade": "g"
            },
            "batata": {
                "calorias": 77,
                "proteinas": 2.0,
                "carboidratos": 17.0,
                "gorduras": 0.1,
                "porcao": 100,
                "unidade": "g"
            },
            "azeite": {
                "calorias": 884,
                "proteinas": 0.0,
                "carboidratos": 0.0,
                "gorduras": 100.0,
                "porcao": 100,
                "unidade": "ml"
            },
            "manteiga": {
                "calorias": 717,
                "proteinas": 0.9,
                "carboidratos": 0.1,
                "gorduras": 81.0,
                "porcao": 100,
                "unidade": "g"
            },
            "queijo": {
                "calorias": 350,
                "proteinas": 25.0,
                "carboidratos": 2.0,
                "gorduras": 27.0,
                "porcao": 100,
                "unidade": "g"
            },
            "iogurte": {
                "calorias": 59,
                "proteinas": 3.5,
                "carboidratos": 4.7,
                "gorduras": 3.3,
                "porcao": 100,
                "unidade": "g"
            },
            "chocolate": {
                "calorias": 546,
                "proteinas": 4.9,
                "carboidratos": 61.0,
                "gorduras": 31.0,
                "porcao": 100,
                "unidade": "g"
            },
            "refrigerante": {
                "calorias": 42,
                "proteinas": 0.0,
                "carboidratos": 10.6,
                "gorduras": 0.0,
                "porcao": 100,
                "unidade": "ml"
            },
            "suco": {
                "calorias": 45,
                "proteinas": 0.5,
                "carboidratos": 10.0,
                "gorduras": 0.1,
                "porcao": 100,
                "unidade": "ml"
            },
            "café": {
                "calorias": 2,
                "proteinas": 0.1,
                "carboidratos": 0.0,
                "gorduras": 0.0,
                "porcao": 100,
                "unidade": "ml"
            },
            "açúcar": {
                "calorias": 387,
                "proteinas": 0.0,
                "carboidratos": 100.0,
                "gorduras": 0.0,
                "porcao": 100,
                "unidade": "g"
            },
            "sal": {
                "calorias": 0,
                "proteinas": 0.0,
                "carboidratos": 0.0,
                "gorduras": 0.0,
                "porcao": 100,
                "unidade": "g"
            },
            "salada": {
                "calorias": 20,
                "proteinas": 1.5,
                "carboidratos": 3.0,
                "gorduras": 0.3,
                "porcao": 100,
                "unidade": "g"
            }
        }
        
        # Salva o banco de dados básico
        with open(self.food_db_path, 'w', encoding='utf-8') as file:
            json.dump(basic_food_db, file, ensure_ascii=False, indent=4)
    
    def analyze_meal_text(self, text):
        """
        Analisa o texto da refeição e identifica alimentos e quantidades.
        
        Args:
            text (str): Texto descrevendo a refeição
            
        Returns:
            dict: Informações sobre a refeição (alimentos, calorias, macronutrientes)
        """
        # Normaliza o texto
        text = text.lower()
        
        # Identifica o tipo de refeição
        meal_type = self._identify_meal_type(text)
        
        # Identifica alimentos e quantidades
        food_items = self._identify_food_items(text)
        
        # Calcula valores nutricionais
        nutrition = self._calculate_nutrition(food_items)
        
        return {
            'meal_type': meal_type,
            'food_items': food_items,
            'nutrition': nutrition,
            'description': text
        }
    
    def _identify_meal_type(self, text):
        """
        Identifica o tipo de refeição com base no texto.
        
        Args:
            text (str): Texto descrevendo a refeição
            
        Returns:
            str: Tipo de refeição
        """
        # Palavras-chave para identificar tipos de refeição
        meal_types = {
            'café_da_manha': ['café da manhã', 'café', 'desjejum', 'manhã'],
            'lanche_manha': ['lanche da manhã', 'lanche manhã', 'colação'],
            'almoco': ['almoço', 'almocei', 'almoçar'],
            'lanche_tarde': ['lanche da tarde', 'lanche tarde', 'merenda'],
            'jantar': ['jantar', 'jantei', 'jantar'],
            'ceia': ['ceia', 'antes de dormir', 'noite']
        }
        
        # Verifica se alguma palavra-chave está presente no texto
        for meal_type, keywords in meal_types.items():
            for keyword in keywords:
                if keyword in text:
                    return meal_type
        
        # Se não identificar, tenta inferir pelo horário (implementação futura)
        # Por enquanto, retorna um valor padrão
        return 'refeicao'
    
    def _identify_food_items(self, text):
        """
        Identifica alimentos e quantidades no texto.
        
        Args:
            text (str): Texto descrevendo a refeição
            
        Returns:
            list: Lista de itens alimentares identificados
        """
        food_items = []
        
        # Procura por alimentos do banco de dados no texto
        for food_name, food_info in self.food_database.items():
            # Padrão para encontrar o alimento e possíveis quantidades
            # Exemplo: "100g de arroz" ou "arroz (100g)" ou "2 ovos"
            pattern = r'(\d+(?:[.,]\d+)?\s*(?:g|ml|unidades?|colheres?|xícaras?|fatias?|pedaços?))?\s*(?:de\s+)?(' + food_name + r')|\b(' + food_name + r')\s*(?:\((\d+(?:[.,]\d+)?\s*(?:g|ml|unidades?|colheres?|xícaras?|fatias?|pedaços?))\))?'
            
            matches = re.finditer(pattern, text)
            for match in matches:
                # Extrai a quantidade e a unidade, se presentes
                quantity_str = match.group(1) or match.group(4) or ""
                
                # Determina o nome do alimento (pode estar no grupo 2 ou 3)
                food = match.group(2) or match.group(3)
                
                # Processa a quantidade
                quantity, unit = self._parse_quantity(quantity_str, food_info['unidade'])
                
                # Calcula a proporção em relação à porção padrão
                proportion = quantity / food_info['porcao'] if food_info['porcao'] > 0 else 1
                
                # Adiciona o item à lista
                food_items.append({
                    'name': food,
                    'quantity': quantity,
                    'unit': unit,
                    'calories': food_info['calorias'] * proportion,
                    'protein': food_info['proteinas'] * proportion,
                    'carbs': food_info['carboidratos'] * proportion,
                    'fat': food_info['gorduras'] * proportion
                })
        
        return food_items
    
    def _parse_quantity(self, quantity_str, default_unit):
        """
        Analisa a string de quantidade e extrai o valor numérico e a unidade.
        
        Args:
            quantity_str (str): String de quantidade
            default_unit (str): Unidade padrão para o alimento
            
        Returns:
            tuple: (quantidade, unidade)
        """
        if not quantity_str:
            # Se não houver quantidade especificada, assume a porção padrão
            return 100, default_unit
        
        # Extrai o número e a unidade
        match = re.match(r'(\d+(?:[.,]\d+)?)\s*([a-zA-Z]+)', quantity_str)
        if match:
            value = float(match.group(1).replace(',', '.'))
            unit = match.group(2).lower()
            
            # Normaliza unidades
            if unit in ['g', 'grama', 'gramas']:
                unit = 'g'
            elif unit in ['ml', 'mililitro', 'mililitros']:
                unit = 'ml'
            elif unit in ['unidade', 'unidades', 'un']:
                unit = 'unidade'
                # Para unidades, assume um peso médio
                if default_unit == 'g':
                    value *= 50  # Peso médio estimado por unidade
                    unit = 'g'
            elif unit in ['colher', 'colheres']:
                unit = 'colher'
                # Para colheres, assume um peso médio
                if default_unit == 'g':
                    value *= 15  # Peso médio estimado por colher
                    unit = 'g'
                elif default_unit == 'ml':
                    value *= 15  # Volume médio estimado por colher
                    unit = 'ml'
            elif unit in ['xícara', 'xícaras', 'xicara', 'xicaras']:
                unit = 'xícara'
                # Para xícaras, assume um peso/volume médio
                if default_unit == 'g':
                    value *= 240  # Peso médio estimado por xícara
                    unit = 'g'
                elif default_unit == 'ml':
                    value *= 240  # Volume médio estimado por xícara
                    unit = 'ml'
            
            return value, unit
        
        # Se não conseguir extrair, assume a porção padrão
        return 100, default_unit
    
    def _calculate_nutrition(self, food_items):
        """
        Calcula os valores nutricionais totais da refeição.
        
        Args:
            food_items (list): Lista de itens alimentares
            
        Returns:
            dict: Valores nutricionais totais
        """
        total_calories = sum(item['calories'] for item in food_items)
        total_protein = sum(item['protein'] for item in food_items)
        total_carbs = sum(item['carbs'] for item in food_items)
        total_fat = sum(item['fat'] for item in food_items)
        
        return {
            'calories': round(total_calories, 2),
            'protein': round(total_protein, 2),
            'carbs': round(total_carbs, 2),
            'fat': round(total_fat, 2)
        }
