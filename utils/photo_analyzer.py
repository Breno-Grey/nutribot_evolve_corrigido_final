"""
Utilitário para análise de fotos corporais para o NutriBot Evolve.
Responsável por processar e comparar fotos corporais.
"""

import sys
import os
import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
import config

class PhotoAnalyzer:
    """Classe para analisar e comparar fotos corporais."""
    
    def __init__(self):
        """Inicializa o analisador de fotos."""
        # Diretório para armazenar fotos
        self.photos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'photos')
        os.makedirs(self.photos_dir, exist_ok=True)
    
    def save_photo(self, photo_file, user_id):
        """
        Salva uma foto no sistema de arquivos.
        
        Args:
            photo_file: Objeto de arquivo da foto
            user_id (int): ID do usuário no Telegram
            
        Returns:
            str: Caminho para o arquivo salvo ou None em caso de erro
        """
        try:
            # Cria diretório específico para o usuário
            user_dir = os.path.join(self.photos_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Gera nome de arquivo único
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            file_path = os.path.join(user_dir, filename)
            
            # Salva o arquivo
            with open(file_path, 'wb') as f:
                f.write(photo_file.read())
            
            return file_path
        except Exception as e:
            print(f"Erro ao salvar foto: {e}")
            return None
    
    def analyze_photo(self, photo_path):
        """
        Realiza uma análise básica da foto.
        
        Args:
            photo_path (str): Caminho para o arquivo da foto
            
        Returns:
            dict: Resultados da análise
        """
        try:
            # Abre a imagem
            image = Image.open(photo_path)
            
            # Obtém dimensões
            width, height = image.size
            
            # Análise básica (simulada)
            # Em uma implementação real, aqui seria usado um modelo de visão computacional
            analysis = {
                'dimensions': {
                    'width': width,
                    'height': height
                },
                'quality': self._analyze_image_quality(image),
                'lighting': self._analyze_lighting(image),
                'framing': self._analyze_framing(image),
                'suggestions': self._generate_suggestions(image)
            }
            
            return analysis
        except Exception as e:
            print(f"Erro ao analisar foto: {e}")
            return None
    
    def _analyze_image_quality(self, image):
        """
        Analisa a qualidade da imagem.
        
        Args:
            image: Objeto de imagem PIL
            
        Returns:
            dict: Resultados da análise de qualidade
        """
        # Em uma implementação real, aqui seria feita uma análise mais sofisticada
        width, height = image.size
        
        # Verifica resolução
        if width < 500 or height < 500:
            quality = "baixa"
            message = "A resolução da imagem é baixa, o que pode dificultar a análise."
        elif width < 1000 or height < 1000:
            quality = "média"
            message = "A resolução da imagem é média, adequada para análise básica."
        else:
            quality = "alta"
            message = "A resolução da imagem é boa, ideal para análise detalhada."
        
        return {
            'level': quality,
            'message': message
        }
    
    def _analyze_lighting(self, image):
        """
        Analisa a iluminação da imagem.
        
        Args:
            image: Objeto de imagem PIL
            
        Returns:
            dict: Resultados da análise de iluminação
        """
        # Em uma implementação real, aqui seria feita uma análise mais sofisticada
        # Simulação simples de análise de brilho
        try:
            # Converte para escala de cinza
            gray_image = image.convert('L')
            
            # Calcula brilho médio
            histogram = gray_image.histogram()
            pixels = sum(histogram)
            brightness = sum(i * histogram[i] for i in range(256)) / pixels
            
            if brightness < 80:
                lighting = "escura"
                message = "A imagem está um pouco escura, o que pode dificultar a visualização de detalhes."
            elif brightness > 180:
                lighting = "clara"
                message = "A imagem está muito clara, o que pode ocultar alguns contornos."
            else:
                lighting = "boa"
                message = "A iluminação da imagem é adequada para análise."
            
            return {
                'level': lighting,
                'message': message
            }
        except:
            # Fallback em caso de erro
            return {
                'level': "indefinida",
                'message': "Não foi possível analisar a iluminação da imagem."
            }
    
    def _analyze_framing(self, image):
        """
        Analisa o enquadramento da imagem.
        
        Args:
            image: Objeto de imagem PIL
            
        Returns:
            dict: Resultados da análise de enquadramento
        """
        # Em uma implementação real, aqui seria usado um modelo para detectar a pessoa na imagem
        # Simulação simples
        width, height = image.size
        aspect_ratio = width / height
        
        if aspect_ratio < 0.5 or aspect_ratio > 2:
            framing = "inadequado"
            message = "O enquadramento da imagem não é ideal para análise corporal."
        else:
            framing = "adequado"
            message = "O enquadramento da imagem é adequado para análise."
        
        return {
            'level': framing,
            'message': message
        }
    
    def _generate_suggestions(self, image):
        """
        Gera sugestões para melhorar a foto.
        
        Args:
            image: Objeto de imagem PIL
            
        Returns:
            list: Lista de sugestões
        """
        suggestions = []
        
        # Sugestões de iluminação
        lighting = self._analyze_lighting(image)
        if lighting['level'] == "escura":
            suggestions.append("Tire a foto em um ambiente mais iluminado ou use iluminação adicional.")
        elif lighting['level'] == "clara":
            suggestions.append("Evite luz direta ou muito intensa. Prefira iluminação difusa.")
        
        # Sugestões de enquadramento
        framing = self._analyze_framing(image)
        if framing['level'] == "inadequado":
            suggestions.append("Mantenha a câmera a aproximadamente 2 metros de distância e enquadre todo o corpo.")
        
        # Sugestões gerais
        suggestions.append("Use roupas justas ou de academia para melhor visualização da silhueta.")
        suggestions.append("Mantenha a mesma posição e ângulo em fotos futuras para facilitar a comparação.")
        suggestions.append("Tire fotos de frente, perfil e costas para uma análise mais completa.")
        
        return suggestions
    
    def compare_photos(self, current_photo_path, previous_photo_path):
        """
        Compara duas fotos corporais.
        
        Args:
            current_photo_path (str): Caminho para a foto atual
            previous_photo_path (str): Caminho para a foto anterior
            
        Returns:
            dict: Resultados da comparação
        """
        try:
            # Em uma implementação real, aqui seria usado um modelo de visão computacional
            # para detectar diferenças reais entre as fotos
            
            # Simulação de análise comparativa
            comparison = {
                'changes_detected': True,
                'observations': self._generate_comparison_observations(),
                'progress': self._generate_progress_assessment()
            }
            
            return comparison
        except Exception as e:
            print(f"Erro ao comparar fotos: {e}")
            return None
    
    def _generate_comparison_observations(self):
        """
        Gera observações simuladas para comparação de fotos.
        
        Returns:
            list: Lista de observações
        """
        # Em uma implementação real, estas observações seriam baseadas em análise real
        # Aqui estamos apenas simulando para demonstração
        observations = [
            "Redução na área do abdômen",
            "Melhora na postura",
            "Contornos mais definidos nos braços",
            "Ombros mais alinhados",
            "Cintura mais definida",
            "Quadril mais proporcional",
            "Pernas mais tonificadas",
            "Redução de volume nas costas"
        ]
        
        # Seleciona algumas observações aleatoriamente
        num_observations = random.randint(2, 4)
        selected_observations = random.sample(observations, num_observations)
        
        return selected_observations
    
    def _generate_progress_assessment(self):
        """
        Gera uma avaliação simulada de progresso.
        
        Returns:
            dict: Avaliação de progresso
        """
        # Em uma implementação real, esta avaliação seria baseada em métricas reais
        # Aqui estamos apenas simulando para demonstração
        progress_levels = ["leve", "moderado", "significativo"]
        selected_level = random.choice(progress_levels)
        
        messages = {
            "leve": "Notamos mudanças leves desde a última foto. Continue com seu plano alimentar!",
            "moderado": "Há progresso moderado visível desde a última foto. Seu esforço está dando resultados!",
            "significativo": "Parabéns! Há mudanças significativas desde a última foto. Seu compromisso está gerando resultados excelentes!"
        }
        
        return {
            'level': selected_level,
            'message': messages[selected_level]
        }
    
    def create_comparison_image(self, current_photo_path, previous_photo_path, user_id):
        """
        Cria uma imagem de comparação entre duas fotos.
        
        Args:
            current_photo_path (str): Caminho para a foto atual
            previous_photo_path (str): Caminho para a foto anterior
            user_id (int): ID do usuário no Telegram
            
        Returns:
            str: Caminho para a imagem de comparação ou None em caso de erro
        """
        try:
            # Abre as imagens
            current_image = Image.open(current_photo_path)
            previous_image = Image.open(previous_photo_path)
            
            # Redimensiona as imagens para o mesmo tamanho
            max_width = 800
            max_height = 600
            
            current_image.thumbnail((max_width, max_height))
            previous_image.thumbnail((max_width, max_height))
            
            # Cria uma nova imagem para a comparação
            comparison_width = current_image.width * 2 + 20  # Espaço entre as imagens
            comparison_height = max(current_image.height, previous_image.height) + 60  # Espaço para texto
            comparison_image = Image.new('RGB', (comparison_width, comparison_height), (255, 255, 255))
            
            # Adiciona as imagens
            comparison_image.paste(previous_image, (0, 30))
            comparison_image.paste(current_image, (previous_image.width + 20, 30))
            
            # Adiciona texto
            draw = ImageDraw.Draw(comparison_image)
            
            # Tenta usar uma fonte, ou usa a fonte padrão se não disponível
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((10, 5), "Antes", fill=(0, 0, 0), font=font)
            draw.text((previous_image.width + 30, 5), "Depois", fill=(0, 0, 0), font=font)
            
            # Salva a imagem de comparação
            user_dir = os.path.join(self.photos_dir, str(user_id))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            comparison_filename = f"comparison_{timestamp}.jpg"
            comparison_path = os.path.join(user_dir, comparison_filename)
            
            comparison_image.save(comparison_path)
            
            return comparison_path
        except Exception as e:
            print(f"Erro ao criar imagem de comparação: {e}")
            return None
    
    def generate_photo_tips(self):
        """
        Gera dicas para tirar melhores fotos corporais.
        
        Returns:
            list: Lista de dicas
        """
        tips = [
            "Tire as fotos sempre no mesmo local, com iluminação semelhante.",
            "Mantenha a mesma distância da câmera em todas as fotos.",
            "Use roupas justas ou de academia para melhor visualização da silhueta.",
            "Tire fotos de frente, perfil e costas para uma análise mais completa.",
            "Mantenha uma postura natural, com os braços relaxados ao lado do corpo.",
            "Evite usar filtros ou editar as fotos para não comprometer a análise.",
            "Prefira luz natural, mas evite luz direta do sol que pode criar sombras fortes.",
            "Use um tripé ou apoio para a câmera para manter o mesmo ângulo.",
            "Tire as fotos em um fundo neutro e sem distrações.",
            "Mantenha a mesma expressão facial em todas as fotos."
        ]
        
        return tips
