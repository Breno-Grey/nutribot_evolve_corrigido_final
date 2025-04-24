"""
Manipulador de recursos premium para o NutriBot Evolve.
Responsável por gerenciar assinaturas e recursos premium.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
import config

class PremiumHandler:
    """Classe para gerenciar assinaturas e recursos premium."""
    
    # Mensagens para interação com o usuário
    MESSAGES = {
        'premium_info': """
✨ NutriBot Evolve Premium ✨

Eleve sua experiência com recursos exclusivos:

🥗 Dietas e receitas exclusivas
💪 Acesso a plano de treino integrado
👨‍⚕️ Consultas com nutricionista humano
📊 Relatórios exportáveis em PDF
🔍 Comparação avançada de fotos com IA

Preço: R$ 19,90/mês

Para ativar, use o comando /ativar_premium
""",
        'premium_activated': """
🎉 Parabéns! Você ativou o NutriBot Evolve Premium!

Agora você tem acesso a todos os recursos exclusivos:

• Use /relatorio_mensal para relatórios detalhados de 30 dias
• Use /exportar para obter seus relatórios em PDF
• Use /treino para acessar planos de treino personalizados
• Use /nutricionista para agendar consultas
• Aproveite análises avançadas de fotos e muito mais!

Aproveite ao máximo sua experiência premium!
""",
        'already_premium': """
Você já é um usuário premium! 🌟

Continue aproveitando todos os benefícios exclusivos.

Use /ajuda para ver todos os comandos disponíveis.
""",
        'premium_required': """
