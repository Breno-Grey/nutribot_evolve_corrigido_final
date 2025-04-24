"""
Manipulador de relatórios para o NutriBot Evolve.
Responsável por gerenciar a geração e envio de relatórios.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.user_repository import UserRepository
from utils.report_generator import ReportGenerator

class ReportHandler:
    """Classe para gerenciar a geração e envio de relatórios."""
    
    # Mensagens para interação com o usuário
    MESSAGES = {
        'weekly_report': """
📊 Relatório Semanal

Período: {start_date} a {end_date}

📈 Consumo Calórico:
• Calorias totais: {total_calories} kcal
• Média diária: {avg_calories} kcal
• Meta diária: {target_calories} kcal
• Dias acima da meta: {days_over_target}
• Dias abaixo da meta: {days_under_target}

🍽️ Macronutrientes (média diária):
• Proteínas: {avg_protein}g
• Carboidratos: {avg_carbs}g
• Gorduras: {avg_fat}g

💡 Insights:
{insights}

Os gráficos do seu relatório serão enviados em seguida.
""",
        'monthly_report': """
📊 Relatório Mensal (Premium)

Período: {start_date} a {end_date}

📈 Consumo Calórico:
• Calorias totais: {total_calories} kcal
• Média diária: {avg_calories} kcal
• Meta diária: {target_calories} kcal
• Dias acima da meta: {days_over_target}
• Dias abaixo da meta: {days_under_target}

🍽️ Macronutrientes (média diária):
• Proteínas: {avg_protein}g
• Carboidratos: {avg_carbs}g
• Gorduras: {avg_fat}g

💡 Insights:
{insights}

Os gráficos do seu relatório serão enviados em seguida.
""",
        'no_data': """
Não há dados suficientes para gerar um relatório.
Continue registrando suas refeições diariamente para receber relatórios detalhados.
""",
        'premium_required': """
Este recurso está disponível apenas para usuários premium.
Use /premium para conhecer os benefícios e ativar sua assinatura.
"""
    }
    
    def __init__(self):
        """Inicializa o manipulador de relatórios."""
        self.report_generator = ReportGenerator()
    
    def handle_relatorio_command(self, update, context):
        """
        Manipula o comando /relatorio para gerar um relatório semanal.
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            tuple: (Mensagem de resposta, Lista de caminhos para arquivos de gráficos)
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário completou o onboarding
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['onboarding_complete']:
            return "Você precisa completar o cadastro inicial antes de gerar relatórios. Use /iniciar para começar.", []
        
        # Gera o relatório semanal
        report = self.report_generator.generate_weekly_report(user_id)
        
        if not report:
            return ReportHandler.MESSAGES['no_data'], []
        
        # Prepara o texto de insights
        insights_text = ""
        for insight in report['insights']:
            insights_text += f"• {insight}\n"
        
        # Prepara a mensagem do relatório
        message = ReportHandler.MESSAGES['weekly_report'].format(
            start_date=report['period']['start_date'],
            end_date=report['period']['end_date'],
            total_calories=report['calorie_data']['stats']['total_calories'],
            avg_calories=report['calorie_data']['stats']['avg_calories'],
            target_calories=report['calorie_data']['stats']['target_calories'],
            days_over_target=report['calorie_data']['stats']['days_over_target'],
            days_under_target=report['calorie_data']['stats']['days_under_target'],
            avg_protein=report['macro_data']['stats']['avg_protein'],
            avg_carbs=report['macro_data']['stats']['avg_carbs'],
            avg_fat=report['macro_data']['stats']['avg_fat'],
            insights=insights_text
        )
        
        # Prepara os caminhos para os gráficos
        chart_paths = [
            report['charts']['calorie_chart'],
            report['charts']['macro_chart']
        ]
        
        return message, chart_paths
    
    def handle_relatorio_mensal_command(self, update, context):
        """
        Manipula o comando /relatorio_mensal para gerar um relatório mensal (premium).
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            tuple: (Mensagem de resposta, Lista de caminhos para arquivos de gráficos)
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário completou o onboarding
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['onboarding_complete']:
            return "Você precisa completar o cadastro inicial antes de gerar relatórios. Use /iniciar para começar.", []
        
        # Verifica se o usuário é premium
        if not user['is_premium']:
            return ReportHandler.MESSAGES['premium_required'], []
        
        # Gera o relatório mensal
        report = self.report_generator.generate_monthly_report(user_id)
        
        if not report:
            return ReportHandler.MESSAGES['no_data'], []
        
        # Prepara o texto de insights
        insights_text = ""
        for insight in report['insights']:
            insights_text += f"• {insight}\n"
        
        # Prepara a mensagem do relatório
        message = ReportHandler.MESSAGES['monthly_report'].format(
            start_date=report['period']['start_date'],
            end_date=report['period']['end_date'],
            total_calories=report['calorie_data']['stats']['total_calories'],
            avg_calories=report['calorie_data']['stats']['avg_calories'],
            target_calories=report['calorie_data']['stats']['target_calories'],
            days_over_target=report['calorie_data']['stats']['days_over_target'],
            days_under_target=report['calorie_data']['stats']['days_under_target'],
            avg_protein=report['macro_data']['stats']['avg_protein'],
            avg_carbs=report['macro_data']['stats']['avg_carbs'],
            avg_fat=report['macro_data']['stats']['avg_fat'],
            insights=insights_text
        )
        
        # Prepara os caminhos para os gráficos
        chart_paths = [
            report['charts']['calorie_chart'],
            report['charts']['macro_chart']
        ]
        
        # Gera o PDF (recurso premium)
        pdf_path = self.report_generator.generate_pdf_report(user_id, report)
        if pdf_path:
            chart_paths.append(pdf_path)
        
        return message, chart_paths
    
    def handle_exportar_command(self, update, context):
        """
        Manipula o comando /exportar para exportar relatórios em PDF (premium).
        
        Args:
            update: Objeto de atualização do Telegram
            context: Contexto do Telegram
            
        Returns:
            tuple: (Mensagem de resposta, Lista de caminhos para arquivos)
        """
        user_id = update.effective_user.id
        
        # Verifica se o usuário completou o onboarding
        user = UserRepository.get_user_by_id(user_id)
        if not user or not user['onboarding_complete']:
            return "Você precisa completar o cadastro inicial antes de exportar relatórios. Use /iniciar para começar.", []
        
        # Verifica se o usuário é premium
        if not user['is_premium']:
            return ReportHandler.MESSAGES['premium_required'], []
        
        # Gera o relatório semanal
        report = self.report_generator.generate_weekly_report(user_id)
        
        if not report:
            return ReportHandler.MESSAGES['no_data'], []
        
        # Gera o PDF
        pdf_path = self.report_generator.generate_pdf_report(user_id, report)
        
        if not pdf_path:
            return "Não foi possível gerar o PDF do relatório. Por favor, tente novamente.", []
        
        return "Seu relatório em PDF foi gerado com sucesso e será enviado em seguida.", [pdf_path]
