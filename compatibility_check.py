"""
Script para verificar e corrigir dependências do NutriBot Evolve.
Este script verifica a versão do python-telegram-bot e seleciona o arquivo main apropriado.
"""

import sys
import importlib
import subprocess
import pkg_resources
import os
import shutil

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

def check_telegram_bot_version():
    """Verifica a versão do python-telegram-bot instalada."""
    try:
        # Verifica se o pacote está instalado
        version = pkg_resources.get_distribution("python-telegram-bot").version
        print(f"✅ python-telegram-bot versão {version} encontrada.")
        
        # Determina a versão principal
        major_version = int(version.split('.')[0])
        return major_version, version
    except pkg_resources.DistributionNotFound:
        print("❌ python-telegram-bot não está instalado.")
        return None, None
    except Exception as e:
        print(f"❌ Erro ao verificar versão do python-telegram-bot: {e}")
        return None, None

def install_dependencies(version=None):
    """Instala as dependências necessárias."""
    print("Instalando dependências...")
    
    # Se uma versão específica do python-telegram-bot foi solicitada
    if version:
        try:
            print(f"Instalando python-telegram-bot versão {version}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"python-telegram-bot=={version}"])
            
            # Instala as outras dependências
            print("Instalando outras dependências...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib==3.5.1", "numpy==1.22.3", "Pillow==9.0.1"])
            
            print("✅ Dependências instaladas com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False
    
    # Caso contrário, instala todas as dependências do requirements.txt
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

def select_appropriate_main_file(major_version):
    """Seleciona o arquivo main.py apropriado com base na versão do python-telegram-bot."""
    if major_version is None:
        print("⚠️ Não foi possível determinar a versão do python-telegram-bot.")
        return False
    
    # Verifica se os arquivos necessários existem
    if major_version >= 20:
        if not os.path.exists("main.py"):
            print("❌ Arquivo main.py não encontrado!")
            return False
        print("✅ Usando main.py (compatível com python-telegram-bot 20+)")
        return True
    else:
        # Verifica se o arquivo main_v13.py existe
        if not os.path.exists("main_v13.py"):
            print("❌ Arquivo main_v13.py não encontrado!")
            return False
        
        # Faz backup do main.py original se existir
        if os.path.exists("main.py"):
            try:
                shutil.copy("main.py", "main_v20.py")
                print("✅ Backup do main.py original criado como main_v20.py")
            except Exception as e:
                print(f"⚠️ Não foi possível fazer backup do main.py: {e}")
        
        # Copia main_v13.py para main.py
        try:
            shutil.copy("main_v13.py", "main.py")
            print("✅ main_v13.py copiado para main.py (compatível com python-telegram-bot 13.x)")
            return True
        except Exception as e:
            print(f"❌ Erro ao copiar main_v13.py para main.py: {e}")
            return False

def main():
    """Função principal para verificar e corrigir dependências."""
    print_header("VERIFICAÇÃO DE COMPATIBILIDADE DO NUTRIBOT EVOLVE")
    print("Este script verificará e corrigirá problemas de compatibilidade.")
    
    # Verifica versão do Python
    if not check_python_version():
        print("\n❌ Por favor, atualize sua versão do Python para continuar.")
        return
    
    # Verifica versão do python-telegram-bot
    major_version, version = check_telegram_bot_version()
    
    if major_version is None:
        # python-telegram-bot não está instalado
        print("\nO python-telegram-bot não está instalado. Instalando versão 13.7...")
        if install_dependencies("13.7"):
            major_version = 13
        else:
            print("\n❌ Não foi possível instalar o python-telegram-bot.")
            return
    
    # Seleciona o arquivo main.py apropriado
    if not select_appropriate_main_file(major_version):
        print("\n❌ Não foi possível selecionar o arquivo main.py apropriado.")
        
        # Tenta instalar a versão 13.7 e usar o arquivo main_v13.py
        print("\nTentando instalar a versão 13.7 do python-telegram-bot...")
        if install_dependencies("13.7") and select_appropriate_main_file(13):
            print("\n✅ Versão 13.7 instalada e arquivo main.py atualizado com sucesso!")
        else:
            print("\n❌ Não foi possível resolver o problema de compatibilidade.")
            return
    
    print_header("VERIFICAÇÃO DE COMPATIBILIDADE CONCLUÍDA")
    print("O NutriBot Evolve está pronto para uso com a versão compatível do python-telegram-bot.")
    print("\nPara iniciar o bot, execute: python main.py")

if __name__ == "__main__":
    main()
