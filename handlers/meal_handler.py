"""
Manipulador de refeições para o NutriBot Evolve.
Responsável por gerenciar o registro e análise de refeições.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from database.meal_repository import MealRepository
from utils.meal_analyzer import MealAnalyzer
from utils.conversation_manager import ConversationManager

class MealHandler:
    """Classe para gerenciar o registro e análise de refeições."""
    
    # Estados de conversação para registro de refeições
    STATES = {
        'WAITING_MEAL_TEXT': 'waiting_meal_text',
        'WAITING_MEAL_CONFIRMATION': 'waiting_meal_confirmation',
        'COMPLETED': 'completed'
    }
    
    # Mensagens para interação com o usuário
    MESSAGES = {
        'ask_meal': """
Por favor, descreva o que você comeu.
Exemplo: "Comi 100g de arroz, 150g de frango grelhado e uma salada de alface e tomate."
""",
        'meal_confirmation': """
Analisei sua refeição:

🍽️ {meal_type_display}:
{food_items_text}

📊 Valores nutricionais:
• Calorias: {calories} kcal
• Proteínas: {protein}g
• Carboidratos: {carbs}g
• Gorduras: {fat}g

Esta análise está correta? (Sim/Não)
""",
        'meal_registered': """
✅ Refeição registrada com sucesso!

📊 Resumo do seu dia até agora:
• Calorias consumidas: {consumed_calories} kcal
• Calorias restantes: {remaining_calories} kcal
• Proteínas: {consumed_protein}g / {target_protein}g
• Carboidratos: {consumed_carbs}g / {target_carbs}g
• Gorduras: {consumed_fat}g / {target_fat}g

