"""
Manipulador de fotos para o NutriBot Evolve.
Responsável por gerenciar o envio e análise de fotos corporais.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from database.photo_repository import PhotoRepository
from utils.photo_analyzer import PhotoAnalyzer
from utils.conversation_manager import ConversationManager

class PhotoHandler:
    """Classe para gerenciar o envio e análise de fotos corporais."""
    
    # Estados de conversação para envio de fotos
    STATES = {
        'WAITING_PHOTO': 'waiting_photo',
        'WAITING_DESCRIPTION': 'waiting_description',
        'COMPLETED': 'completed'
    }
    
    # Mensagens para interação com o usuário
    MESSAGES = {
        'ask_photo': """
Por favor, envie uma foto corporal para acompanhamento.

📸 Dicas para tirar uma boa foto:
• Use roupas justas ou de academia
• Mantenha a mesma posição em todas as fotos
• Tire a foto em um local bem iluminado
• Mantenha uma distância de aproximadamente 2 metros da câmera
• Prefira um fundo neutro e sem distrações

Sua privacidade é nossa prioridade! As fotos são armazenadas de forma segura e só você tem acesso a elas.
""",
        'ask_description': """
Foto recebida! 📸

Gostaria de adicionar alguma descrição ou observação para esta foto?
Por exemplo: "Início da dieta", "Após 1 mês", "Peso atual: 70kg", etc.

Ou envie "pular" se não quiser adicionar uma descrição.
""",
        'photo_registered': """
✅ Foto registrada com sucesso!

📊 Análise da imagem:
• Qualidade: {quality_level}
• Iluminação: {lighting_level}
• Enquadramento: {framing_level}

💡 {quality_message}
💡 {lighting_message}
💡 {framing_message}

{comparison_text}

📝 Sugestões para próximas fotos:
{suggestions}

Use /fotos para ver suas fotos anteriores e acompanhar seu progresso.
""",
        'comparison_text': """
📊 Comparação com foto anterior:

{observations}

{progress_message}
""",
        'no_comparison': "Esta é sua primeira foto! Envie mais fotos no futuro para acompanhar seu progresso.",
        'photo_list': """
📸 Suas fotos registradas:

{photo_list}

Para ver uma comparação entre duas fotos, use o comando /comparar seguido dos números das fotos.
Exemplo: /comparar 1 3
""",
        'no_photos': "Você ainda não tem fotos registradas. Use /foto para enviar sua primeira foto!",
        'photo_tips': """
📸 Dicas para tirar melhores fotos corporais:

{tips}

