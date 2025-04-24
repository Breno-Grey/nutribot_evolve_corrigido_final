"""
Arquivo de configuração para o NutriBot Evolve.
Contém constantes, configurações e variáveis de ambiente.
"""

# Token do Telegram Bot (deve ser substituído pelo token real)
TOKEN = "7527630621:AAFVK10miTDtB1ivqZA5HCshQREKaBNs1es"

# Configurações do banco de dados
DATABASE_PATH = "database/nutribot.db"

# Constantes para cálculo de calorias
# Fórmula de Harris-Benedict para cálculo de TMB (Taxa Metabólica Basal)
# Homens: TMB = 88.362 + (13.397 × peso em kg) + (4.799 × altura em cm) - (5.677 × idade em anos)
# Mulheres: TMB = 447.593 + (9.247 × peso em kg) + (3.098 × altura em cm) - (4.330 × idade em anos)
MALE_BMR_CONSTANT = 88.362
MALE_WEIGHT_MULTIPLIER = 13.397
MALE_HEIGHT_MULTIPLIER = 4.799
MALE_AGE_MULTIPLIER = 5.677

FEMALE_BMR_CONSTANT = 447.593
FEMALE_WEIGHT_MULTIPLIER = 9.247
FEMALE_HEIGHT_MULTIPLIER = 3.098
FEMALE_AGE_MULTIPLIER = 4.330

# Multiplicadores de nível de atividade
ACTIVITY_LEVELS = {
    "sedentario": 1.2,  # Pouco ou nenhum exercício
    "leve": 1.375,      # Exercício leve 1-3 dias por semana
    "moderado": 1.55,   # Exercício moderado 3-5 dias por semana
    "ativo": 1.725,     # Exercício intenso 6-7 dias por semana
    "muito_ativo": 1.9  # Exercício muito intenso, trabalho físico ou treinamento 2x por dia
}

# Ajustes de calorias baseados no objetivo
GOAL_ADJUSTMENTS = {
    "emagrecer": -500,   # Déficit calórico para perda de peso
    "manter": 0,         # Manutenção do peso atual
    "ganhar_massa": 500  # Superávit calórico para ganho de massa
}

# Tipos de dieta e suas características
DIET_TYPES = {
    "flexivel": {
        "carbs_percent": 45,
        "protein_percent": 30,
        "fat_percent": 25
    },
    "low_carb": {
        "carbs_percent": 20,
        "protein_percent": 40,
        "fat_percent": 40
    },
    "cetogenica": {
        "carbs_percent": 5,
        "protein_percent": 30,
        "fat_percent": 65
    },
    "vegetariana": {
        "carbs_percent": 55,
        "protein_percent": 25,
        "fat_percent": 20
    },
    "vegana": {
        "carbs_percent": 60,
        "protein_percent": 20,
        "fat_percent": 20
    }
}

# Configurações de mensagens
MAX_MESSAGE_LENGTH = 4096  # Limite de caracteres para mensagens do Telegram

# Configurações de relatórios
REPORT_FREQUENCY = 7  # Frequência de geração de relatórios em dias

# Configurações de lembretes
DEFAULT_REMINDERS = {
    "cafe_da_manha": "08:00",
    "lanche_manha": "10:30",
    "almoco": "13:00",
    "lanche_tarde": "16:00",
    "jantar": "19:30",
    "ceia": "21:30"
}

# Configurações de recursos premium
PREMIUM_FEATURES = [
    "dietas_exclusivas",
    "plano_treino",
    "consulta_nutricionista",
    "relatorios_pdf",
    "analise_avancada_fotos"
]

# Mensagens do sistema
WELCOME_MESSAGE = """
Olá! Bem-vindo ao NutriBot Evolve, seu assistente pessoal de dieta! 🥗💪

Estou aqui para ajudar você a alcançar seus objetivos de forma prática e personalizada.

Vamos começar com algumas perguntas para conhecer melhor você e criar um plano alimentar adequado às suas necessidades.

Digite /iniciar para começarmos!
"""

HELP_MESSAGE = """
Comandos disponíveis:

/iniciar - Inicia o processo de cadastro
/refeicao - Registra uma nova refeição
/status - Mostra seu consumo calórico do dia
/sugestao - Recebe uma sugestão de refeição
/foto - Envia uma foto para acompanhamento
/relatorio - Gera um relatório de progresso
/premium - Conhecer recursos premium
/ajuda - Mostra esta mensagem de ajuda
"""
