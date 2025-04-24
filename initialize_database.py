"""
Script para inicializar o banco de dados do NutriBot Evolve.
Este script cria o banco de dados SQLite e todas as tabelas necessárias.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent))

# Importa o gerenciador de banco de dados
from database.db_manager import db_manager

def main():
    """Função principal para inicializar o banco de dados."""
    print("Iniciando criação do banco de dados para o NutriBot Evolve...")
    
    # Cria diretórios necessários
    print("Criando diretórios necessários...")
    os.makedirs('photos', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Inicializa o banco de dados
    print("Inicializando banco de dados...")
    db_manager.initialize_database()
    
    print("\nInicialização concluída com sucesso!")
    print("O banco de dados foi criado e está pronto para uso.")
    print("Para iniciar o bot, execute: python main.py")

if __name__ == "__main__":
    main()
