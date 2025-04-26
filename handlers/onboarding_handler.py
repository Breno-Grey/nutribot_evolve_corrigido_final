"""
Manipulador de onboarding para o NutriBot Evolve.
Responsável por gerenciar o processo de cadastro inicial do usuário.
"""

import sys
import traceback
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from utils.conversation_manager import ConversationManager
from utils.calorie_calculator import CalorieCalculator
import config

class OnboardingHandler:
    """Classe para gerenciar o processo de onboarding."""
    
    # Mensagens para cada etapa do onboarding
    MESSAGES = {
        'welcome': """
Olá! Bem-vindo ao NutriBot Evolve, seu assistente pessoal de dieta! 🥗💪

Estou aqui para ajudar você a alcançar seus objetivos de forma prática e personalizada.

Vamos começar com algumas perguntas para conhecer melhor você e criar um plano alimentar adequado às suas necessidades.

Digite /iniciar para começarmos!
""",
        'ask_name': """
Ótimo! Vamos começar.

Qual é o seu nome completo?
""",
        'ask_age': """
Prazer em conhecê-lo, {name}! 

Qual é a sua idade?
""",
        'ask_gender': """
Obrigado! 

Qual é o seu gênero? (Masculino/Feminino)
""",
        'ask_weight': """
Entendido!

Qual é o seu peso atual em kg? (exemplo: 70.5)
""",
        'ask_height': """
Anotado!

Qual é a sua altura em cm? (exemplo: 175)
""",
        'ask_activity': """
Perfeito!

Qual é o seu nível de atividade física?

1️⃣ Sedentário (pouco ou nenhum exercício)
2️⃣ Leve (exercício leve 1-3 dias por semana)
3️⃣ Moderado (exercício moderado 3-5 dias por semana)
4️⃣ Ativo (exercício intenso 6-7 dias por semana)
5️⃣ Muito ativo (exercício muito intenso, trabalho físico ou treinamento 2x por dia)

Responda com o número correspondente.
""",
        'ask_goal': """
Ótimo!

Qual é o seu objetivo principal?

1️⃣ Emagrecer
2️⃣ Manter o peso
3️⃣ Ganhar massa muscular

Responda com o número correspondente.
""",
        'ask_diet_type': """
Entendido!

Qual tipo de dieta você prefere seguir?

1️⃣ Flexível (sem restrições específicas)
2️⃣ Low Carb (baixo carboidrato)
3️⃣ Cetogênica (muito baixo carboidrato, alto em gorduras)
4️⃣ Vegetariana (sem carne)
5️⃣ Vegana (sem produtos de origem animal)

Responda com o número correspondente.
""",
        'completion': """
🎉 Parabéns, {name}! Seu cadastro foi concluído com sucesso!

Com base nas informações fornecidas, calculei seu gasto calórico diário:

📊 Informações do seu perfil:
• Nome: {name}
• Idade: {age} anos
• Gênero: {gender}
• Peso: {weight} kg
• Altura: {height} cm
• Nível de atividade: {activity}
• Objetivo: {goal}
• Tipo de dieta: {diet_type}

🔥 Seu metabolismo basal (TMB): {bmr} calorias
🏃‍♂️ Seu gasto energético total (TDEE): {tdee} calorias
✅ Calorias diárias recomendadas: {daily_calories} calorias

📋 Distribuição recomendada de macronutrientes:
• Proteínas: {protein}g
• Carboidratos: {carbs}g
• Gorduras: {fat}g

Agora você pode começar a registrar suas refeições! Basta me enviar uma mensagem descrevendo o que você comeu, e eu calcularei as calorias e macronutrientes automaticamente.

Use /ajuda para ver todos os comandos disponíveis.
"""
    }
    
    # Mapeamento de respostas numéricas para níveis de atividade
    ACTIVITY_MAPPING = {
        '1': 'sedentario',
        '2': 'leve',
        '3': 'moderado',
        '4': 'ativo',
        '5': 'muito_ativo'
    }
    
    # Mapeamento de respostas numéricas para objetivos
    GOAL_MAPPING = {
        '1': 'emagrecer',
        '2': 'manter',
        '3': 'ganhar_massa'
    }
    
    # Mapeamento de respostas numéricas para tipos de dieta
    DIET_MAPPING = {
        '1': 'flexivel',
        '2': 'low_carb',
        '3': 'cetogenica',
        '4': 'vegetariana',
        '5': 'vegana'
    }
    
    @staticmethod
    def handle_start(update, context):
        """
        Manipula o comando /start.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        try:
            user_id = update.effective_user.id
            username = update.effective_user.username
            full_name = update.effective_user.full_name
            
            # Verifica se o usuário já existe
            user = UserRepository.get_user_by_id(user_id)
            
            if not user:
                # Cria um novo usuário
                UserRepository.create_user(user_id, username, full_name)
            
            # Retorna a mensagem de boas-vindas
            return OnboardingHandler.MESSAGES['welcome']
        except Exception as e:
            print(f"Erro em handle_start: {e}")
            traceback.print_exc()
            return "Ocorreu um erro ao iniciar. Por favor, tente novamente com /start."
    
    @staticmethod
    def handle_iniciar(update, context):
        """
        Manipula o comando /iniciar para começar o onboarding.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        try:
            user_id = update.effective_user.id
            
            # Verifica se o usuário já existe
            user = UserRepository.get_user_by_id(user_id)
            
            if not user:
                # Cria um novo usuário
                UserRepository.create_user(user_id, update.effective_user.username, update.effective_user.full_name)
            
            # Inicia o processo de onboarding
            ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_NAME'])
            
            # Retorna a mensagem solicitando o nome
            return OnboardingHandler.MESSAGES['ask_name']
        except Exception as e:
            print(f"Erro em handle_iniciar: {e}")
            traceback.print_exc()
            return "Ocorreu um erro ao iniciar o cadastro. Por favor, tente novamente com /iniciar."
    
    @staticmethod
    def handle_message(update, context):
        """
        Manipula mensagens durante o processo de onboarding.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta ou None se não estiver em onboarding
        """
        try:
            user_id = update.effective_user.id
            message_text = update.message.text
            
            # Obtém o estado atual da conversação
            conversation = ConversationManager.get_state(user_id)
            
            if not conversation:
                # Usuário não está em processo de onboarding
                return None
            
            state = conversation['state']
            context_data = conversation.get('context', {}) or {}
            
            print(f"Estado atual: {state}, Mensagem: {message_text}, Contexto: {context_data}")
            
            # Processa a mensagem com base no estado atual
            if state == ConversationManager.STATES['WAITING_NAME']:
                # Salva o nome e avança para a próxima etapa
                context_data['name'] = message_text
                ConversationManager.update_context(user_id, {'name': message_text})
                ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_AGE'], context_data)
                
                # Retorna a mensagem solicitando a idade
                return OnboardingHandler.MESSAGES['ask_age'].format(name=message_text)
                
            elif state == ConversationManager.STATES['WAITING_AGE']:
                try:
                    # Valida e salva a idade
                    age = int(message_text)
                    if age < 12 or age > 120:
                        return "Por favor, informe uma idade válida entre 12 e 120 anos."
                    
                    ConversationManager.update_context(user_id, {'age': age})
                    context_data['age'] = age # Atualiza o contexto local
                    ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_GENDER'], context_data)
                    
                    # Retorna a mensagem solicitando o gênero
                    return OnboardingHandler.MESSAGES['ask_gender']
                    
                except ValueError:
                    return "Por favor, informe uma idade válida em números (exemplo: 30)."
                
            elif state == ConversationManager.STATES['WAITING_GENDER']:
                # Valida e salva o gênero
                gender = message_text.lower()
                
                if gender not in ['masculino', 'feminino', 'm', 'f']:
                    return "Por favor, informe 'Masculino' ou 'Feminino'."
                
                # Normaliza o gênero
                if gender == 'm':
                    gender = 'masculino'
                elif gender == 'f':
                    gender = 'feminino'
                
                ConversationManager.update_context(user_id, {'gender': gender})
                context_data['gender'] = gender # Atualiza o contexto local
                ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_WEIGHT'], context_data)
                
                # Retorna a mensagem solicitando o peso
                return OnboardingHandler.MESSAGES['ask_weight']
                
            elif state == ConversationManager.STATES['WAITING_WEIGHT']:
                try:
                    # Valida e salva o peso
                    weight = float(message_text.replace(',', '.'))
                    if weight < 30 or weight > 300:
                        return "Por favor, informe um peso válido entre 30 e 300 kg."
                    
                    ConversationManager.update_context(user_id, {'weight': weight})
                    context_data['weight'] = weight # Atualiza o contexto local
                    ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_HEIGHT'], context_data)
                    
                    # Retorna a mensagem solicitando a altura
                    return OnboardingHandler.MESSAGES['ask_height']
                    
                except ValueError:
                    return "Por favor, informe um peso válido em números (exemplo: 70.5)."
                
            elif state == ConversationManager.STATES['WAITING_HEIGHT']:
                try:
                    # Valida e salva a altura
                    height = float(message_text.replace(',', '.'))
                    if height < 100 or height > 250:
                        return "Por favor, informe uma altura válida entre 100 e 250 cm."
                    
                    ConversationManager.update_context(user_id, {'height': height})
                    context_data['height'] = height # Atualiza o contexto local
                    ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_ACTIVITY'], context_data)
                    
                    # Retorna a mensagem solicitando o nível de atividade
                    return OnboardingHandler.MESSAGES['ask_activity']
                    
                except ValueError:
                    return "Por favor, informe uma altura válida em números (exemplo: 175)."
                
            elif state == ConversationManager.STATES['WAITING_ACTIVITY']:
                # Valida e salva o nível de atividade
                if message_text not in ['1', '2', '3', '4', '5']:
                    return "Por favor, responda com um número de 1 a 5 correspondente ao seu nível de atividade."
                
                activity = OnboardingHandler.ACTIVITY_MAPPING[message_text]
                ConversationManager.update_context(user_id, {'activity_level': activity})
                context_data['activity_level'] = activity # Atualiza o contexto local
                ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_GOAL'], context_data)
                
                # Retorna a mensagem solicitando o objetivo
                return OnboardingHandler.MESSAGES['ask_goal']
                
            elif state == ConversationManager.STATES['WAITING_GOAL']:
                # Valida e salva o objetivo
                if message_text not in ['1', '2', '3']:
                    return "Por favor, responda com um número de 1 a 3 correspondente ao seu objetivo."
                
                goal = OnboardingHandler.GOAL_MAPPING[message_text]
                ConversationManager.update_context(user_id, {'goal': goal})
                context_data['goal'] = goal # Atualiza o contexto local
                ConversationManager.set_state(user_id, ConversationManager.STATES['WAITING_DIET_TYPE'], context_data)
                
                # Retorna a mensagem solicitando o tipo de dieta
                return OnboardingHandler.MESSAGES['ask_diet_type']
                
            elif state == ConversationManager.STATES['WAITING_DIET_TYPE']:
                # Valida e salva o tipo de dieta
                if message_text not in ['1', '2', '3', '4', '5']:
                    return "Por favor, responda com um número de 1 a 5 correspondente ao tipo de dieta."
                
                diet_type = OnboardingHandler.DIET_MAPPING[message_text]
                
                # Atualiza o contexto com o tipo de dieta antes de completar o onboarding
                context_data['diet_type'] = diet_type
                ConversationManager.update_context(user_id, {'diet_type': diet_type})
                
                # Completa o onboarding
                return OnboardingHandler.complete_onboarding(user_id, context_data)
                
            return None
        except Exception as e:
            print(f"Erro em handle_message: {e}")
            traceback.print_exc()
            return "Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente ou use /iniciar para recomeçar."
    
    @staticmethod
    def complete_onboarding(user_id, context_data):
        """
        Completa o processo de onboarding e calcula as calorias diárias.
        
        Args:
            user_id (int): ID do usuário no Telegram
            context_data (dict): Dados coletados durante o onboarding
            
        Returns:
            str: Mensagem de conclusão
        """
        try:
            print(f"Completando onboarding para usuário {user_id} com dados: {context_data}")
            
            # Verifica se todos os dados necessários estão presentes
            required_fields = ['name', 'age', 'gender', 'weight', 'height', 'activity_level', 'goal', 'diet_type']
            for field in required_fields:
                if field not in context_data or context_data[field] is None:
                    print(f"Campo obrigatório ausente: {field}")
                    return f"Erro: Informação de {field} ausente. Por favor, use /iniciar para recomeçar o cadastro."
            
            # Atualiza o estado para concluído
            ConversationManager.set_state(user_id, ConversationManager.STATES['COMPLETED'], context_data)
            
            # Calcula as calorias diárias
            calorie_data = CalorieCalculator.calculate_daily_calories(
                weight=context_data['weight'],
                height=context_data['height'],
                age=context_data['age'],
                gender=context_data['gender'],
                activity_level=context_data['activity_level'],
                goal=context_data['goal'],
                diet_type=context_data['diet_type']
            )
            
            print(f"Dados de calorias calculados: {calorie_data}")
            
            # Extrai dados de macros
            macros = calorie_data.get('macros', {})
            protein = macros.get('protein')
            carbs = macros.get('carbs')
            fat = macros.get('fat')

            # Atualiza os dados do usuário no banco de dados
            user_data = {
                'full_name': context_data['name'],
                'age': context_data['age'],
                'weight': context_data['weight'],
                'height': context_data['height'],
                'gender': context_data['gender'],
                'activity_level': context_data['activity_level'],
                'goal': context_data['goal'],
                'diet_type': context_data['diet_type'],
                'daily_calories': calorie_data.get('daily_calories'),
                'protein_goal': protein,
                'carb_goal': carbs,
                'fat_goal': fat,
                'bmr': calorie_data.get('bmr'),
                'tdee': calorie_data.get('tdee'),
                'onboarding_completed': True
            }
            UserRepository.update_user(user_id, user_data)
            
            # Formata a mensagem de conclusão
            # Adiciona uma verificação para garantir que os valores de macro existem antes de arredondar
            completion_message = OnboardingHandler.MESSAGES['completion'].format(
                name=context_data['name'],
                age=context_data['age'],
                gender=context_data['gender'].capitalize(),
                weight=context_data['weight'],
                height=context_data['height'],
                activity=context_data['activity_level'].replace('_', ' ').capitalize(),
                goal=context_data['goal'].replace('_', ' ').capitalize(),
                diet_type=context_data['diet_type'].replace('_', ' ').capitalize(),
                bmr=round(calorie_data['bmr']) if calorie_data.get('bmr') is not None else 'N/A',
                tdee=round(calorie_data['tdee']) if calorie_data.get('tdee') is not None else 'N/A',
                daily_calories=round(calorie_data['daily_calories']) if calorie_data.get('daily_calories') is not None else 'N/A',
                protein=round(protein) if protein is not None else 'N/A',
                carbs=round(carbs) if carbs is not None else 'N/A',
                fat=round(fat) if fat is not None else 'N/A'
            )
            
            return completion_message
            
        except Exception as e:
            print(f"Erro em complete_onboarding: {e}")
            traceback.print_exc()
            return "Ocorreu um erro ao finalizar seu cadastro. Por favor, tente novamente ou contate o suporte."