Use /foto para enviar uma nova foto seguindo estas dicas!
"""
    }
    
    def __init__(self):
        """Inicializa o manipulador de fotos."""
        self.photo_analyzer = PhotoAnalyzer()
    
    def handle_foto_command(self, update, context):
        """
        Manipula o comando /foto para iniciar o envio de uma foto.
        
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
            return "Você precisa completar o cadastro inicial antes de enviar fotos. Use /iniciar para começar."
        
        # Inicia o processo de envio de foto
        ConversationManager.set_state(user_id, PhotoHandler.STATES['WAITING_PHOTO'])
        
        # Retorna a mensagem solicitando a foto
        return PhotoHandler.MESSAGES['ask_photo']
    
    def handle_fotos_command(self, update, context):
        """
        Manipula o comando /fotos para listar as fotos do usuário.
        
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
            return "Você precisa completar o cadastro inicial antes de acessar suas fotos. Use /iniciar para começar."
        
        # Obtém as fotos do usuário
        photos = PhotoRepository.get_photos_by_user(user_id)
        
        if not photos:
            return PhotoHandler.MESSAGES['no_photos']
        
        # Prepara a lista de fotos
        photo_list = ""
        for i, photo in enumerate(photos):
            date_str = photo['photo_date'].strftime('%d/%m/%Y') if isinstance(photo['photo_date'], datetime.date) else photo['photo_date']
            description = f" - {photo['description']}" if photo['description'] else ""
            photo_list += f"{i+1}. Foto de {date_str}{description}\n"
        
        # Retorna a mensagem com a lista de fotos
        return PhotoHandler.MESSAGES['photo_list'].format(
            photo_list=photo_list
        )
    
    def handle_comparar_command(self, update, context):
        """
        Manipula o comando /comparar para comparar duas fotos.
        
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
            return "Você precisa completar o cadastro inicial antes de comparar fotos. Use /iniciar para começar."
        
        # Verifica se foram fornecidos os índices das fotos
        if not context.args or len(context.args) < 2:
            return "Por favor, forneça os números das duas fotos que deseja comparar. Exemplo: /comparar 1 3"
        
        try:
            # Obtém os índices das fotos
            index1 = int(context.args[0]) - 1
            index2 = int(context.args[1]) - 1
            
            # Obtém as fotos do usuário
            photos = PhotoRepository.get_photos_by_user(user_id)
            
            if not photos or len(photos) < 2:
                return "Você precisa ter pelo menos duas fotos registradas para fazer uma comparação."
            
            if index1 < 0 or index1 >= len(photos) or index2 < 0 or index2 >= len(photos):
                return f"Índices inválidos. Você tem {len(photos)} fotos registradas (1 a {len(photos)})."
            
            # Obtém os caminhos das fotos
            photo1_path = photos[index1]['photo_path']
            photo2_path = photos[index2]['photo_path']
            
            # Cria a imagem de comparação
            comparison_path = self.photo_analyzer.create_comparison_image(photo2_path, photo1_path, user_id)
            
            if not comparison_path:
                return "Não foi possível criar a comparação entre as fotos. Por favor, tente novamente."
            
            # Realiza a comparação
            comparison = self.photo_analyzer.compare_photos(photo2_path, photo1_path)
            
            # Prepara o texto de observações
            observations_text = ""
            for obs in comparison['observations']:
                observations_text += f"• {obs}\n"
            
            # Retorna a mensagem com a comparação
            return f"""
📊 Comparação entre as fotos {index1+1} e {index2+1}:

Observações:
{observations_text}

{comparison['progress']['message']}

A imagem de comparação será enviada em seguida.
""", comparison_path
            
        except ValueError:
            return "Por favor, forneça números válidos para as fotos. Exemplo: /comparar 1 3"
        except Exception as e:
            print(f"Erro ao comparar fotos: {e}")
            return "Ocorreu um erro ao comparar as fotos. Por favor, tente novamente."
    
    def handle_dicas_foto_command(self, update, context):
        """
        Manipula o comando /dicas_foto para mostrar dicas para tirar fotos.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta
        """
        # Obtém as dicas
        tips = self.photo_analyzer.generate_photo_tips()
        
        # Prepara o texto de dicas
        tips_text = ""
        for i, tip in enumerate(tips):
            tips_text += f"{i+1}. {tip}\n"
        
        # Retorna a mensagem com as dicas
        return PhotoHandler.MESSAGES['photo_tips'].format(
            tips=tips_text
        )
    
    def handle_photo_message(self, update, context):
        """
        Manipula o recebimento de uma foto.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta ou None se não estiver esperando uma foto
        """
        user_id = update.effective_user.id
        
        # Obtém o estado atual da conversação
        conversation = ConversationManager.get_state(user_id)
        
        if not conversation or conversation['state'] != PhotoHandler.STATES['WAITING_PHOTO']:
            # Usuário não está em processo de envio de foto
            return None
        
        # Obtém a foto
        photo = update.message.photo[-1]  # Pega a versão de maior resolução
        
        # Baixa a foto
        photo_file = context.bot.get_file(photo.file_id)
        
        # Salva a foto
        photo_path = self.photo_analyzer.save_photo(photo_file, user_id)
        
        if not photo_path:
            return "Ocorreu um erro ao salvar a foto. Por favor, tente novamente."
        
        # Atualiza o contexto com o caminho da foto
        ConversationManager.update_context(user_id, {'photo_path': photo_path})
        
        # Avança para o próximo estado
        ConversationManager.set_state(user_id, PhotoHandler.STATES['WAITING_DESCRIPTION'])
        
        # Retorna a mensagem solicitando a descrição
        return PhotoHandler.MESSAGES['ask_description']
    
    def handle_description_message(self, update, context):
        """
        Manipula o recebimento de uma descrição para a foto.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            str: Mensagem de resposta ou None se não estiver esperando uma descrição
        """
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Obtém o estado atual da conversação
        conversation = ConversationManager.get_state(user_id)
        
        if not conversation or conversation['state'] != PhotoHandler.STATES['WAITING_DESCRIPTION']:
            # Usuário não está em processo de envio de descrição
            return None
        
        # Obtém o caminho da foto do contexto
        photo_path = conversation['context'].get('photo_path')
        
        if not photo_path:
            return "Ocorreu um erro ao processar a foto. Por favor, tente novamente."
        
        # Define a descrição
        description = None if message_text.lower() == 'pular' else message_text
        
        # Registra a foto no banco de dados
        PhotoRepository.add_photo(user_id, photo_path, description)
        
        # Analisa a foto
        analysis = self.photo_analyzer.analyze_photo(photo_path)
        
        if not analysis:
            return "Ocorreu um erro ao analisar a foto. A foto foi salva, mas não foi possível gerar uma análise."
        
        # Prepara o texto de sugestões
        suggestions_text = ""
        for i, suggestion in enumerate(analysis['suggestions'][:3]):  # Limita a 3 sugestões
            suggestions_text += f"• {suggestion}\n"
        
        # Verifica se há fotos anteriores para comparação
        photos = PhotoRepository.get_photos_by_user(user_id)
        
        comparison_text = PhotoHandler.MESSAGES['no_comparison']
        
        if len(photos) > 1:
            # A foto atual já está na lista, então a anterior é a segunda
            previous_photo = photos[1]
            
            # Realiza a comparação
            comparison = self.photo_analyzer.compare_photos(photo_path, previous_photo['photo_path'])
            
            if comparison:
                # Prepara o texto de observações
                observations_text = ""
                for obs in comparison['observations']:
                    observations_text += f"• {obs}\n"
                
                # Atualiza o texto de comparação
                comparison_text = PhotoHandler.MESSAGES['comparison_text'].format(
                    observations=observations_text,
                    progress_message=comparison['progress']['message']
                )
        
        # Finaliza o estado de conversação
        ConversationManager.set_state(user_id, PhotoHandler.STATES['COMPLETED'])
        
        # Retorna a mensagem de confirmação
        return PhotoHandler.MESSAGES['photo_registered'].format(
            quality_level=analysis['quality']['level'].capitalize(),
            lighting_level=analysis['lighting']['level'].capitalize(),
            framing_level=analysis['framing']['level'].capitalize(),
            quality_message=analysis['quality']['message'],
            lighting_message=analysis['lighting']['message'],
            framing_message=analysis['framing']['message'],
            comparison_text=comparison_text,
            suggestions=suggestions_text
        )
