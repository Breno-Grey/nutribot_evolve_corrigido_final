"""
Arquivo principal do NutriBot Evolve.
Ponto de entrada da aplicação.
"""

import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula o comando /start."""
    response = OnboardingHandler.handle_start(update, context)
    await update.message.reply_text(response)

async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula o comando /iniciar para começar o onboarding."""
    response = OnboardingHandler.handle_iniciar(update, context)
    await update.message.reply_text(response)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula o comando /ajuda."""
    await update.message.reply_text(config.HELP_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula mensagens de texto."""
    user_id = update.effective_user.id
    
    # Verifica se o usuário está em processo de onboarding
    conversation = ConversationManager.get_state(user_id)
    
    if conversation and conversation['state'] != ConversationManager.STATES['COMPLETED']:
        # Usuário está em processo de onboarding
        response = OnboardingHandler.handle_message(update, context)
        if response:
            await update.message.reply_text(response)
        return
    
    # Aqui serão implementados os manipuladores para outras funcionalidades
    # como registro de refeições, análise de fotos, etc.
    
    # Mensagem temporária para funcionalidades não implementadas
    await update.message.reply_text(
        "Esta funcionalidade ainda será implementada. "
        "Use /ajuda para ver os comandos disponíveis."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manipula erros."""
    logger.error(f"Erro: {context.error} - Update: {update}")
    
    # Envia mensagem de erro para o usuário
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente."
        )

def main():
    """Função principal."""
    # Inicializa o banco de dados
    db_manager.initialize_database()
    
    # Cria a aplicação
    application = Application.builder().token(config.TOKEN).build()
    
    # Adiciona manipuladores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("iniciar", iniciar))
    application.add_handler(CommandHandler("ajuda", ajuda))
    
    # Adiciona manipulador de mensagens
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Adiciona manipulador de erros
    application.add_error_handler(error_handler)
    
    # Inicia o bot
    application.run_polling()
    
    logger.info("Bot iniciado!")

if __name__ == "__main__":
    main()
