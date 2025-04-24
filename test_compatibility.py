"""
Script para testar a compatibilidade do NutriBot Evolve em diferentes ambientes.
Este script verifica se o bot funciona corretamente com diferentes versões do python-telegram-bot.
"""

import os
import sys
import subprocess
import importlib
import pkg_resources
import time

def print_header(message):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def test_import_telegram():
    """Testa a importação da biblioteca python-telegram-bot."""
    print("Testando importação da biblioteca python-telegram-bot...")
    
    try:
        import telegram
        print(f"✅ Biblioteca telegram importada com sucesso (versão {telegram.__version__})")
        
        import telegram.ext
        print("✅ Módulo telegram.ext importado com sucesso")
        
        # Verifica se estamos usando a versão 13.x ou 20.x+
        if hasattr(telegram.ext, 'Updater'):
            print("✅ Classe Updater encontrada (compatível com versão 13.x)")
        else:
            print("❌ Classe Updater não encontrada (incompatível com versão 13.x)")
        
        if hasattr(telegram.ext, 'Application'):
            print("✅ Classe Application encontrada (compatível com versão 20.x+)")
        else:
            print("❌ Classe Application não encontrada (incompatível com versão 20.x+)")
        
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar biblioteca telegram: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_database_initialization():
    """Testa a inicialização do banco de dados."""
    print("\nTestando inicialização do banco de dados...")
    
    try:
        # Verifica se o script initialize_database.py existe
        if not os.path.exists("initialize_database.py"):
            print("❌ Arquivo initialize_database.py não encontrado!")
            return False
        
        # Executa o script
        result = subprocess.run([sys.executable, "initialize_database.py"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Banco de dados inicializado com sucesso")
            return True
        else:
            print(f"❌ Erro ao inicializar banco de dados: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar inicialização do banco de dados: {e}")
        return False

def test_main_file_compatibility():
    """Testa a compatibilidade do arquivo main.py."""
    print("\nTestando compatibilidade do arquivo main.py...")
    
    try:
        # Verifica se o arquivo main.py existe
        if not os.path.exists("main.py"):
            print("❌ Arquivo main.py não encontrado!")
            return False
        
        # Tenta importar o módulo main
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(main)
            print("✅ Arquivo main.py importado com sucesso")
            return True
        except ImportError as e:
            if "Application" in str(e):
                print("❌ Erro de compatibilidade: 'Application' não encontrado")
                print("   Este erro indica que você está usando a versão 13.x do python-telegram-bot")
                print("   mas o arquivo main.py foi escrito para a versão 20.x+")
                return False
            else:
                print(f"❌ Erro de importação: {e}")
                return False
        except Exception as e:
            print(f"❌ Erro ao carregar main.py: {e}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar compatibilidade do main.py: {e}")
        return False

def test_compatibility_check_script():
    """Testa o script de verificação de compatibilidade."""
    print("\nTestando script de verificação de compatibilidade...")
    
    try:
        # Verifica se o script compatibility_check.py existe
        if not os.path.exists("compatibility_check.py"):
            print("❌ Arquivo compatibility_check.py não encontrado!")
            return False
        
        # Executa o script
        print("Executando compatibility_check.py...")
        result = subprocess.run([sys.executable, "compatibility_check.py"], 
                               capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Script de verificação de compatibilidade executado com sucesso")
            return True
        else:
            print(f"❌ Erro ao executar script de verificação de compatibilidade: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar script de verificação de compatibilidade: {e}")
        return False

def test_bot_startup():
    """Testa o início do bot (sem realmente iniciar o polling)."""
    print("\nTestando inicialização do bot (sem polling)...")
    
    # Cria um arquivo de teste temporário
    test_file = "test_bot_startup.py"
    with open(test_file, "w") as f:
        f.write("""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.getcwd())

try:
    # Tenta importar os módulos necessários
    import config
    from database.db_manager import db_manager
    
    # Verifica a versão do python-telegram-bot
    import telegram
    print(f"Versão do python-telegram-bot: {telegram.__version__}")
    
    # Verifica se estamos usando a versão 13.x ou 20.x+
    import telegram.ext
    if hasattr(telegram.ext, 'Updater'):
        print("Usando API da versão 13.x")
        
        # Tenta criar um Updater (sem iniciar o polling)
        from telegram.ext import Updater
        updater = Updater(token=config.BOT_TOKEN)
        print("Updater criado com sucesso")
    elif hasattr(telegram.ext, 'Application'):
        print("Usando API da versão 20.x+")
        
        # Tenta criar um Application (sem iniciar o polling)
        from telegram.ext import Application
        application = Application.builder().token(config.BOT_TOKEN).build()
        print("Application criado com sucesso")
    else:
        print("Versão do python-telegram-bot não reconhecida")
        sys.exit(1)
    
    print("Teste de inicialização concluído com sucesso")
    sys.exit(0)
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)
""")
    
    try:
        # Executa o script de teste
        result = subprocess.run([sys.executable, test_file], 
                               capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Teste de inicialização do bot concluído com sucesso")
            return True
        else:
            print(f"❌ Erro ao testar inicialização do bot: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar inicialização do bot: {e}")
        return False
    finally:
        # Remove o arquivo de teste
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """Função principal para testar a compatibilidade."""
    print_header("TESTE DE COMPATIBILIDADE DO NUTRIBOT EVOLVE")
    print("Este script testará a compatibilidade do bot em seu ambiente atual.")
    
    # Testa importação da biblioteca telegram
    telegram_imported = test_import_telegram()
    
    # Testa inicialização do banco de dados
    database_initialized = test_database_initialization()
    
    # Testa compatibilidade do arquivo main.py
    main_compatible = test_main_file_compatibility()
    
    # Testa script de verificação de compatibilidade
    compatibility_check_works = test_compatibility_check_script()
    
    # Testa inicialização do bot
    bot_starts = test_bot_startup()
    
    # Resumo dos testes
    print_header("RESUMO DOS TESTES DE COMPATIBILIDADE")
    print(f"Importação da biblioteca telegram: {'✅ OK' if telegram_imported else '❌ FALHA'}")
    print(f"Inicialização do banco de dados: {'✅ OK' if database_initialized else '❌ FALHA'}")
    print(f"Compatibilidade do arquivo main.py: {'✅ OK' if main_compatible else '❌ FALHA'}")
    print(f"Script de verificação de compatibilidade: {'✅ OK' if compatibility_check_works else '❌ FALHA'}")
    print(f"Inicialização do bot: {'✅ OK' if bot_starts else '❌ FALHA'}")
    
    # Verifica se todos os testes passaram
    all_tests_passed = telegram_imported and database_initialized and main_compatible and compatibility_check_works and bot_starts
    
    if all_tests_passed:
        print("\n✅ Todos os testes passaram! O NutriBot Evolve é compatível com seu ambiente.")
        print("\nPara iniciar o bot, execute: python main.py")
    else:
        print("\n❌ Alguns testes falharam. Execute o script de verificação de compatibilidade para corrigir os problemas:")
        print("\npython compatibility_check.py")

if __name__ == "__main__":
    main()
