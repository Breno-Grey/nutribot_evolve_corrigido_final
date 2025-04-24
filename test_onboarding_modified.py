"""
Script de teste modificado para o fluxo de onboarding do NutriBot Evolve.
Esta versão usa o módulo photo_analyzer_test para evitar problemas de dependência.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(os.getcwd())

# Substitui o módulo photo_analyzer pelo photo_analyzer_test
sys.modules['utils.photo_analyzer'] = __import__('utils.photo_analyzer_test', fromlist=['PhotoAnalyzer'])

from handlers.onboarding_handler import OnboardingHandler
from utils.conversation_manager import ConversationManager
from database.db_manager import db_manager
from database.user_repository import UserRepository

class MockUpdate:
    """Classe para simular um objeto Update do Telegram."""
    
    def __init__(self, user_id, username, full_name, text=None):
        self.effective_user = MockUser(user_id, username, full_name)
        self.message = MockMessage(text) if text else None

class MockUser:
    """Classe para simular um objeto User do Telegram."""
    
    def __init__(self, user_id, username, full_name):
        self.id = user_id
        self.username = username
        self.full_name = full_name

class MockMessage:
    """Classe para simular um objeto Message do Telegram."""
    
    def __init__(self, text):
        self.text = text

class MockContext:
    """Classe para simular um objeto Context do Telegram."""
    
    def __init__(self):
        pass

def print_header(message):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def reset_database():
    """Limpa os dados de teste do banco de dados."""
    print("Limpando dados de teste do banco de dados...")
    
    # Conecta diretamente ao banco de dados para garantir limpeza completa
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database/nutribot.db")
    
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Remove o usuário de teste
        cursor.execute("DELETE FROM users WHERE user_id = ?", (TEST_USER_ID,))
        
        # Remove o estado de conversação do usuário de teste
        cursor.execute("DELETE FROM conversation_states WHERE user_id = ?", (TEST_USER_ID,))
        
        conn.commit()
        conn.close()
        
        print("Dados de teste removidos com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao limpar dados de teste: {e}")
        return False

def test_start_command():
    """Testa o comando /start."""
    print_header("Testando comando /start")
    
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME)
    context = MockContext()
    
    response = OnboardingHandler.handle_start(update, context)
    print(f"Resposta: {response[:100]}...")
    
    # Verifica se o usuário foi criado
    user = UserRepository.get_user_by_id(TEST_USER_ID)
    print(f"Usuário criado: {user is not None}")
    
    return user is not None

def test_iniciar_command():
    """Testa o comando /iniciar."""
    print_header("Testando comando /iniciar")
    
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME)
    context = MockContext()
    
    response = OnboardingHandler.handle_iniciar(update, context)
    print(f"Resposta: {response[:100]}...")
    
    # Verifica se o estado foi definido corretamente
    conversation = ConversationManager.get_state(TEST_USER_ID)
    print(f"Estado atual: {conversation['state']}")
    
    return conversation['state'] == ConversationManager.STATES['WAITING_NAME']

def test_onboarding_flow():
    """Testa o fluxo completo de onboarding."""
    print_header("Testando fluxo completo de onboarding")
    
    context = MockContext()
    
    # Etapa 1: Nome
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "João Silva")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Nome): {response[:100]}...")
    
    # Etapa 2: Idade
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "30")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Idade): {response[:100]}...")
    
    # Etapa 3: Gênero
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "Masculino")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Gênero): {response[:100]}...")
    
    # Etapa 4: Peso
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "75.5")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Peso): {response[:100]}...")
    
    # Etapa 5: Altura
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "180")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Altura): {response[:100]}...")
    
    # Etapa 6: Nível de atividade
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "3")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Nível de atividade): {response[:100]}...")
    
    # Etapa 7: Objetivo
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "1")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Objetivo): {response[:100]}...")
    
    # Etapa 8: Tipo de dieta
    update = MockUpdate(TEST_USER_ID, TEST_USERNAME, TEST_FULL_NAME, "1")
    response = OnboardingHandler.handle_message(update, context)
    print(f"Resposta (Tipo de dieta): {response[:100]}...")
    
    # Verifica se o onboarding foi concluído
    conversation = ConversationManager.get_state(TEST_USER_ID)
    print(f"Estado final: {conversation['state']}")
    
    # Verifica se o usuário foi atualizado no banco de dados
    user = UserRepository.get_user_by_id(TEST_USER_ID)
    print(f"Dados do usuário: {user}")
    
    return (conversation['state'] == ConversationManager.STATES['COMPLETED'] and 
            user and user['onboarding_complete'] == 1)

def main():
    """Função principal para testar o fluxo de onboarding."""
    print_header("TESTE DO FLUXO DE ONBOARDING DO NUTRIBOT EVOLVE")
    
    # Limpa dados de teste anteriores
    reset_database()
    
    # Testa o comando /start
    start_success = test_start_command()
    
    # Testa o comando /iniciar
    iniciar_success = test_iniciar_command()
    
    # Testa o fluxo completo de onboarding
    flow_success = test_onboarding_flow()
    
    # Resumo dos testes
    print_header("RESUMO DOS TESTES")
    print(f"Comando /start: {'✅ OK' if start_success else '❌ FALHA'}")
    print(f"Comando /iniciar: {'✅ OK' if iniciar_success else '❌ FALHA'}")
    print(f"Fluxo completo de onboarding: {'✅ OK' if flow_success else '❌ FALHA'}")
    
    # Verifica se todos os testes passaram
    all_tests_passed = start_success and iniciar_success and flow_success
    
    if all_tests_passed:
        print("\n✅ Todos os testes passaram! O fluxo de onboarding está funcionando corretamente.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs para mais detalhes.")
    
    # Limpa dados de teste
    reset_database()

# Dados de teste
TEST_USER_ID = 123456789
TEST_USERNAME = "test_user"
TEST_FULL_NAME = "Test User"

if __name__ == "__main__":
    main()
