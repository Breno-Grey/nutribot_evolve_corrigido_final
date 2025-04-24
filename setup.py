"""
Script de instalação simplificada para o NutriBot Evolve.
Este script automatiza todo o processo de instalação e configuração.
"""

import os
import sys
import subprocess
import importlib
import shutil
from pathlib import Path

def print_header(message):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"❌ Versão do Python incompatível: {sys.version}")
        print(f"   É necessário Python {required_version[0]}.{required_version[1]} ou superior.")
        return False
    
    print(f"✅ Versão do Python compatível: {sys.version}")
    return True

def install_dependencies():
    """Instala todas as dependências necessárias."""
    print("Instalando dependências...")
    try:
        # Verifica se o arquivo requirements.txt existe
        if not os.path.exists("requirements.txt"):
            print("❌ Arquivo requirements.txt não encontrado!")
            return False
            
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_directories():
    """Cria os diretórios necessários para o funcionamento do bot."""
    print("Criando diretórios necessários...")
    directories = ['photos', 'reports']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Diretório '{directory}' criado/verificado.")
    
    return True

def initialize_database():
    """Inicializa o banco de dados."""
    print("Inicializando banco de dados...")
    try:
        # Importa o gerenciador de banco de dados
        sys.path.append(os.getcwd())
        from database.db_manager import db_manager
        
        # Inicializa o banco de dados
        db_manager.initialize_database()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return False

def configure_bot_token():
    """Configura o token do bot do Telegram."""
    print("Configurando token do bot...")
    
    config_path = os.path.join(os.getcwd(), 'config.py')
    
    # Verifica se o arquivo config.py existe
    if not os.path.exists(config_path):
        print("❌ Arquivo config.py não encontrado!")
        return False
    
    # Lê o conteúdo atual
    with open(config_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Verifica se o token já está configurado
    if 'BOT_TOKEN = "SEU_TOKEN_AQUI"' in content or 'BOT_TOKEN = ""' in content:
        token = input("\nDigite o token do seu bot do Telegram (obtido através do @BotFather): ")
        
        if not token:
            print("⚠️ Nenhum token fornecido. Você precisará configurar manualmente mais tarde.")
            return False
        
        # Substitui o token
        content = content.replace('BOT_TOKEN = "SEU_TOKEN_AQUI"', f'BOT_TOKEN = "{token}"')
        content = content.replace('BOT_TOKEN = ""', f'BOT_TOKEN = "{token}"')
        
        # Salva o arquivo atualizado
        with open(config_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("✅ Token configurado com sucesso!")
    else:
        print("✅ Token já configurado anteriormente.")
    
    return True

def test_installation():
    """Testa se a instalação foi bem-sucedida."""
    print("Testando instalação...")
    
    # Verifica se os módulos principais podem ser importados
    try:
        sys.path.append(os.getcwd())
        
        # Tenta importar os módulos principais
        from database import db_manager
        from utils import calorie_calculator
        from handlers import onboarding_handler
        
        print("✅ Módulos principais importados com sucesso!")
        
        # Verifica se o banco de dados existe
        if os.path.exists(os.path.join(os.getcwd(), 'nutribot.db')):
            print("✅ Banco de dados encontrado!")
        else:
            print("⚠️ Banco de dados não encontrado. Será criado na primeira execução.")
        
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar instalação: {e}")
        return False

def main():
    """Função principal para instalar e configurar o NutriBot Evolve."""
    print_header("INSTALAÇÃO DO NUTRIBOT EVOLVE")
    print("Este script irá guiá-lo através do processo de instalação completo.")
    
    # Verifica versão do Python
    if not check_python_version():
        print("\n❌ Por favor, atualize sua versão do Python para continuar.")
        return
    
    # Instala dependências
    if not install_dependencies():
        print("\n❌ Não foi possível instalar todas as dependências.")
        print("   Tente instalar manualmente com: pip install -r requirements.txt")
        return
    
    # Cria diretórios
    create_directories()
    
    # Inicializa banco de dados
    if not initialize_database():
        print("\n❌ Não foi possível inicializar o banco de dados.")
        print("   Verifique se você tem permissões de escrita no diretório atual.")
        return
    
    # Configura token do bot
    configure_bot_token()
    
    # Testa instalação
    if test_installation():
        print_header("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("O NutriBot Evolve está pronto para uso.")
        print("\nPara iniciar o bot, execute: python main.py")
    else:
        print_header("INSTALAÇÃO CONCLUÍDA COM AVISOS")
        print("Alguns testes falharam, mas você ainda pode tentar executar o bot.")
        print("\nPara iniciar o bot, execute: python main.py")

if __name__ == "__main__":
    main()
