"""
Otimizações para o NutriBot Evolve.
Este arquivo contém melhorias de desempenho e usabilidade para o bot.
"""

import sys
import os
import logging
from pathlib import Path
import functools
import time

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Decorador para medir tempo de execução
def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Função {func.__name__} executada em {end_time - start_time:.4f} segundos")
        return result
    return wrapper

# Decorador para cache em memória
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Otimizações para o banco de dados
def optimize_database():
    """Otimiza o banco de dados SQLite."""
    from database.db_manager import db_manager
    
    logger.info("Otimizando banco de dados...")
    
    try:
        conn = db_manager.connect()
        
        # Executa VACUUM para otimizar o banco de dados
        conn.execute("VACUUM")
        
        # Executa ANALYZE para otimizar estatísticas
        conn.execute("ANALYZE")
        
        # Cria índices para melhorar performance de consultas frequentes
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_meals_user_id ON meals(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_meals_meal_date ON meals(meal_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_photos_user_id ON photos(user_id)")
        
        conn.commit()
        logger.info("Banco de dados otimizado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao otimizar banco de dados: {e}")
        return False
    finally:
        db_manager.close()

# Otimizações para o analisador de refeições
def optimize_meal_analyzer():
    """Otimiza o analisador de refeições."""
    from utils.meal_analyzer import MealAnalyzer
    
    logger.info("Otimizando analisador de refeições...")
    
    # Aplica o decorador de cache ao método de análise
    MealAnalyzer.analyze_meal_text = memoize(MealAnalyzer.analyze_meal_text)
    
    logger.info("Analisador de refeições otimizado com sucesso.")
    return True

# Otimizações para o calculador de calorias
def optimize_calorie_calculator():
    """Otimiza o calculador de calorias."""
    from utils.calorie_calculator import CalorieCalculator
    
    logger.info("Otimizando calculador de calorias...")
    
    # Aplica o decorador de cache aos métodos de cálculo
    CalorieCalculator.calculate_bmr = memoize(CalorieCalculator.calculate_bmr)
    CalorieCalculator.calculate_tdee = memoize(CalorieCalculator.calculate_tdee)
    CalorieCalculator.calculate_macros = memoize(CalorieCalculator.calculate_macros)
    
    logger.info("Calculador de calorias otimizado com sucesso.")
    return True

# Otimizações para o gerador de relatórios
def optimize_report_generator():
    """Otimiza o gerador de relatórios."""
    from utils.report_generator import ReportGenerator
    
    logger.info("Otimizando gerador de relatórios...")
    
    # Aplica o decorador de medição de tempo aos métodos de geração de relatórios
    ReportGenerator.generate_weekly_report = measure_time(ReportGenerator.generate_weekly_report)
    ReportGenerator.generate_monthly_report = measure_time(ReportGenerator.generate_monthly_report)
    
    logger.info("Gerador de relatórios otimizado com sucesso.")
    return True

# Otimizações para o manipulador de mensagens
def optimize_message_handling():
    """Otimiza o manipulador de mensagens."""
    logger.info("Otimizando manipulador de mensagens...")
    
    # Modifica o arquivo main.py para otimizar o manipulador de mensagens
    main_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Adiciona cache para estados de conversação
        if "# Cache para estados de conversação" not in content:
            # Encontra a função handle_message
            handle_message_pos = content.find("async def handle_message")
            if handle_message_pos != -1:
                # Encontra o início da função
                function_start = content.find("    user_id = update.effective_user.id", handle_message_pos)
                if function_start != -1:
                    # Adiciona cache antes da verificação de estado
                    new_content = content[:function_start] + """    # Cache para estados de conversação
    user_id = update.effective_user.id
    
    # Usa cache para melhorar performance
    if hasattr(context, 'user_states') and user_id in context.user_states:
        conversation = context.user_states[user_id]
    else:
        # Obtém o estado atual da conversação
        conversation = ConversationManager.get_state(user_id)
        if not hasattr(context, 'user_states'):
            context.user_states = {}
        context.user_states[user_id] = conversation
    
""" + content[function_start + 4:]
                    
                    # Salva o arquivo modificado
                    with open(main_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    logger.info("Manipulador de mensagens otimizado com sucesso.")
                    return True
        
        logger.warning("Não foi possível otimizar o manipulador de mensagens: estrutura não encontrada.")
        return False
    except Exception as e:
        logger.error(f"Erro ao otimizar manipulador de mensagens: {e}")
        return False

# Otimizações para a interface do usuário
def optimize_user_interface():
    """Otimiza a interface do usuário."""
    logger.info("Otimizando interface do usuário...")
    
    # Modifica as mensagens para melhorar a usabilidade
    try:
        # Otimiza as mensagens de ajuda
        config_path = os.path.join(os.path.dirname(__file__), 'config.py')
        
        with open(config_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Encontra a mensagem de ajuda
        help_pos = content.find("HELP_MESSAGE = ")
        if help_pos != -1:
            # Encontra o início e fim da mensagem
            start = content.find('"""', help_pos)
            end = content.find('"""', start + 3)
            
            if start != -1 and end != -1:
                # Substitui a mensagem de ajuda por uma versão otimizada
                new_help = '''"""
Comandos disponíveis:

📝 Cadastro e Configuração
/iniciar - Inicia o processo de cadastro
/ajuda - Mostra esta mensagem de ajuda

🍽️ Alimentação
/refeicao - Registra uma nova refeição
/status - Mostra seu consumo calórico do dia
/sugestao - Recebe uma sugestão de refeição
/motivacao - Recebe uma mensagem motivacional

📸 Fotos e Progresso
/foto - Envia uma foto para acompanhamento
/fotos - Lista suas fotos anteriores
/comparar - Compara duas fotos (ex: /comparar 1 3)
/dicas_foto - Mostra dicas para tirar melhores fotos

📊 Relatórios
/relatorio - Gera um relatório semanal
/relatorio_mensal - Gera um relatório mensal (premium)
/exportar - Exporta relatório em PDF (premium)

✨ Premium
/premium - Conhecer recursos premium
/ativar_premium - Ativar recursos premium
/treino - Recebe um plano de treino personalizado (premium)
/nutricionista - Agenda consulta com nutricionista (premium)
"""'''
                
                new_content = content[:start] + new_help + content[end + 3:]
                
                # Salva o arquivo modificado
                with open(config_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                logger.info("Interface do usuário otimizada com sucesso.")
                return True
        
        logger.warning("Não foi possível otimizar a interface do usuário: estrutura não encontrada.")
        return False
    except Exception as e:
        logger.error(f"Erro ao otimizar interface do usuário: {e}")
        return False

# Função principal para executar todas as otimizações
def run_all_optimizations():
    """Executa todas as otimizações."""
    logger.info("=== INICIANDO OTIMIZAÇÕES DO NUTRIBOT EVOLVE ===")
    
    # Lista de otimizações
    optimizations = [
        optimize_database,
        optimize_meal_analyzer,
        optimize_calorie_calculator,
        optimize_report_generator,
        optimize_message_handling,
        optimize_user_interface
    ]
    
    # Executa as otimizações
    results = []
    for optimization in optimizations:
        results.append(optimization())
    
    # Exibe resultado final
    logger.info("=== RESULTADO DAS OTIMIZAÇÕES ===")
    total_optimizations = len(optimizations)
    successful_optimizations = sum(results)
    
    logger.info(f"Total de otimizações: {total_optimizations}")
    logger.info(f"Otimizações bem-sucedidas: {successful_optimizations}")
    logger.info(f"Otimizações com falha: {total_optimizations - successful_optimizations}")
    
    if successful_optimizations == total_optimizations:
        logger.info("TODAS AS OTIMIZAÇÕES FORAM BEM-SUCEDIDAS!")
    else:
        logger.warning(f"{total_optimizations - successful_optimizations} OTIMIZAÇÕES FALHARAM!")
    
    return successful_optimizations == total_optimizations

if __name__ == "__main__":
    run_all_optimizations()
