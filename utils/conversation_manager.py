"""
Gerenciador de estados de conversação para o NutriBot Evolve.
Responsável por controlar o fluxo de onboarding e outras conversações.
"""

import sys
import json
import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from database.db_manager import db_manager

class ConversationManager:
    """Classe para gerenciar estados de conversação."""
    
    # Estados de conversação para o onboarding
    STATES = {
        'INITIAL': 'initial',
        'WAITING_NAME': 'waiting_name',
        'WAITING_AGE': 'waiting_age',
        'WAITING_GENDER': 'waiting_gender',
        'WAITING_WEIGHT': 'waiting_weight',
        'WAITING_HEIGHT': 'waiting_height',
        'WAITING_ACTIVITY': 'waiting_activity',
        'WAITING_GOAL': 'waiting_goal',
        'WAITING_DIET_TYPE': 'waiting_diet_type',
        'COMPLETED': 'completed'
    }
    
    @staticmethod
    def get_state(user_id):
        """
        Obtém o estado atual da conversação de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            dict: Estado atual e contexto ou None se não existir
        """
        query = "SELECT * FROM conversation_states WHERE user_id = ?"
        result = db_manager.fetch_one(query, (user_id,))
        
        if result:
            # Converte o contexto de JSON para dicionário
            context = json.loads(result['context']) if result['context'] else {}
            return {
                'state': result['state'],
                'context': context
            }
        return None
    
    @staticmethod
    def set_state(user_id, state, context=None):
        """
        Define o estado da conversação de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            state (str): Novo estado
            context (dict, optional): Contexto adicional
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        now = datetime.datetime.now()
        
        # Converte o contexto para JSON
        context_json = json.dumps(context) if context else None
        
        # Verifica se o usuário já tem um estado
        current_state = ConversationManager.get_state(user_id)
        
        if current_state:
            # Atualiza o estado existente
            data = {
                'state': state,
                'context': context_json,
                'updated_at': now
            }
            condition = {'user_id': user_id}
            rows_updated = db_manager.update('conversation_states', data, condition)
            return rows_updated > 0
        else:
            # Cria um novo estado
            data = {
                'user_id': user_id,
                'state': state,
                'context': context_json,
                'updated_at': now
            }
            result = db_manager.insert('conversation_states', data)
            return result is not None
    
    @staticmethod
    def update_context(user_id, new_context_data):
        """
        Atualiza o contexto da conversação de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            new_context_data (dict): Novos dados de contexto
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        current_state = ConversationManager.get_state(user_id)
        
        if not current_state:
            return False
        
        # Mescla o contexto atual com os novos dados
        context = current_state['context'] or {}
        context.update(new_context_data)
        
        # Atualiza o estado com o novo contexto
        return ConversationManager.set_state(user_id, current_state['state'], context)
    
    @staticmethod
    def clear_state(user_id):
        """
        Remove o estado de conversação de um usuário.
        
        Args:
            user_id (int): ID do usuário no Telegram
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        condition = {'user_id': user_id}
        rows_deleted = db_manager.delete('conversation_states', condition)
        return rows_deleted > 0
    
    @staticmethod
    def get_next_onboarding_state(current_state):
        """
        Retorna o próximo estado de onboarding com base no estado atual.
        
        Args:
            current_state (str): Estado atual
            
        Returns:
            str: Próximo estado
        """
        states_sequence = [
            ConversationManager.STATES['INITIAL'],
            ConversationManager.STATES['WAITING_NAME'],
            ConversationManager.STATES['WAITING_AGE'],
            ConversationManager.STATES['WAITING_GENDER'],
            ConversationManager.STATES['WAITING_WEIGHT'],
            ConversationManager.STATES['WAITING_HEIGHT'],
            ConversationManager.STATES['WAITING_ACTIVITY'],
            ConversationManager.STATES['WAITING_GOAL'],
            ConversationManager.STATES['WAITING_DIET_TYPE'],
            ConversationManager.STATES['COMPLETED']
        ]
        
        try:
            current_index = states_sequence.index(current_state)
            if current_index < len(states_sequence) - 1:
                return states_sequence[current_index + 1]
            else:
                return ConversationManager.STATES['COMPLETED']
        except ValueError:
            # Se o estado atual não estiver na sequência, retorna o estado inicial
            return ConversationManager.STATES['INITIAL']
