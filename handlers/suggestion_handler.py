"""
Manipulador de sugestões para o NutriBot Evolve.
Responsável por gerenciar sugestões de refeições e mensagens motivacionais.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from utils.meal_suggester import MealSuggester

class SuggestionHandler:
    """Classe para gerenciar sugestões de refeições e mensagens motivacionais."""
    
    # Mensagens para interação com o usuário
    MESSAGES = {
        'suggestion_intro': """
Aqui está uma sugestão de {meal_type} para sua dieta {diet_type}:

🍽️ {suggestion_name}

📝 Descrição: {suggestion_description}

📊 Valores nutricionais:
• Calorias: {calories} kcal
• Proteínas: {protein}g
• Carboidratos: {carbs}g
• Gorduras: {fat}g

👨‍🍳 Modo de preparo:
{recipe}

{motivation_message}
""",
        'no_suggestion': """
Desculpe, não foi possível encontrar uma sugestão específica para sua dieta.
Por favor, tente novamente mais tarde ou escolha outro tipo de refeição.
""",
        'motivation_message': """
Aqui está uma mensagem motivacional para te inspirar:

"{message}"

Continue se esforçando! Você está no caminho certo. 💪
"""
    }
    
    # Mapeamento de tipos de refeição para exibição
    MEAL_TYPE_DISPLAY = {
        'cafe_da_manha': 'café da manhã',
        'lanche_manha': 'lanche da manhã',
        'almoco': 'almoço',
        'lanche_tarde': 'lanche da tarde',
        'jantar': 'jantar',
        'ceia': 'ceia',
        'refeicao': 'refeição'
    }
    
    # Mapeamento de tipos de dieta para exibição
    DIET_TYPE_DISPLAY = {
        'flexivel': 'flexível',
        'low_carb': 'low carb',
        'cetogenica': 'cetogênica',
        'vegetariana': 'vegetariana',
        'vegana': 'vegana'
    }
    
    def __init__(self):
        """Inicializa o manipulador de sugestões."""
        self.meal_suggester = MealSuggester()
    
    def handle_sugestao_command(self, update, context):
        """
        Manipula o comando /sugestao para fornecer uma sugestão de refeição.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário completou o onboarding
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['onboarding_complete']:
            return "Você precisa completar o cadastro inicial antes de receber sugestões. Use /iniciar para começar."
        
        # Obtém o tipo de dieta do usuário
        diet_type = user['diet_type']
        
        # Determina o tipo de refeição com base na hora do dia (simplificado)
        import datetime
        current_hour = datetime.datetime.now().hour
        
        if 5 <= current_hour < 10:
            meal_type = 'cafe_da_manha'
        elif 10 <= current_hour < 12:
            meal_type = 'lanche_manha'
        elif 12 <= current_hour < 15:
            meal_type = 'almoco'
        elif 15 <= current_hour < 18:
            meal_type = 'lanche_tarde'
        elif 18 <= current_hour < 21:
            meal_type = 'jantar'
        else:
            meal_type = 'ceia'
        
        # Verifica se há argumentos adicionais (tipo de refeição específico)
        if context.args and len(context.args) > 0:
            arg = context.args[0].lower()
            if arg in ['cafe', 'café', 'manha', 'manhã']:
                meal_type = 'cafe_da_manha'
            elif arg in ['lanche', 'lanche_manha', 'lanche_tarde']:
                meal_type = 'lanche_tarde'  # Simplificado para qualquer lanche
            elif arg in ['almoco', 'almoço']:
                meal_type = 'almoco'
            elif arg in ['jantar', 'janta']:
                meal_type = 'jantar'
            elif arg in ['ceia', 'noite']:
                meal_type = 'ceia'
        
        # Obtém uma sugestão de refeição
        suggestion = self.meal_suggester.get_meal_suggestion(diet_type, meal_type)
        
        if not suggestion:
            return SuggestionHandler.MESSAGES['no_suggestion']
        
        # Obtém uma mensagem motivacional
        motivation_message = self.meal_suggester.get_motivation_message(user['goal'])
        
        # Retorna a mensagem com a sugestão
        return SuggestionHandler.MESSAGES['suggestion_intro'].format(
            meal_type=SuggestionHandler.MEAL_TYPE_DISPLAY.get(meal_type, 'refeição'),
            diet_type=SuggestionHandler.DIET_TYPE_DISPLAY.get(diet_type, 'personalizada'),
            suggestion_name=suggestion['nome'],
            suggestion_description=suggestion['descricao'],
            calories=suggestion['calorias'],
            protein=suggestion['proteinas'],
            carbs=suggestion['carboidratos'],
            fat=suggestion['gorduras'],
            recipe=suggestion['receita'],
            motivation_message=motivation_message
        )
    
    def handle_motivacao_command(self, update, context):
        """
        Manipula o comando /motivacao para fornecer uma mensagem motivacional.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário completou o onboarding
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['onboarding_complete']:
            return "Você precisa completar o cadastro inicial antes de receber mensagens motivacionais. Use /iniciar para começar."
        
        # Obtém o objetivo do usuário
        goal = user['goal']
        
        # Obtém uma mensagem motivacional
        message = self.meal_suggester.get_motivation_message(goal)
        
        # Retorna a mensagem motivacional
        return SuggestionHandler.MESSAGES['motivation_message'].format(
            message=message
        )
    
    def get_reminder_message(self, user_id, reminder_type):
        """
        Gera uma mensagem de lembrete com base no tipo de lembrete.
        
        Args:
            user_id (int): ID do usuário no Telegram
            reminder_type (str): Tipo de lembrete
            
        Returns:
            str: Mensagem de lembrete
        """
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        
        # Obtém o tipo de dieta e objetivo do usuário
        diet_type = user['diet_type']
        goal = user['goal']
        
        # Mapeia tipos de lembrete para tipos de refeição
        meal_type_mapping = {
            'cafe_da_manha': 'cafe_da_manha',
            'lanche_manha': 'lanche_manha',
            'almoco': 'almoco',
            'lanche_tarde': 'lanche_tarde',
            'jantar': 'jantar',
            'ceia': 'ceia'
        }
        
        # Verifica se é um lembrete de refeição
        if reminder_type in meal_type_mapping:
            meal_type = meal_type_mapping[reminder_type]
            
            # Obtém uma sugestão de refeição
            suggestion = self.meal_suggester.get_meal_suggestion(diet_type, meal_type)
            
            if suggestion:
                return f"""
⏰ Hora do seu {SuggestionHandler.MEAL_TYPE_DISPLAY.get(meal_type, 'refeição')}!

Que tal experimentar: {suggestion['nome']}?
{suggestion['descricao']}

Use /refeicao para registrar o que você comer.
"""
            else:
                return f"""
⏰ Hora do seu {SuggestionHandler.MEAL_TYPE_DISPLAY.get(meal_type, 'refeição')}!

Lembre-se de fazer escolhas saudáveis e registrar sua refeição usando /refeicao.
"""
        
        # Lembrete de água
        elif reminder_type == 'agua':
            return """
💧 Lembrete de hidratação!

Não se esqueça de beber água regularmente. A hidratação adequada é essencial para o metabolismo e para a saúde em geral.
"""
        
        # Lembrete de motivação
        elif reminder_type == 'motivacao':
            # Obtém uma mensagem motivacional
            message = self.meal_suggester.get_motivation_message(goal)
            
            return f"""
✨ Momento de motivação!

{message}

Continue firme em sua jornada! Você está fazendo um ótimo trabalho.
"""
        
        return None
