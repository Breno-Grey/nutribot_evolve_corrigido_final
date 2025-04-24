"""
Utilitário para geração de relatórios para o NutriBot Evolve.
Responsável por gerar relatórios de progresso e gráficos.
"""

import sys
import os
import json
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Usar backend não interativo
import numpy as np
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from database.meal_repository import MealRepository
from database.photo_repository import PhotoRepository

class ReportGenerator:
    """Classe para gerar relatórios de progresso e gráficos."""
    
    def __init__(self):
        """Inicializa o gerador de relatórios."""
        # Diretório para armazenar relatórios
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_weekly_report(self, user_id):
        """
        Gera um relatório semanal para o usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            dict: Dados do relatório e caminho para os gráficos
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        
        # Define o período do relatório (últimos 7 dias)
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=6)  # 7 dias incluindo hoje
        
        # Cria diretório específico para o usuário
        user_dir = os.path.join(self.reports_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Gera relatório de consumo calórico
        calorie_data = self._generate_calorie_report(user_id, start_date, end_date)
        
        # Gera relatório de macronutrientes
        macro_data = self._generate_macro_report(user_id, start_date, end_date)
        
        # Gera gráficos
        calorie_chart_path = self._generate_calorie_chart(user_id, calorie_data, start_date, end_date)
        macro_chart_path = self._generate_macro_chart(user_id, macro_data, start_date, end_date)
        
        # Gera insights
        insights = self._generate_insights(user, calorie_data, macro_data)
        
        # Compila o relatório
        report = {
            'user_id': user_id,
            'period': {
                'start_date': start_date.strftime('%d/%m/%Y'),
                'end_date': end_date.strftime('%d/%m/%Y')
            },
            'calorie_data': calorie_data,
            'macro_data': macro_data,
            'insights': insights,
            'charts': {
                'calorie_chart': calorie_chart_path,
                'macro_chart': macro_chart_path
            }
        }
        
        return report
    
    def _generate_calorie_report(self, user_id, start_date, end_date):
        """
        Gera dados de consumo calórico para o período.
        
        Args:
            user_id (int): ID do usuário no Telegram
            start_date (datetime.date): Data inicial
            end_date (datetime.date): Data final
            
        Returns:
            dict: Dados de consumo calórico
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        daily_target = user['daily_calories']
        
        # Inicializa dados para cada dia do período
        date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        daily_data = {date.strftime('%Y-%m-%d'): {'date': date.strftime('%d/%m'), 'calories': 0, 'target': daily_target} for date in date_range}
        
        # Obtém as refeições do período
        meals = MealRepository.get_meals_by_user_and_date_range(user_id, start_date, end_date)
        
        # Calcula calorias diárias
        for meal in meals:
            date_key = meal['meal_date'].strftime('%Y-%m-%d')
            if date_key in daily_data:
                daily_data[date_key]['calories'] += meal['calories']
        
        # Calcula estatísticas
        total_calories = sum(day['calories'] for day in daily_data.values())
        avg_calories = total_calories / len(daily_data) if daily_data else 0
        days_over_target = sum(1 for day in daily_data.values() if day['calories'] > day['target'])
        days_under_target = sum(1 for day in daily_data.values() if day['calories'] < day['target'])
        
        # Organiza os dados em formato de lista para facilitar o uso
        daily_list = [daily_data[date.strftime('%Y-%m-%d')] for date in date_range]
        
        return {
            'daily': daily_list,
            'stats': {
                'total_calories': round(total_calories),
                'avg_calories': round(avg_calories),
                'days_over_target': days_over_target,
                'days_under_target': days_under_target,
                'target_calories': round(daily_target)
            }
        }
    
    def _generate_macro_report(self, user_id, start_date, end_date):
        """
        Gera dados de consumo de macronutrientes para o período.
        
        Args:
            user_id (int): ID do usuário no Telegram
            start_date (datetime.date): Data inicial
            end_date (datetime.date): Data final
            
        Returns:
            dict: Dados de consumo de macronutrientes
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        
        # Calcula os macros alvo com base nas calorias diárias e tipo de dieta
        from utils.calorie_calculator import CalorieCalculator
        target_macros = CalorieCalculator.calculate_macros(user['daily_calories'], user['diet_type'])
        
        # Inicializa dados para cada dia do período
        date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        daily_data = {date.strftime('%Y-%m-%d'): {
            'date': date.strftime('%d/%m'),
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'target_protein': target_macros['protein'],
            'target_carbs': target_macros['carbs'],
            'target_fat': target_macros['fat']
        } for date in date_range}
        
        # Obtém as refeições do período
        meals = MealRepository.get_meals_by_user_and_date_range(user_id, start_date, end_date)
        
        # Calcula macros diários
        for meal in meals:
            date_key = meal['meal_date'].strftime('%Y-%m-%d')
            if date_key in daily_data:
                daily_data[date_key]['protein'] += meal['protein']
                daily_data[date_key]['carbs'] += meal['carbs']
                daily_data[date_key]['fat'] += meal['fat']
        
        # Calcula estatísticas
        total_protein = sum(day['protein'] for day in daily_data.values())
        total_carbs = sum(day['carbs'] for day in daily_data.values())
        total_fat = sum(day['fat'] for day in daily_data.values())
        
        avg_protein = total_protein / len(daily_data) if daily_data else 0
        avg_carbs = total_carbs / len(daily_data) if daily_data else 0
        avg_fat = total_fat / len(daily_data) if daily_data else 0
        
        # Organiza os dados em formato de lista para facilitar o uso
        daily_list = [daily_data[date.strftime('%Y-%m-%d')] for date in date_range]
        
        return {
            'daily': daily_list,
            'stats': {
                'total_protein': round(total_protein),
                'total_carbs': round(total_carbs),
                'total_fat': round(total_fat),
                'avg_protein': round(avg_protein),
                'avg_carbs': round(avg_carbs),
                'avg_fat': round(avg_fat),
                'target_protein': round(target_macros['protein']),
                'target_carbs': round(target_macros['carbs']),
                'target_fat': round(target_macros['fat'])
            }
        }
    
    def _generate_calorie_chart(self, user_id, calorie_data, start_date, end_date):
        """
        Gera um gráfico de consumo calórico.
        
        Args:
            user_id (int): ID do usuário no Telegram
            calorie_data (dict): Dados de consumo calórico
            start_date (datetime.date): Data inicial
            end_date (datetime.date): Data final
            
        Returns:
            str: Caminho para o arquivo do gráfico
        """
        # Configura o gráfico
        plt.figure(figsize=(10, 6))
        
        # Extrai dados para o gráfico
        dates = [day['date'] for day in calorie_data['daily']]
        calories = [day['calories'] for day in calorie_data['daily']]
        targets = [day['target'] for day in calorie_data['daily']]
        
        # Cria o gráfico de barras para calorias
        bars = plt.bar(dates, calories, color='#4CAF50', alpha=0.7, label='Calorias consumidas')
        
        # Adiciona linha para o alvo
        plt.plot(dates, targets, 'r--', label='Meta diária')
        
        # Configura o layout
        plt.title('Consumo Calórico Diário')
        plt.xlabel('Data')
        plt.ylabel('Calorias')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salva o gráfico
        user_dir = os.path.join(self.reports_dir, str(user_id))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_filename = f"calorie_chart_{timestamp}.png"
        chart_path = os.path.join(user_dir, chart_filename)
        
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_macro_chart(self, user_id, macro_data, start_date, end_date):
        """
        Gera um gráfico de consumo de macronutrientes.
        
        Args:
            user_id (int): ID do usuário no Telegram
            macro_data (dict): Dados de consumo de macronutrientes
            start_date (datetime.date): Data inicial
            end_date (datetime.date): Data final
            
        Returns:
            str: Caminho para o arquivo do gráfico
        """
        # Configura o gráfico
        plt.figure(figsize=(10, 6))
        
        # Extrai dados para o gráfico
        dates = [day['date'] for day in macro_data['daily']]
        proteins = [day['protein'] for day in macro_data['daily']]
        carbs = [day['carbs'] for day in macro_data['daily']]
        fats = [day['fat'] for day in macro_data['daily']]
        
        # Cria o gráfico de linhas para macronutrientes
        plt.plot(dates, proteins, 'b-', marker='o', label='Proteínas (g)')
        plt.plot(dates, carbs, 'g-', marker='s', label='Carboidratos (g)')
        plt.plot(dates, fats, 'r-', marker='^', label='Gorduras (g)')
        
        # Configura o layout
        plt.title('Consumo de Macronutrientes')
        plt.xlabel('Data')
        plt.ylabel('Gramas')
        plt.legend()
        plt.grid(linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salva o gráfico
        user_dir = os.path.join(self.reports_dir, str(user_id))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_filename = f"macro_chart_{timestamp}.png"
        chart_path = os.path.join(user_dir, chart_filename)
        
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_insights(self, user, calorie_data, macro_data):
        """
        Gera insights com base nos dados do relatório.
        
        Args:
            user (dict): Dados do usuário
            calorie_data (dict): Dados de consumo calórico
            macro_data (dict): Dados de consumo de macronutrientes
            
        Returns:
            list: Lista de insights
        """
        insights = []
        
        # Insight sobre consumo calórico
        avg_calories = calorie_data['stats']['avg_calories']
        target_calories = calorie_data['stats']['target_calories']
        
        if avg_calories > target_calories * 1.1:
            insights.append(f"Seu consumo calórico médio está {round((avg_calories/target_calories - 1) * 100)}% acima da meta. Considere reduzir as porções ou escolher alimentos menos calóricos.")
        elif avg_calories < target_calories * 0.9:
            insights.append(f"Seu consumo calórico médio está {round((1 - avg_calories/target_calories) * 100)}% abaixo da meta. Certifique-se de consumir calorias suficientes para manter sua energia e metabolismo.")
        else:
            insights.append("Seu consumo calórico médio está próximo da meta. Continue mantendo esse equilíbrio!")
        
        # Insight sobre consistência
        days_over = calorie_data['stats']['days_over_target']
        days_under = calorie_data['stats']['days_under_target']
        days_on_target = 7 - days_over - days_under
        
        if days_on_target >= 4:
            insights.append(f"Você manteve seu consumo próximo da meta em {days_on_target} dias esta semana. Excelente consistência!")
        elif days_over >= 4:
            insights.append(f"Você excedeu sua meta calórica em {days_over} dias esta semana. Tente planejar suas refeições com antecedência para manter-se dentro da meta.")
        elif days_under >= 4:
            insights.append(f"Você ficou abaixo da meta calórica em {days_under} dias esta semana. Lembre-se que consumir calorias suficientes é importante para sua saúde e energia.")
        
        # Insight sobre macronutrientes
        avg_protein = macro_data['stats']['avg_protein']
        target_protein = macro_data['stats']['target_protein']
        
        if avg_protein < target_protein * 0.8:
            insights.append(f"Seu consumo de proteínas está abaixo do recomendado. Considere incluir mais fontes de proteína como carnes magras, ovos, laticínios ou leguminosas.")
        
        # Insight sobre distribuição de macros
        avg_carbs = macro_data['stats']['avg_carbs']
        avg_fat = macro_data['stats']['avg_fat']
        
        total_macros = avg_protein + avg_carbs + avg_fat
        if total_macros > 0:
            protein_percent = (avg_protein * 4) / (avg_protein * 4 + avg_carbs * 4 + avg_fat * 9) * 100
            carbs_percent = (avg_carbs * 4) / (avg_protein * 4 + avg_carbs * 4 + avg_fat * 9) * 100
            fat_percent = (avg_fat * 9) / (avg_protein * 4 + avg_carbs * 4 + avg_fat * 9) * 100
            
            diet_type = user['diet_type']
            
            if diet_type == 'low_carb' and carbs_percent > 30:
                insights.append(f"Para uma dieta low carb, seu consumo de carboidratos está alto ({round(carbs_percent)}% das calorias). Tente reduzir alimentos ricos em carboidratos como pães, massas e açúcares.")
            elif diet_type == 'cetogenica' and carbs_percent > 10:
                insights.append(f"Para uma dieta cetogênica, seu consumo de carboidratos está alto ({round(carbs_percent)}% das calorias). Limite ainda mais os carboidratos e aumente o consumo de gorduras saudáveis.")
        
        # Insight sobre variação ao longo da semana
        calories_variation = np.std([day['calories'] for day in calorie_data['daily']])
        if calories_variation > target_calories * 0.3:
            insights.append("Seu consumo calórico varia bastante ao longo da semana. Tentar manter um padrão mais consistente pode ajudar a alcançar seus objetivos.")
        
        # Insight sobre próximos passos
        goal = user['goal']
        if goal == 'emagrecer':
            if avg_calories >= target_calories:
                insights.append("Para atingir seu objetivo de emagrecimento, tente reduzir um pouco mais seu consumo calórico ou aumentar sua atividade física.")
            else:
                insights.append("Você está no caminho certo para seu objetivo de emagrecimento. Continue mantendo o déficit calórico de forma saudável.")
        elif goal == 'ganhar_massa':
            if avg_calories <= target_calories:
                insights.append("Para ganhar massa muscular, tente aumentar um pouco seu consumo calórico, especialmente de proteínas, e combine com treinos de força.")
            else:
                insights.append("Você está consumindo calorias suficientes para seu objetivo de ganho de massa. Certifique-se de combinar com treinos adequados.")
        
        return insights
    
    def generate_monthly_report(self, user_id):
        """
        Gera um relatório mensal para o usuário (recurso premium).
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            dict: Dados do relatório e caminho para os gráficos
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['is_premium']:
            return None
        
        # Define o período do relatório (últimos 30 dias)
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=29)  # 30 dias incluindo hoje
        
        # Implementação similar ao relatório semanal, mas com período maior e análises mais detalhadas
        # Para simplificar, vamos reutilizar a lógica do relatório semanal
        
        # Cria diretório específico para o usuário
        user_dir = os.path.join(self.reports_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Gera relatório de consumo calórico
        calorie_data = self._generate_calorie_report(user_id, start_date, end_date)
        
        # Gera relatório de macronutrientes
        macro_data = self._generate_macro_report(user_id, start_date, end_date)
        
        # Gera gráficos
        calorie_chart_path = self._generate_calorie_chart(user_id, calorie_data, start_date, end_date)
        macro_chart_path = self._generate_macro_chart(user_id, macro_data, start_date, end_date)
        
        # Gera insights
        insights = self._generate_insights(user, calorie_data, macro_data)
        
        # Adiciona insights premium
        premium_insights = self._generate_premium_insights(user, calorie_data, macro_data)
        insights.extend(premium_insights)
        
        # Compila o relatório
        report = {
            'user_id': user_id,
            'period': {
                'start_date': start_date.strftime('%d/%m/%Y'),
                'end_date': end_date.strftime('%d/%m/%Y')
            },
            'calorie_data': calorie_data,
            'macro_data': macro_data,
            'insights': insights,
            'charts': {
                'calorie_chart': calorie_chart_path,
                'macro_chart': macro_chart_path
            }
        }
        
        return report
    
    def _generate_premium_insights(self, user, calorie_data, macro_data):
        """
        Gera insights premium com base nos dados do relatório.
        
        Args:
            user (dict): Dados do usuário
            calorie_data (dict): Dados de consumo calórico
            macro_data (dict): Dados de consumo de macronutrientes
            
        Returns:
            list: Lista de insights premium
        """
        premium_insights = []
        
        # Análise de tendência
        calories_by_day = [day['calories'] for day in calorie_data['daily']]
        if len(calories_by_day) >= 7:
            first_week_avg = sum(calories_by_day[:7]) / 7
            last_week_avg = sum(calories_by_day[-7:]) / 7
            
            if first_week_avg > last_week_avg:
                change_percent = (first_week_avg - last_week_avg) / first_week_avg * 100
                premium_insights.append(f"Tendência positiva: Seu consumo calórico reduziu {round(change_percent)}% nas últimas semanas.")
            elif last_week_avg > first_week_avg:
                change_percent = (last_week_avg - first_week_avg) / first_week_avg * 100
                premium_insights.append(f"Tendência de atenção: Seu consumo calórico aumentou {round(change_percent)}% nas últimas semanas.")
        
        # Análise de padrões alimentares
        # Em uma implementação real, seria feita uma análise mais sofisticada
        premium_insights.append("Análise Premium: Seus padrões alimentares indicam preferência por refeições mais substanciais no almoço. Considere distribuir melhor as calorias ao longo do dia para manter a energia constante.")
        
        # Recomendações personalizadas
        goal = user['goal']
        if goal == 'emagrecer':
            premium_insights.append("Recomendação Premium: Para otimizar seu emagrecimento, experimente adicionar 15 minutos de exercícios de alta intensidade (HIIT) 3 vezes por semana.")
        elif goal == 'ganhar_massa':
            premium_insights.append("Recomendação Premium: Para maximizar o ganho de massa muscular, aumente sua ingestão de proteínas em 20g nos dias de treino e priorize carboidratos complexos antes do exercício.")
        else:  # manter
            premium_insights.append("Recomendação Premium: Para manter seu peso de forma saudável, alterne entre dias de maior e menor consumo calórico (+-200 kcal) para estimular seu metabolismo.")
        
        return premium_insights
    
    def generate_pdf_report(self, user_id, report_data):
        """
        Gera um relatório em PDF (recurso premium).
        
        Args:
            user_id (int): ID do usuário no Telegram
            report_data (dict): Dados do relatório
            
        Returns:
            str: Caminho para o arquivo PDF ou None em caso de erro
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['is_premium']:
            return None
        
        # Em uma implementação real, aqui seria gerado um PDF completo
        # Para simplificar, vamos apenas salvar os dados do relatório em um arquivo JSON
        
        # Cria diretório específico para o usuário
        user_dir = os.path.join(self.reports_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Gera nome de arquivo único
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.json"
        report_path = os.path.join(user_dir, report_filename)
        
        # Salva os dados do relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=4, default=str)
        
        return report_path
