"""
Script de teste para o NutriBot Evolve.
Este script testa as principais funcionalidades do bot.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent))

from database.db_manager import db_manager
from database.user_repository import UserRepository
from database.meal_repository import MealRepository
from database.photo_repository import PhotoRepository
from utils.calorie_calculator import CalorieCalculator
from utils.conversation_manager import ConversationManager
from utils.meal_analyzer import MealAnalyzer
from utils.meal_suggester import MealSuggester
from utils.photo_analyzer import PhotoAnalyzer
from utils.report_generator import ReportGenerator

def test_database_connection():
    """Testa a conexão com o banco de dados."""
    print("Testando conexão com o banco de dados...")
    try:
        db_manager.initialize_database()
        print("✅ Conexão com o banco de dados estabelecida com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False

def test_user_repository():
    """Testa as operações do repositório de usuários."""
    print("\nTestando repositório de usuários...")
    try:
        # Cria um usuário de teste
        user_id = 123456789
        username = "test_user"
        full_name = "Test User"
        
        # Remove o usuário se já existir
        user = UserRepository.get_user_by_id(user_id)
        if user:
            UserRepository.delete_user(user_id)
        
        # Cria o usuário
        UserRepository.create_user(user_id, username, full_name)
        print("✅ Usuário criado com sucesso.")
        
        # Busca o usuário
        user = UserRepository.get_user_by_id(user_id)
        if user and user['user_id'] == user_id:
            print("✅ Usuário encontrado com sucesso.")
        else:
            print("❌ Erro ao buscar usuário.")
            return False
        
        # Atualiza o usuário
        data = {
            'age': 30,
            'weight': 70.5,
            'height': 175,
            'gender': 'masculino',
            'activity_level': 'moderado',
            'goal': 'emagrecer',
            'diet_type': 'low_carb',
            'daily_calories': 2000,
            'onboarding_complete': 1
        }
        UserRepository.update_user(user_id, data)
        print("✅ Usuário atualizado com sucesso.")
        
        # Verifica a atualização
        user = UserRepository.get_user_by_id(user_id)
        if user and user['daily_calories'] == 2000:
            print("✅ Atualização verificada com sucesso.")
        else:
            print("❌ Erro ao verificar atualização.")
            return False
        
        # Define status premium
        UserRepository.set_user_premium_status(user_id, True)
        user = UserRepository.get_user_by_id(user_id)
        if user and user['is_premium'] == 1:
            print("✅ Status premium definido com sucesso.")
        else:
            print("❌ Erro ao definir status premium.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do repositório de usuários: {e}")
        return False

def test_meal_repository():
    """Testa as operações do repositório de refeições."""
    print("\nTestando repositório de refeições...")
    try:
        # Usa o usuário de teste
        user_id = 123456789
        
        # Adiciona uma refeição
        meal_id = MealRepository.add_meal(
            user_id=user_id,
            meal_type="almoco",
            description="Arroz, feijão, frango e salada",
            calories=500,
            protein=30,
            carbs=60,
            fat=10
        )
        
        if meal_id:
            print("✅ Refeição adicionada com sucesso.")
        else:
            print("❌ Erro ao adicionar refeição.")
            return False
        
        # Busca refeições do usuário
        meals = MealRepository.get_meals_by_user_and_date(user_id)
        if meals and len(meals) > 0:
            print("✅ Refeições encontradas com sucesso.")
        else:
            print("❌ Erro ao buscar refeições.")
            return False
        
        # Calcula totais diários
        totals = MealRepository.get_daily_totals(user_id)
        if totals and totals['calories'] > 0:
            print("✅ Totais diários calculados com sucesso.")
        else:
            print("❌ Erro ao calcular totais diários.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do repositório de refeições: {e}")
        return False

def test_calorie_calculator():
    """Testa o calculador de calorias."""
    print("\nTestando calculador de calorias...")
    try:
        # Calcula TMB
        bmr = CalorieCalculator.calculate_bmr(70, 175, 30, 'masculino')
        print(f"TMB calculada: {bmr} kcal")
        
        # Calcula TDEE
        tdee = CalorieCalculator.calculate_tdee(bmr, 'moderado')
        print(f"TDEE calculado: {tdee} kcal")
        
        # Ajusta calorias para objetivo
        daily_calories = CalorieCalculator.adjust_calories_for_goal(tdee, 'emagrecer')
        print(f"Calorias diárias ajustadas: {daily_calories} kcal")
        
        # Calcula macros
        macros = CalorieCalculator.calculate_macros(daily_calories, 'low_carb')
        print(f"Macros calculados: Proteínas: {macros['protein']}g, Carboidratos: {macros['carbs']}g, Gorduras: {macros['fat']}g")
        
        # Calcula calorias diárias completo
        result = CalorieCalculator.calculate_daily_calories(70, 175, 30, 'masculino', 'moderado', 'emagrecer', 'low_carb')
        if result and 'daily_calories' in result:
            print("✅ Cálculo de calorias realizado com sucesso.")
        else:
            print("❌ Erro no cálculo de calorias.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do calculador de calorias: {e}")
        return False

def test_meal_analyzer():
    """Testa o analisador de refeições."""
    print("\nTestando analisador de refeições...")
    try:
        analyzer = MealAnalyzer()
        
        # Analisa texto de refeição
        meal_text = "Comi 100g de arroz, 150g de frango grelhado e uma salada de alface e tomate"
        result = analyzer.analyze_meal_text(meal_text)
        
        if result and 'nutrition' in result:
            print("✅ Análise de refeição realizada com sucesso.")
            print(f"Calorias: {result['nutrition']['calories']} kcal")
            print(f"Proteínas: {result['nutrition']['protein']}g")
            print(f"Carboidratos: {result['nutrition']['carbs']}g")
            print(f"Gorduras: {result['nutrition']['fat']}g")
        else:
            print("❌ Erro na análise de refeição.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do analisador de refeições: {e}")
        return False

def test_meal_suggester():
    """Testa o sugestor de refeições."""
    print("\nTestando sugestor de refeições...")
    try:
        suggester = MealSuggester()
        
        # Obtém sugestão de refeição
        suggestion = suggester.get_meal_suggestion('low_carb', 'almoco')
        
        if suggestion and 'nome' in suggestion:
            print("✅ Sugestão de refeição obtida com sucesso.")
            print(f"Nome: {suggestion['nome']}")
            print(f"Descrição: {suggestion['descricao']}")
            print(f"Calorias: {suggestion['calorias']} kcal")
        else:
            print("❌ Erro ao obter sugestão de refeição.")
            return False
        
        # Obtém mensagem motivacional
        message = suggester.get_motivation_message('emagrecer')
        
        if message:
            print("✅ Mensagem motivacional obtida com sucesso.")
            print(f"Mensagem: {message}")
        else:
            print("❌ Erro ao obter mensagem motivacional.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do sugestor de refeições: {e}")
        return False

def test_conversation_manager():
    """Testa o gerenciador de conversação."""
    print("\nTestando gerenciador de conversação...")
    try:
        # Usa o usuário de teste
        user_id = 123456789
        
        # Define um estado
        state = ConversationManager.STATES['WAITING_NAME']
        context = {'test_key': 'test_value'}
        
        result = ConversationManager.set_state(user_id, state, context)
        if result:
            print("✅ Estado definido com sucesso.")
        else:
            print("❌ Erro ao definir estado.")
            return False
        
        # Obtém o estado
        conversation = ConversationManager.get_state(user_id)
        if conversation and conversation['state'] == state:
            print("✅ Estado obtido com sucesso.")
        else:
            print("❌ Erro ao obter estado.")
            return False
        
        # Atualiza o contexto
        new_context = {'new_key': 'new_value'}
        result = ConversationManager.update_context(user_id, new_context)
        if result:
            print("✅ Contexto atualizado com sucesso.")
        else:
            print("❌ Erro ao atualizar contexto.")
            return False
        
        # Verifica a atualização
        conversation = ConversationManager.get_state(user_id)
        if conversation and 'new_key' in conversation['context']:
            print("✅ Atualização de contexto verificada com sucesso.")
        else:
            print("❌ Erro ao verificar atualização de contexto.")
            return False
        
        # Limpa o estado
        result = ConversationManager.clear_state(user_id)
        if result:
            print("✅ Estado limpo com sucesso.")
        else:
            print("❌ Erro ao limpar estado.")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do gerenciador de conversação: {e}")
        return False

def test_photo_analyzer():
    """Testa o analisador de fotos."""
    print("\nTestando analisador de fotos (simulado)...")
    try:
        analyzer = PhotoAnalyzer()
        
        # Testa geração de dicas
        tips = analyzer.generate_photo_tips()
        if tips and len(tips) > 0:
            print("✅ Dicas de foto geradas com sucesso.")
        else:
            print("❌ Erro ao gerar dicas de foto.")
            return False
        
        # Nota: Testes reais de análise de fotos requerem arquivos de imagem
        # Aqui estamos apenas verificando se a classe foi inicializada corretamente
        
        print("✅ Analisador de fotos inicializado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do analisador de fotos: {e}")
        return False

def test_report_generator():
    """Testa o gerador de relatórios."""
    print("\nTestando gerador de relatórios (simulado)...")
    try:
        generator = ReportGenerator()
        
        # Nota: Testes reais de geração de relatórios requerem dados no banco
        # Aqui estamos apenas verificando se a classe foi inicializada corretamente
        
        print("✅ Gerador de relatórios inicializado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro nos testes do gerador de relatórios: {e}")
        return False

def run_all_tests():
    """Executa todos os testes."""
    print("=== INICIANDO TESTES DO NUTRIBOT EVOLVE ===\n")
    
    # Lista de testes
    tests = [
        test_database_connection,
        test_user_repository,
        test_meal_repository,
        test_calorie_calculator,
        test_meal_analyzer,
        test_meal_suggester,
        test_conversation_manager,
        test_photo_analyzer,
        test_report_generator
    ]
    
    # Executa os testes
    results = []
    for test in tests:
        results.append(test())
    
    # Exibe resultado final
    print("\n=== RESULTADO DOS TESTES ===")
    total_tests = len(tests)
    passed_tests = sum(results)
    
    print(f"Total de testes: {total_tests}")
    print(f"Testes bem-sucedidos: {passed_tests}")
    print(f"Testes com falha: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("\n✅ TODOS OS TESTES FORAM BEM-SUCEDIDOS!")
    else:
        print(f"\n❌ {total_tests - passed_tests} TESTES FALHARAM!")

if __name__ == "__main__":
    run_all_tests()
