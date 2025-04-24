"""
Script para verificar dependências do NutriBot Evolve.
Este script verifica se todas as bibliotecas necessárias estão instaladas.
"""

import sys
import importlib
import subprocess
import pkg_resources

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

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    required_packages = {
        'python-telegram-bot': '13.7',
        'matplotlib': '3.5.1',
        'numpy': '1.22.3',
        'Pillow': '9.0.1'
    }
    
    missing_packages = []
    outdated_packages = []
    
    for package, version in required_packages.items():
        try:
            # Tenta importar o pacote
            if package == 'python-telegram-bot':
                module_name = 'telegram'
            else:
                module_name = package.lower()
            
            importlib.import_module(module_name)
            
            # Verifica a versão
            installed_version = pkg_resources.get_distribution(package).version
            if installed_version != version:
                outdated_packages.append((package, installed_version, version))
                print(f"⚠️ Versão diferente: {package} {installed_version} (recomendado: {version})")
            else:
                print(f"✅ Dependência instalada: {package} {version}")
                
        except (ImportError, pkg_resources.DistributionNotFound):
            missing_packages.append(package)
            print(f"❌ Dependência não encontrada: {package}")
    
    return missing_packages, outdated_packages

def install_dependencies(packages):
    """Instala as dependências faltantes."""
    if not packages:
        return True
    
    print("\nInstalando dependências faltantes...")
    try:
        for package in packages:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências.")
        return False

def main():
    """Função principal para verificar e instalar dependências."""
    print("Verificando dependências do NutriBot Evolve...\n")
    
    # Verifica versão do Python
    if not check_python_version():
        print("\n❌ Por favor, atualize sua versão do Python para continuar.")
        return False
    
    # Verifica dependências
    print("\nVerificando bibliotecas necessárias:")
    missing_packages, outdated_packages = check_dependencies()
    
    # Instala dependências faltantes
    if missing_packages:
        print("\n⚠️ Algumas dependências estão faltando.")
        choice = input("Deseja instalar as dependências faltantes agora? (s/n): ")
        if choice.lower() == 's':
            if install_dependencies(missing_packages):
                print("\n✅ Todas as dependências foram instaladas com sucesso!")
            else:
                print("\n❌ Não foi possível instalar todas as dependências.")
                print("   Tente instalar manualmente com: pip install -r requirements.txt")
                return False
        else:
            print("\n⚠️ Por favor, instale as dependências manualmente com: pip install -r requirements.txt")
            return False
    
    # Avisa sobre versões diferentes
    if outdated_packages:
        print("\n⚠️ Algumas dependências têm versões diferentes das recomendadas.")
        print("   O bot pode funcionar, mas podem ocorrer comportamentos inesperados.")
        print("   Para instalar as versões recomendadas, execute: pip install -r requirements.txt")
    
    if not missing_packages and not outdated_packages:
        print("\n✅ Todas as dependências estão instaladas corretamente!")
    
    print("\nVerificação de dependências concluída.")
    print("Para inicializar o banco de dados, execute: python initialize_database.py")
    return True

if __name__ == "__main__":
    main()
