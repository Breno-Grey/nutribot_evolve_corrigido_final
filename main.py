"""
Arquivo principal do NutriBot Evolve (versão compatível com python-telegram-bot 13.7).
Ponto de entrada da aplicação.
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

import config
from database.db_manager import db_manager
from database.user_repository import UserRepository
from utils.conversation_manager import ConversationManager
from handlers.onboarding_handler import OnboardingHandler

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    """Manipula o comando /start."""
    response = OnboardingHandler.handle_start(update, context)
    update.message.reply_text(response)

def iniciar(update: Update, context: CallbackContext):
    """Manipula o comando /iniciar para começar o onboarding."""
    response = OnboardingHandler.handle_iniciar(update, context)
    update.message.reply_text(response)

def ajuda(update: Update, context: CallbackContext):
    """Manipula o comando /ajuda."""
    update.message.reply_text(config.HELP_MESSAGE)

def handle_message(update: Update, context: CallbackContext):
    """Manipula mensagens de texto."""
    user_id = update.effective_user.id
    
    # Verifica se o usuário está em processo de onboarding
    conversation = ConversationManager.get_state(user_id)
    
    if conversation and conversation['state'] != ConversationManager.STATES['COMPLETED']:
        # Usuário está em processo de onboarding
        response = OnboardingHandler.handle_message(update, context)
        if response:
            update.message.reply_text(response)
        return
    
    # Aqui serão implementados os manipuladores para outras funcionalidades
    # como registro de refeições, análise de fotos, etc.
    
    # Mensagem temporária para funcionalidades não implementadas
    update.message.reply_text(
        "Esta funcionalidade ainda será implementada. "
        "Use /ajuda para ver os comandos disponíveis."
    )

def error_handler(update: Update, context: CallbackContext):
    """Manipula erros."""
    logger.error(f"Erro: {context.error} - Update: {update}")
    
    # Envia mensagem de erro para o usuário
    if update and update.effective_message:
        update.effective_message.reply_text(
            "Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente."
        )

def main():
    """Função principal."""
    # Inicializa o banco de dados
    db_manager.initialize_database()
    
    # Cria o updater e o dispatcher
    updater = Updater(token=config.TOKEN)
    dispatcher = updater.dispatcher
    
    # Adiciona manipuladores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("iniciar", iniciar))
    dispatcher.add_handler(CommandHandler("ajuda", ajuda))
    
    # Adiciona manipulador de mensagens
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Adiciona manipulador de erros
    dispatcher.add_error_handler(error_handler)
    
    # Inicia o bot
    updater.start_polling()
    updater.idle()
    
    logger.info("Bot iniciado!")

if __name__ == "__main__":
    main()
