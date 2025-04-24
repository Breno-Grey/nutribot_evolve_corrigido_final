"""
Utilitário para sugestões de refeições para o NutriBot Evolve.
Responsável por gerar sugestões personalizadas de refeições.
"""

import sys
import json
import os
import random
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
import config

class MealSuggester:
    """Classe para gerar sugestões de refeições personalizadas."""
    
    def __init__(self):
        """Inicializa o sugestor de refeições."""
        # Carrega o banco de sugestões de refeições
        self.suggestions_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                               'resources', 'meal_suggestions.json')
        self.suggestions_database = self._load_suggestions_database()
        
        # Carrega o banco de mensagens motivacionais
        self.motivation_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                              'resources', 'motivation_messages.json')
        self.motivation_database = self._load_motivation_database()
    
    def _load_suggestions_database(self):
        """
        Carrega o banco de sugestões de refeições.
        
        Returns:
            dict: Banco de sugestões de refeições
        """
        # Verifica se o arquivo existe
        if not os.path.exists(self.suggestions_db_path):
            # Cria um banco de sugestões básico se não existir
            self._create_basic_suggestions_database()
        
        try:
            with open(self.suggestions_db_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Erro ao carregar banco de sugestões de refeições: {e}")
            return {}
    
    def _create_basic_suggestions_database(self):
        """Cria um banco de sugestões básico de refeições."""
        # Diretório de recursos
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        
        # Banco de sugestões básico de refeições
        basic_suggestions_db = {
            "flexivel": {
                "cafe_da_manha": [
                    {
                        "nome": "Café da manhã equilibrado",
                        "descricao": "2 fatias de pão integral com 2 ovos mexidos, 1 fatia de queijo branco e 1 maçã",
                        "calorias": 450,
                        "proteinas": 25,
                        "carboidratos": 45,
                        "gorduras": 18,
                        "receita": "Prepare os ovos mexidos em uma frigideira antiaderente. Torre o pão e monte o sanduíche com o queijo. Acompanhe com a maçã."
                    },
                    {
                        "nome": "Iogurte com frutas e granola",
                        "descricao": "1 pote de iogurte natural, 1 banana, 100g de morango e 30g de granola",
                        "calorias": 350,
                        "proteinas": 15,
                        "carboidratos": 60,
                        "gorduras": 8,
                        "receita": "Em uma tigela, coloque o iogurte, adicione as frutas picadas e finalize com a granola por cima."
                    }
                ],
                "almoco": [
                    {
                        "nome": "Prato colorido",
                        "descricao": "150g de frango grelhado, 100g de arroz integral, 50g de feijão e salada de folhas verdes com tomate",
                        "calorias": 500,
                        "proteinas": 40,
                        "carboidratos": 55,
                        "gorduras": 10,
                        "receita": "Grelhe o frango temperado com ervas. Cozinhe o arroz e o feijão. Monte o prato com a base de salada, arroz, feijão e o frango por cima."
                    },
                    {
                        "nome": "Macarrão com molho de tomate e carne moída",
                        "descricao": "100g de macarrão integral, 100g de carne moída, molho de tomate caseiro e salada verde",
                        "calorias": 550,
                        "proteinas": 35,
                        "carboidratos": 65,
                        "gorduras": 15,
                        "receita": "Cozinhe o macarrão. Refogue a carne moída e adicione o molho de tomate. Misture com o macarrão e sirva com a salada."
                    }
                ],
                "jantar": [
                    {
                        "nome": "Omelete de legumes",
                        "descricao": "3 ovos, tomate, cebola, pimentão e espinafre, acompanhado de 1 fatia de pão integral",
                        "calorias": 400,
                        "proteinas": 25,
                        "carboidratos": 20,
                        "gorduras": 22,
                        "receita": "Bata os ovos e adicione os legumes picados. Cozinhe em frigideira antiaderente. Sirva com uma fatia de pão integral."
                    },
                    {
                        "nome": "Sopa de legumes com frango",
                        "descricao": "Sopa com 100g de frango desfiado, cenoura, abobrinha, cebola e batata",
                        "calorias": 350,
                        "proteinas": 30,
                        "carboidratos": 30,
                        "gorduras": 10,
                        "receita": "Cozinhe o frango e desfie. Refogue os legumes picados, adicione água e o frango. Tempere a gosto e deixe cozinhar até os legumes ficarem macios."
                    }
                ],
                "lanche": [
                    {
                        "nome": "Mix de oleaginosas",
                        "descricao": "30g de mix de castanhas, nozes e amêndoas",
                        "calorias": 180,
                        "proteinas": 6,
                        "carboidratos": 5,
                        "gorduras": 16,
                        "receita": "Misture as oleaginosas em um pote e consuma como lanche."
                    },
                    {
                        "nome": "Smoothie de frutas",
                        "descricao": "1 banana, 100g de morango, 200ml de leite desnatado e 1 colher de aveia",
                        "calorias": 250,
                        "proteinas": 10,
                        "carboidratos": 45,
                        "gorduras": 3,
                        "receita": "Bata todos os ingredientes no liquidificador até obter uma mistura homogênea."
                    }
                ]
            },
            "low_carb": {
                "cafe_da_manha": [
                    {
                        "nome": "Omelete proteico",
                        "descricao": "3 ovos, queijo, espinafre e tomate",
                        "calorias": 350,
                        "proteinas": 25,
                        "carboidratos": 5,
                        "gorduras": 25,
                        "receita": "Bata os ovos e adicione os ingredientes picados. Cozinhe em frigideira antiaderente até dourar."
                    },
                    {
                        "nome": "Iogurte com frutas vermelhas",
                        "descricao": "1 pote de iogurte grego, 50g de frutas vermelhas e 1 colher de chia",
                        "calorias": 250,
                        "proteinas": 15,
                        "carboidratos": 15,
                        "gorduras": 12,
                        "receita": "Em uma tigela, coloque o iogurte, adicione as frutas e finalize com a chia por cima."
                    }
                ],
                "almoco": [
                    {
                        "nome": "Salada de frango",
                        "descricao": "150g de frango grelhado, folhas verdes variadas, tomate, pepino e azeite",
                        "calorias": 400,
                        "proteinas": 40,
                        "carboidratos": 10,
                        "gorduras": 20,
                        "receita": "Grelhe o frango temperado. Monte a salada com as folhas, adicione os legumes picados, o frango e regue com azeite."
                    },
                    {
                        "nome": "Carne com legumes",
                        "descricao": "150g de carne bovina, brócolis, couve-flor e abobrinha refogados",
                        "calorias": 450,
                        "proteinas": 35,
                        "carboidratos": 15,
                        "gorduras": 25,
                        "receita": "Grelhe a carne. Refogue os legumes em azeite e temperos. Sirva a carne com os legumes ao lado."
                    }
                ],
                "jantar": [
                    {
                        "nome": "Peixe com aspargos",
                        "descricao": "150g de filé de peixe, aspargos grelhados e salada verde",
                        "calorias": 350,
                        "proteinas": 35,
                        "carboidratos": 8,
                        "gorduras": 18,
                        "receita": "Grelhe o peixe temperado. Cozinhe os aspargos no vapor ou grelhe. Sirva com salada verde."
                    },
                    {
                        "nome": "Omelete de queijo e presunto",
                        "descricao": "3 ovos, queijo, presunto e espinafre",
                        "calorias": 400,
                        "proteinas": 30,
                        "carboidratos": 5,
                        "gorduras": 28,
                        "receita": "Bata os ovos e adicione os ingredientes picados. Cozinhe em frigideira antiaderente até dourar."
                    }
                ],
                "lanche": [
                    {
                        "nome": "Queijo com azeitonas",
                        "descricao": "50g de queijo e 10 azeitonas",
                        "calorias": 200,
                        "proteinas": 12,
                        "carboidratos": 2,
                        "gorduras": 16,
                        "receita": "Corte o queijo em cubos e sirva com as azeitonas."
                    },
                    {
                        "nome": "Abacate com atum",
                        "descricao": "1/2 abacate e 50g de atum em conserva",
                        "calorias": 250,
                        "proteinas": 15,
                        "carboidratos": 6,
                        "gorduras": 18,
                        "receita": "Amasse o abacate, misture com o atum e tempere a gosto."
                    }
                ]
            },
            "cetogenica": {
                "cafe_da_manha": [
                    {
                        "nome": "Café com manteiga",
                        "descricao": "Café preto com 1 colher de manteiga e 1 colher de óleo de coco",
                        "calorias": 250,
                        "proteinas": 0,
                        "carboidratos": 0,
                        "gorduras": 28,
                        "receita": "Prepare o café, adicione a manteiga e o óleo de coco. Bata no liquidificador até ficar cremoso."
                    },
                    {
                        "nome": "Ovos com bacon e abacate",
                        "descricao": "2 ovos fritos, 2 fatias de bacon e 1/2 abacate",
                        "calorias": 450,
                        "proteinas": 20,
                        "carboidratos": 5,
                        "gorduras": 40,
                        "receita": "Frite o bacon, depois frite os ovos na mesma frigideira. Sirva com meio abacate fatiado."
                    }
                ],
                "almoco": [
                    {
                        "nome": "Bife com manteiga de ervas",
                        "descricao": "200g de bife, 1 colher de manteiga com ervas e salada verde",
                        "calorias": 500,
                        "proteinas": 35,
                        "carboidratos": 2,
                        "gorduras": 38,
                        "receita": "Grelhe o bife ao ponto desejado. Adicione a manteiga com ervas por cima para derreter. Sirva com salada verde."
                    },
                    {
                        "nome": "Salmão com espinafre",
                        "descricao": "150g de salmão grelhado e espinafre refogado em manteiga",
                        "calorias": 450,
                        "proteinas": 30,
                        "carboidratos": 3,
                        "gorduras": 35,
                        "receita": "Grelhe o salmão. Refogue o espinafre em manteiga. Sirva o salmão sobre o espinafre."
                    }
                ],
                "jantar": [
                    {
                        "nome": "Frango com molho de queijo",
                        "descricao": "150g de frango grelhado com molho de queijo e brócolis",
                        "calorias": 500,
                        "proteinas": 40,
                        "carboidratos": 5,
                        "gorduras": 35,
                        "receita": "Grelhe o frango. Prepare o molho de queijo derretendo queijo com creme de leite. Sirva o frango com o molho por cima e brócolis ao lado."
                    },
                    {
                        "nome": "Omelete recheado",
                        "descricao": "3 ovos, queijo, bacon e abacate",
                        "calorias": 550,
                        "proteinas": 25,
                        "carboidratos": 5,
                        "gorduras": 45,
                        "receita": "Bata os ovos, adicione o queijo e o bacon picado. Cozinhe em frigideira antiaderente. Sirva com abacate fatiado."
                    }
                ],
                "lanche": [
                    {
                        "nome": "Bombinhas de gordura",
                        "descricao": "1 colher de manteiga de amendoim, 1 colher de óleo de coco e 1 colher de cacau em pó",
                        "calorias": 200,
                        "proteinas": 3,
                        "carboidratos": 2,
                        "gorduras": 20,
                        "receita": "Misture todos os ingredientes, forme pequenas bolas e leve à geladeira para endurecer."
                    },
                    {
                        "nome": "Queijo com azeitonas",
                        "descricao": "50g de queijo e 10 azeitonas",
                        "calorias": 200,
                        "proteinas": 12,
                        "carboidratos": 2,
                        "gorduras": 16,
                        "receita": "Corte o queijo em cubos e sirva com as azeitonas."
                    }
                ]
            },
            "vegetariana": {
                "cafe_da_manha": [
                    {
                        "nome": "Smoothie proteico",
                        "descricao": "1 banana, 200ml de leite, 1 colher de pasta de amendoim e 1 colher de aveia",
                        "calorias": 350,
                        "proteinas": 15,
                        "carboidratos": 45,
                        "gorduras": 12,
                        "receita": "Bata todos os ingredientes no liquidificador até obter uma mistura homogênea."
                    },
                    {
                        "nome": "Torradas com abacate",
                        "descricao": "2 fatias de pão integral com 1/2 abacate amassado e tomate",
                        "calorias": 300,
                        "proteinas": 8,
                        "carboidratos": 35,
                        "gorduras": 15,
                        "receita": "Torre o pão, amasse o abacate e espalhe sobre as torradas. Adicione fatias de tomate por cima."
                    }
                ],
                "almoco": [
                    {
                        "nome": "Bowl de grãos",
                        "descricao": "100g de quinoa, grão-de-bico, abacate, tomate e folhas verdes",
                        "calorias": 450,
                        "proteinas": 15,
                        "carboidratos": 60,
                        "gorduras": 15,
                        "receita": "Cozinhe a quinoa e o grão-de-bico. Monte o bowl com a base de quinoa, adicione o grão-de-bico, legumes picados e abacate."
                    },
                    {
                        "nome": "Risoto de cogumelos",
                        "descricao": "100g de arroz arbóreo, cogumelos variados, cebola e queijo parmesão",
                        "calorias": 500,
                        "proteinas": 12,
                        "carboidratos": 70,
                        "gorduras": 15,
                        "receita": "Refogue a cebola, adicione os cogumelos e o arroz. Acrescente caldo aos poucos até o arroz ficar al dente. Finalize com queijo parmesão."
                    }
                ],
                "jantar": [
                    {
                        "nome": "Omelete de legumes",
                        "descricao": "3 ovos, tomate, cebola, pimentão e espinafre",
                        "calorias": 350,
                        "proteinas": 20,
                        "carboidratos": 10,
                        "gorduras": 22,
                        "receita": "Bata os ovos e adicione os legumes picados. Cozinhe em frigideira antiaderente até dourar."
                    },
                    {
                        "nome": "Sopa de lentilha",
                        "descricao": "100g de lentilha, cenoura, cebola, alho e tomate",
                        "calorias": 300,
                        "proteinas": 15,
                        "carboidratos": 50,
                        "gorduras": 2,
                        "receita": "Refogue a cebola e o alho, adicione os legumes picados e a lentilha. Acrescente água e deixe cozinhar até a lentilha ficar macia."
                    }
                ],
                "lanche": [
                    {
                        "nome": "Iogurte com frutas",
                        "descricao": "1 pote de iogurte, 1 banana e 1 colher de granola",
                        "calorias": 200,
                        "proteinas": 10,
                        "carboidratos": 35,
                        "gorduras": 3,
                        "receita": "Em uma tigela, coloque o iogurte, adicione a banana picada e finalize com a granola por cima."
                    },
                    {
                        "nome": "Hummus com palitos de legumes",
                        "descricao": "50g de hummus com palitos de cenoura e pepino",
                        "calorias": 150,
                        "proteinas": 5,
                        "carboidratos": 15,
                        "gorduras": 8,
                        "receita": "Sirva o hummus em uma tigela pequena com os palitos de legumes ao lado para mergulhar."
                    }
                ]
            },
            "vegana": {
                "cafe_da_manha": [
                    {
                        "nome": "Smoothie verde",
                        "descricao": "1 banana, espinafre, 200ml de leite vegetal e 1 colher de chia",
                        "calorias": 250,
                        "proteinas": 8,
                        "carboidratos": 40,
                        "gorduras": 6,
                        "receita": "Bata todos os ingredientes no liquidificador até obter uma mistura homogênea."
                    },
                    {
                        "nome": "Aveia overnight",
                        "descricao": "50g de aveia, 200ml de leite vegetal, 1 colher de chia e frutas",
                        "calorias": 300,
                        "proteinas": 10,
                        "carboidratos": 50,
                        "gorduras": 5,
                        "receita": "Misture a aveia, o leite vegetal e a chia em um pote. Deixe na geladeira durante a noite. Pela manhã, adicione frutas picadas."
                    }
                ],
                "almoco": [
                    {
                        "nome": "Bowl de proteína vegetal",
                        "descricao": "100g de tofu, 100g de quinoa, legumes variados e molho de tahine",
                        "calorias": 450,
                        "proteinas": 20,
                        "carboidratos": 55,
                        "gorduras": 15,
                        "receita": "Refogue o tofu temperado. Cozinhe a quinoa. Monte o bowl com a base de quinoa, adicione o tofu e os legumes. Regue com molho de tahine."
                    },
                    {
                        "nome": "Macarrão com molho de tomate e lentilha",
                        "descricao": "100g de macarrão integral, molho de tomate caseiro e 50g de lentilha",
                        "calorias": 400,
                        "proteinas": 15,
                        "carboidratos": 70,
                        "gorduras": 5,
                        "receita": "Cozinhe o macarrão e a lentilha separadamente. Prepare o molho de tomate e misture com a lentilha. Sirva sobre o macarrão."
                    }
                ],
                "jantar": [
                    {
                        "nome": "Curry de grão-de-bico",
                        "descricao": "100g de grão-de-bico, leite de coco, curry e legumes",
                        "calorias": 400,
                        "proteinas": 15,
                        "carboidratos": 45,
                        "gorduras": 18,
                        "receita": "Refogue os legumes, adicione o grão-de-bico cozido, o curry e o leite de coco. Deixe cozinhar até engrossar o molho."
                    },
                    {
                        "nome": "Wrap de legumes",
                        "descricao": "1 wrap integral, hummus, alface, tomate, pepino e cenoura ralada",
                        "calorias": 300,
                        "proteinas": 10,
                        "carboidratos": 45,
                        "gorduras": 8,
                        "receita": "Espalhe o hummus sobre o wrap, adicione os legumes e enrole."
                    }
                ],
                "lanche": [
                    {
                        "nome": "Mix de frutas secas e oleaginosas",
                        "descricao": "30g de mix de castanhas, nozes, amêndoas e frutas secas",
                        "calorias": 180,
                        "proteinas": 5,
                        "carboidratos": 15,
                        "gorduras": 12,
                        "receita": "Misture as oleaginosas e frutas secas em um pote e consuma como lanche."
                    },
                    {
                        "nome": "Smoothie de frutas",
                        "descricao": "1 banana, 100g de morango, 200ml de leite vegetal e 1 colher de aveia",
                        "calorias": 200,
                        "proteinas": 5,
                        "carboidratos": 40,
                        "gorduras": 2,
                        "receita": "Bata todos os ingredientes no liquidificador até obter uma mistura homogênea."
                    }
                ]
            }
        }
        
        # Salva o banco de sugestões básico
        with open(self.suggestions_db_path, 'w', encoding='utf-8') as file:
            json.dump(basic_suggestions_db, file, ensure_ascii=False, indent=4)
    
    def _load_motivation_database(self):
        """
        Carrega o banco de mensagens motivacionais.
        
        Returns:
            dict: Banco de mensagens motivacionais
        """
        # Verifica se o arquivo existe
        if not os.path.exists(self.motivation_db_path):
            # Cria um banco de mensagens motivacionais básico se não existir
            self._create_basic_motivation_database()
        
        try:
            with open(self.motivation_db_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Erro ao carregar banco de mensagens motivacionais: {e}")
            return {}
    
    def _create_basic_motivation_database(self):
        """Cria um banco básico de mensagens motivacionais."""
        # Diretório de recursos
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        os.makedirs(resources_dir, exist_ok=True)
        
        # Banco básico de mensagens motivacionais
        basic_motivation_db = {
            "geral": [
                "Lembre-se: cada escolha alimentar saudável é um passo em direção ao seu objetivo! 💪",
                "Você está indo muito bem! Manter a consistência é a chave para o sucesso. 🔑",
                "Pequenas mudanças diárias levam a grandes resultados ao longo do tempo. ✨",
                "Sua saúde agradece por cada decisão consciente que você toma. ❤️",
                "Não desista! Os resultados virão com persistência e paciência. 🌱",
                "Alimentação saudável não é sobre perfeição, mas sobre equilíbrio. ⚖️",
                "Celebre cada vitória, por menor que seja! Você está evoluindo. 🎉",
                "Seu corpo é seu templo. Alimente-o com respeito e amor. 🏛️",
                "A jornada para uma vida mais saudável é um maratona, não uma corrida de 100 metros. 🏃‍♂️",
                "Você tem o poder de transformar sua saúde um prato de cada vez! 🥗"
            ],
            "emagrecer": [
                "Cada caloria conta! Continue fazendo escolhas inteligentes. 🧠",
                "Lembre-se do seu objetivo quando sentir vontade de desistir. 🎯",
                "Seu futuro eu agradecerá por cada esforço que você faz hoje. 🙏",
                "Perder peso é desafiador, mas você é mais forte que qualquer desafio! 💪",
                "Visualize seu progresso e mantenha o foco no resultado final. 👁️",
                "Não compare sua jornada com a de outros. Seu corpo, seu ritmo. ⏱️",
                "Cada dia é uma nova oportunidade para se aproximar do seu objetivo. 🌟",
                "A consistência supera a intensidade. Mantenha-se no caminho! 🛤️",
                "Você não está apenas perdendo peso, está ganhando saúde e qualidade de vida. ✨",
                "Transformação leva tempo. Confie no processo e continue avançando. 🌱"
            ],
            "manter": [
                "Manter o peso é tão importante quanto perder! Continue com o bom trabalho. 👏",
                "Equilíbrio é a chave para manter seu peso e sua saúde. ⚖️",
                "Você encontrou seu ritmo! Continue ouvindo seu corpo. 🎵",
                "Manutenção é sobre consistência e hábitos sustentáveis. 🌿",
                "Celebre a estabilidade! Você conquistou um equilíbrio que muitos desejam. 🏆",
                "Pequenos ajustes mantêm grandes resultados. Continue atento. 👀",
                "Seu compromisso com a saúde é inspirador! Continue assim. ✨",
                "A manutenção é uma prova de disciplina e autoconhecimento. 🧘‍♂️",
                "Você dominou a arte do equilíbrio! Continue praticando diariamente. 🎭",
                "Manter-se saudável é um presente que você dá a si mesmo todos os dias. 🎁"
            ],
            "ganhar_massa": [
                "Construir músculos requer paciência e persistência. Você está no caminho certo! 💪",
                "Cada refeição é uma oportunidade para nutrir seus músculos. Aproveite! 🍽️",
                "Proteína é seu aliado! Continue alimentando seus músculos adequadamente. 🥩",
                "Ganhar massa é um processo. Confie na jornada e nos resultados. 🌱",
                "Seu corpo está respondendo aos estímulos. Continue fornecendo o que ele precisa! 🔄",
                "Força não vem apenas do treino, mas também da nutrição adequada. 🥗",
                "Você está construindo uma versão mais forte de si mesmo, um dia de cada vez. 🏗️",
                "Consistência no treino e na alimentação é a fórmula para o sucesso. ⚗️",
                "Seus músculos agradecem por cada grama de proteína e cada caloria nutritiva! ❤️",
                "O processo de hipertrofia leva tempo. Seja paciente e persistente. ⏳"
            ]
        }
        
        # Salva o banco de mensagens motivacionais básico
        with open(self.motivation_db_path, 'w', encoding='utf-8') as file:
            json.dump(basic_motivation_db, file, ensure_ascii=False, indent=4)
    
    def get_meal_suggestion(self, diet_type, meal_type):
        """
        Retorna uma sugestão de refeição com base no tipo de dieta e tipo de refeição.
        
        Args:
            diet_type (str): Tipo de dieta (flexivel, low_carb, etc.)
            meal_type (str): Tipo de refeição (cafe_da_manha, almoco, etc.)
            
        Returns:
            dict: Sugestão de refeição
        """
        # Normaliza os tipos
        diet_type = diet_type.lower()
        meal_type = meal_type.lower()
        
        # Mapeia tipos de refeição para categorias no banco de dados
        meal_type_mapping = {
            'cafe_da_manha': 'cafe_da_manha',
            'lanche_manha': 'lanche',
            'almoco': 'almoco',
            'lanche_tarde': 'lanche',
            'jantar': 'jantar',
            'ceia': 'lanche',
            'refeicao': 'almoco'  # Padrão para refeições não especificadas
        }
        
        # Obtém a categoria correta
        category = meal_type_mapping.get(meal_type, 'almoco')
        
        # Verifica se o tipo de dieta existe no banco de dados
        if diet_type not in self.suggestions_database:
            # Usa dieta flexível como padrão
            diet_type = 'flexivel'
        
        # Obtém as sugestões para a categoria
        suggestions = self.suggestions_database[diet_type][category]
        
        # Retorna uma sugestão aleatória
        if suggestions:
            return random.choice(suggestions)
        else:
            return None
    
    def get_motivation_message(self, goal=None):
        """
        Retorna uma mensagem motivacional com base no objetivo do usuário.
        
        Args:
            goal (str, optional): Objetivo do usuário (emagrecer, manter, ganhar_massa)
            
        Returns:
            str: Mensagem motivacional
        """
        if goal and goal in self.motivation_database:
            # Retorna uma mensagem específica para o objetivo
            messages = self.motivation_database[goal]
        else:
            # Retorna uma mensagem geral
            messages = self.motivation_database['geral']
        
        # Retorna uma mensagem aleatória
        if messages:
            return random.choice(messages)
        else:
            return "Continue se esforçando! Você está no caminho certo. 💪"