Este recurso está disponível apenas para usuários premium.
Use /premium para conhecer os benefícios e ativar sua assinatura.
"""
    }
    
    @staticmethod
    def handle_premium_command(update, context):
        """
        Manipula o comando /premium para mostrar informações sobre o plano premium.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário já é premium
        user = UserRepository.get_user_by_id(user_id)
        if user and user['is_premium']:
            return PremiumHandler.MESSAGES['already_premium']
        
        # Retorna informações sobre o plano premium
        return PremiumHandler.MESSAGES['premium_info']
    
    @staticmethod
    def handle_ativar_premium_command(update, context):
        """
        Manipula o comando /ativar_premium para ativar o plano premium.
        
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
            return "Você precisa completar o cadastro inicial antes de ativar o premium. Use /iniciar para começar."
        
        # Verifica se o usuário já é premium
        if user['is_premium']:
            return PremiumHandler.MESSAGES['already_premium']
        
        # Ativa o plano premium
        # Em uma implementação real, aqui seria integrado com um sistema de pagamento
        UserRepository.set_user_premium_status(user_id, True)
        
        # Retorna mensagem de confirmação
        return PremiumHandler.MESSAGES['premium_activated']
    
    @staticmethod
    def handle_treino_command(update, context):
        """
        Manipula o comando /treino para fornecer planos de treino (recurso premium).
        
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
            return "Você precisa completar o cadastro inicial antes de acessar planos de treino. Use /iniciar para começar."
        
        # Verifica se o usuário é premium
        if not user['is_premium']:
            return PremiumHandler.MESSAGES['premium_required']
        
        # Obtém o objetivo do usuário
        goal = user['goal']
        
        # Retorna um plano de treino personalizado
        if goal == 'emagrecer':
            return """
🏋️‍♀️ Plano de Treino para Emagrecimento

Segunda-feira: Treino Cardiovascular
• 5 min de aquecimento
• 30 min de corrida intervalada (1 min intenso, 2 min moderado)
• 10 min de alongamento

Terça-feira: Treino de Força - Parte Superior
• 3 séries de 15 flexões
• 3 séries de 12 remadas com halteres
• 3 séries de 15 elevações laterais
• 3 séries de 12 tríceps no banco

Quarta-feira: Descanso Ativo
• 30 min de caminhada leve
• Alongamento completo

Quinta-feira: Treino HIIT
• 5 min de aquecimento
• 20 min de HIIT (30 seg de esforço máximo, 30 seg de descanso)
• 10 min de alongamento

Sexta-feira: Treino de Força - Parte Inferior
• 3 séries de 15 agachamentos
• 3 séries de 12 afundos
• 3 séries de 15 elevações de panturrilha
• 3 séries de 20 abdominais

Sábado: Treino Cardiovascular
• 45 min de atividade aeróbica de sua preferência

Domingo: Descanso Completo

💡 Dicas:
• Mantenha-se hidratado durante os treinos
• Combine com sua dieta de déficit calórico
• Aumente gradualmente a intensidade a cada semana
"""
        elif goal == 'ganhar_massa':
            return """
🏋️‍♀️ Plano de Treino para Ganho de Massa

Segunda-feira: Peito e Tríceps
• 4 séries de 8-10 supino reto
• 4 séries de 8-10 supino inclinado
• 3 séries de 10-12 crucifixo
• 4 séries de 8-10 tríceps na polia
• 3 séries de 10-12 tríceps francês

Terça-feira: Costas e Bíceps
• 4 séries de 8-10 puxada frontal
• 4 séries de 8-10 remada curvada
• 3 séries de 10-12 puxada alta
• 4 séries de 8-10 rosca direta
• 3 séries de 10-12 rosca martelo

Quarta-feira: Descanso ou Cardio Leve
• 20-30 min de cardio de baixa intensidade (opcional)

Quinta-feira: Pernas
• 4 séries de 8-10 agachamento
• 4 séries de 8-10 leg press
• 3 séries de 10-12 cadeira extensora
• 4 séries de 8-10 stiff
• 3 séries de 10-12 panturrilha em pé

Sexta-feira: Ombros e Abdômen
• 4 séries de 8-10 desenvolvimento militar
• 4 séries de 8-10 elevação lateral
• 3 séries de 10-12 elevação frontal
• 4 séries de 15-20 abdominais
• 3 séries de 15-20 prancha (30 segundos)

Sábado e Domingo: Descanso

💡 Dicas:
• Consuma proteína suficiente (1.6-2.2g/kg de peso)
• Alimente-se 1-2 horas antes do treino
• Priorize o descanso adequado entre os treinos
• Aumente gradualmente as cargas a cada semana
"""
        else:  # manter
            return """
🏋️‍♀️ Plano de Treino para Manutenção

Segunda-feira: Treino Completo
• 3 séries de 12 agachamentos
• 3 séries de 12 supino
• 3 séries de 12 remada
• 3 séries de 12 desenvolvimento de ombros
• 3 séries de 15 abdominais

Terça-feira: Cardio
• 5 min de aquecimento
• 30 min de cardio moderado (corrida, natação, ciclismo)
• 5 min de volta à calma

Quarta-feira: Treino Funcional
• Circuito de 3 voltas:
  - 15 burpees
  - 20 mountain climbers
  - 15 jumping jacks
  - 10 flexões
  - 30 seg de prancha
  - 1 min de descanso entre voltas

Quinta-feira: Descanso Ativo
• 30 min de caminhada ou yoga

Sexta-feira: Treino Completo
• 3 séries de 12 afundos
• 3 séries de 12 puxada
• 3 séries de 12 elevação lateral
• 3 séries de 12 tríceps
• 3 séries de 15 abdominais oblíquos

Sábado: Atividade Recreativa
• 45-60 min de atividade de sua preferência (esporte, dança, etc.)

Domingo: Descanso Completo

💡 Dicas:
• Mantenha a consistência nos treinos
• Varie as atividades para manter o interesse
• Ajuste a intensidade conforme necessário
• Equilibre treino e alimentação para manter o peso
"""
    
    @staticmethod
    def handle_nutricionista_command(update, context):
        """
        Manipula o comando /nutricionista para agendar consultas (recurso premium).
        
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
            return "Você precisa completar o cadastro inicial antes de agendar consultas. Use /iniciar para começar."
        
        # Verifica se o usuário é premium
        if not user['is_premium']:
            return PremiumHandler.MESSAGES['premium_required']
        
        # Em uma implementação real, aqui seria integrado com um sistema de agendamento
        return """
👨‍⚕️ Consulta com Nutricionista

Como assinante premium, você tem direito a uma consulta mensal com um de nossos nutricionistas parceiros.

Horários disponíveis:
• Segunda-feira: 9h às 17h
• Quarta-feira: 13h às 19h
• Sexta-feira: 8h às 16h

Para agendar, entre em contato com nossa central:
📞 (11) 9999-9999
📧 agendamento@nutribotevolve.com

Informe seu nome completo e número de usuário: {user_id}
""".format(user_id=user_id)