{progress_message}
""",
        'meal_canceled': "Registro de refeição cancelado. Você pode tentar novamente quando quiser."
    }
    
    # Mapeamento de tipos de refeição para exibição
    MEAL_TYPE_DISPLAY = {
        'cafe_da_manha': 'Café da Manhã',
        'lanche_manha': 'Lanche da Manhã',
        'almoco': 'Almoço',
        'lanche_tarde': 'Lanche da Tarde',
        'jantar': 'Jantar',
        'ceia': 'Ceia',
        'refeicao': 'Refeição'
    }
    
    def __init__(self):
        """Inicializa o manipulador de refeições."""
        self.meal_analyzer = MealAnalyzer()
    
    def handle_refeicao_command(self, update, context):
        """
        Manipula o comando /refeicao para iniciar o registro de uma refeição.
        
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
            return "Você precisa completar o cadastro inicial antes de registrar refeições. Use /iniciar para começar."
        
        # Inicia o processo de registro de refeição
        ConversationManager.set_state(user_id, MealHandler.STATES['WAITING_MEAL_TEXT'])
        
        # Retorna a mensagem solicitando a descrição da refeição
        return MealHandler.MESSAGES['ask_meal']
    
    def handle_message(self, update, context):
        """
        Manipula mensagens durante o processo de registro de refeição.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta ou None se não estiver em registro de refeição
        """
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Obtém o estado atual da conversação
        conversation = ConversationManager.get_state(user_id)
        
        if not conversation:
            # Usuário não está em processo de registro de refeição
            return None
        
        state = conversation['state']
        context_data = conversation['context'] or {}
        
        # Processa a mensagem com base no estado atual
        if state == MealHandler.STATES['WAITING_MEAL_TEXT']:
            # Analisa o texto da refeição
            meal_data = self.meal_analyzer.analyze_meal_text(message_text)
            
            # Salva os dados no contexto
            ConversationManager.update_context(user_id, {'meal_data': meal_data})
            ConversationManager.set_state(user_id, MealHandler.STATES['WAITING_MEAL_CONFIRMATION'], context_data)
            
            # Prepara o texto dos itens alimentares
            food_items_text = ""
            for item in meal_data['food_items']:
                food_items_text += f"• {item['name'].capitalize()}: {item['quantity']}{item['unit']} - {item['calories']:.0f} kcal\n"
            
            if not food_items_text:
                food_items_text = "Não consegui identificar alimentos específicos na sua descrição."
            
            # Retorna a mensagem de confirmação
            return MealHandler.MESSAGES['meal_confirmation'].format(
                meal_type_display=MealHandler.MEAL_TYPE_DISPLAY.get(meal_data['meal_type'], 'Refeição'),
                food_items_text=food_items_text,
                calories=round(meal_data['nutrition']['calories']),
                protein=round(meal_data['nutrition']['protein']),
                carbs=round(meal_data['nutrition']['carbs']),
                fat=round(meal_data['nutrition']['fat'])
            )
            
        elif state == MealHandler.STATES['WAITING_MEAL_CONFIRMATION']:
            # Verifica a resposta de confirmação
            response = message_text.lower()
            
            if response in ['sim', 's', 'yes', 'y', 'confirmar', 'confirmo']:
                # Registra a refeição no banco de dados
                return self._register_meal(user_id, context_data)
            else:
                # Cancela o registro
                ConversationManager.set_state(user_id, MealHandler.STATES['COMPLETED'])
                return MealHandler.MESSAGES['meal_canceled']
        
        return None
    
    def _register_meal(self, user_id, context_data):
        """
        Registra a refeição no banco de dados.
        
        Args:
            user_id (int): ID do usuário no Telegram
            context_data (dict): Dados do contexto da conversação
            
        Returns:
            str: Mensagem de confirmação
        """
        # Obtém os dados da refeição do contexto
        meal_data = context_data.get('meal_data', {})
        
        if not meal_data:
            return "Erro ao registrar refeição. Por favor, tente novamente."
        
        # Obtém os dados do usuário
        user = UserRepository.get_user_by_id(user_id)
        
        # Registra a refeição
        MealRepository.add_meal(
            user_id=user_id,
            meal_type=meal_data['meal_type'],
            description=meal_data['description'],
            calories=meal_data['nutrition']['calories'],
            protein=meal_data['nutrition']['protein'],
            carbs=meal_data['nutrition']['carbs'],
            fat=meal_data['nutrition']['fat']
        )
        
        # Obtém os totais diários
        daily_totals = MealRepository.get_daily_totals(user_id)
        
        # Calcula as calorias e macros restantes
        daily_calories = user['daily_calories']
        remaining_calories = daily_calories - daily_totals['calories']
        
        # Calcula os macros alvo com base nas calorias diárias e tipo de dieta
        from utils.calorie_calculator import CalorieCalculator
        target_macros = CalorieCalculator.calculate_macros(daily_calories, user['diet_type'])
        
        # Prepara mensagem de progresso
        progress_percentage = (daily_totals['calories'] / daily_calories) * 100 if daily_calories > 0 else 0
        
        if progress_percentage < 50:
            progress_message = "Você ainda tem bastante espaço para mais refeições hoje! 🍽️"
        elif progress_percentage < 80:
            progress_message = "Você está indo bem no seu plano alimentar hoje! 👍"
        elif progress_percentage < 100:
            progress_message = "Você está quase atingindo seu limite calórico diário. 🔍"
        elif progress_percentage < 110:
            progress_message = "Você atingiu seu limite calórico diário. Considere encerrar a alimentação por hoje. ⚠️"
        else:
            progress_message = "Você excedeu seu limite calórico diário. Tente compensar nos próximos dias. ⚠️"
        
        # Finaliza o estado de conversação
        ConversationManager.set_state(user_id, MealHandler.STATES['COMPLETED'])
        
        # Retorna a mensagem de confirmação
        return MealHandler.MESSAGES['meal_registered'].format(
            consumed_calories=round(daily_totals['calories']),
            remaining_calories=round(remaining_calories),
            consumed_protein=round(daily_totals['protein']),
            target_protein=round(target_macros['protein']),
            consumed_carbs=round(daily_totals['carbs']),
            target_carbs=round(target_macros['carbs']),
            consumed_fat=round(daily_totals['fat']),
            target_fat=round(target_macros['fat']),
            progress_message=progress_message
        )
    
    def handle_status_command(self, update, context):
        """
        Manipula o comando /status para mostrar o consumo calórico do dia.
        
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
            return "Você precisa completar o cadastro inicial antes de verificar seu status. Use /iniciar para começar."
        
        # Obtém os totais diários
        daily_totals = MealRepository.get_daily_totals(user_id)
        
        # Calcula as calorias e macros restantes
        daily_calories = user['daily_calories']
        remaining_calories = daily_calories - daily_totals['calories']
        
        # Calcula os macros alvo com base nas calorias diárias e tipo de dieta
        from utils.calorie_calculator import CalorieCalculator
        target_macros = CalorieCalculator.calculate_macros(daily_calories, user['diet_type'])
        
        # Prepara mensagem de progresso
        progress_percentage = (daily_totals['calories'] / daily_calories) * 100 if daily_calories > 0 else 0
        
        if progress_percentage < 50:
            progress_message = "Você ainda tem bastante espaço para mais refeições hoje! 🍽️"
        elif progress_percentage < 80:
            progress_message = "Você está indo bem no seu plano alimentar hoje! 👍"
        elif progress_percentage < 100:
            progress_message = "Você está quase atingindo seu limite calórico diário. 🔍"
        elif progress_percentage < 110:
            progress_message = "Você atingiu seu limite calórico diário. Considere encerrar a alimentação por hoje. ⚠️"
        else:
            progress_message = "Você excedeu seu limite calórico diário. Tente compensar nos próximos dias. ⚠️"
        
        # Obtém as refeições do dia
        import datetime
        meals = MealRepository.get_meals_by_user_and_date(user_id, datetime.datetime.now().date())
        
        meals_text = ""
        if meals:
            for meal in meals:
                meal_type_display = MealHandler.MEAL_TYPE_DISPLAY.get(meal['meal_type'], 'Refeição')
                meals_text += f"\n🍽️ {meal_type_display}: {meal['calories']:.0f} kcal"
        else:
            meals_text = "\nVocê ainda não registrou refeições hoje."
        
        # Retorna a mensagem de status
        return f"""
📊 Seu status alimentar de hoje:

• Calorias consumidas: {round(daily_totals['calories'])} kcal
• Calorias restantes: {round(remaining_calories)} kcal
• Proteínas: {round(daily_totals['protein'])}g / {round(target_macros['protein'])}g
• Carboidratos: {round(daily_totals['carbs'])}g / {round(target_macros['carbs'])}g
• Gorduras: {round(daily_totals['fat'])}g / {round(target_macros['fat'])}g

{progress_message}

📝 Refeições registradas hoje:{meals_text}
"""
