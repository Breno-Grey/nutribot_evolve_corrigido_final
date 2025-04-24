# Arquitetura do NutriBot Evolve

## Visão Geral
O NutriBot Evolve é um bot de Telegram para acompanhamento de dieta com recursos de IA. A arquitetura foi projetada para ser modular, escalável e de fácil manutenção.

## Estrutura de Diretórios
```
nutribot_evolve/
├── main.py                  # Ponto de entrada da aplicação
├── config.py                # Configurações e constantes
├── database/
│   ├── __init__.py
│   ├── db_manager.py        # Gerenciador de conexão com banco de dados
│   ├── user_repository.py   # Operações de banco de dados relacionadas a usuários
│   ├── meal_repository.py   # Operações de banco de dados relacionadas a refeições
│   └── photo_repository.py  # Operações de banco de dados relacionadas a fotos
├── handlers/
│   ├── __init__.py
│   ├── start_handler.py     # Manipulador de comandos iniciais
│   ├── onboarding_handler.py # Manipulador do processo de onboarding
│   ├── meal_handler.py      # Manipulador de registro de refeições
│   ├── photo_handler.py     # Manipulador de fotos corporais
│   ├── report_handler.py    # Manipulador de relatórios
│   └── premium_handler.py   # Manipulador de recursos premium
├── utils/
│   ├── __init__.py
│   ├── calorie_calculator.py # Cálculo de calorias e macronutrientes
│   ├── meal_analyzer.py     # Análise de texto para identificar alimentos
│   ├── photo_analyzer.py    # Análise básica de fotos
│   ├── report_generator.py  # Geração de relatórios e gráficos
│   └── message_templates.py # Templates de mensagens
└── resources/
    ├── food_database.json   # Banco de dados de alimentos e valores nutricionais
    ├── meal_suggestions.json # Sugestões de refeições por tipo de dieta
    └── motivation_messages.json # Mensagens motivacionais
```

## Esquema do Banco de Dados

### Tabela: users
```
id INTEGER PRIMARY KEY
user_id INTEGER UNIQUE       # ID do usuário no Telegram
username TEXT                # Nome de usuário no Telegram
full_name TEXT               # Nome completo
age INTEGER                  # Idade
weight REAL                  # Peso em kg
height REAL                  # Altura em cm
gender TEXT                  # Gênero
goal TEXT                    # Objetivo (emagrecer, manter, ganhar massa)
diet_type TEXT               # Tipo de dieta (low carb, cetogênica, etc.)
daily_calories REAL          # Calorias diárias calculadas
is_premium BOOLEAN           # Status premium
created_at TIMESTAMP         # Data de criação
updated_at TIMESTAMP         # Data de atualização
```

### Tabela: meals
```
id INTEGER PRIMARY KEY
user_id INTEGER              # Referência ao usuário
meal_type TEXT               # Tipo de refeição (café da manhã, almoço, etc.)
description TEXT             # Descrição da refeição
calories REAL                # Calorias totais
protein REAL                 # Proteínas em gramas
carbs REAL                   # Carboidratos em gramas
fat REAL                     # Gorduras em gramas
meal_date DATE               # Data da refeição
created_at TIMESTAMP         # Data de criação
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

### Tabela: photos
```
id INTEGER PRIMARY KEY
user_id INTEGER              # Referência ao usuário
photo_path TEXT              # Caminho para o arquivo da foto
description TEXT             # Descrição ou comentários
photo_date DATE              # Data da foto
created_at TIMESTAMP         # Data de criação
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

### Tabela: reminders
```
id INTEGER PRIMARY KEY
user_id INTEGER              # Referência ao usuário
reminder_type TEXT           # Tipo de lembrete
reminder_time TIME           # Horário do lembrete
is_active BOOLEAN            # Status do lembrete
created_at TIMESTAMP         # Data de criação
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

### Tabela: reports
```
id INTEGER PRIMARY KEY
user_id INTEGER              # Referência ao usuário
report_type TEXT             # Tipo de relatório
start_date DATE              # Data inicial do período
end_date DATE                # Data final do período
report_data TEXT             # Dados do relatório em JSON
created_at TIMESTAMP         # Data de criação
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

## Fluxo de Interação do Usuário

1. **Início e Onboarding**
   - Usuário inicia o bot com comando /start
   - Bot apresenta mensagem de boas-vindas e explica seu propósito
   - Bot inicia processo de onboarding com perguntas sequenciais
   - Dados são coletados e armazenados no banco de dados
   - Cálculo de gasto calórico é realizado e apresentado ao usuário

2. **Registro de Refeições**
   - Usuário envia texto descrevendo o que comeu
   - Bot analisa o texto e identifica alimentos
   - Bot calcula calorias e macronutrientes
   - Informações são armazenadas no banco de dados
   - Bot apresenta resumo da refeição e status diário

3. **Sugestões e Lembretes**
   - Bot envia lembretes em horários configurados
   - Bot sugere refeições baseadas no perfil do usuário
   - Bot envia mensagens motivacionais periodicamente

4. **Análise de Fotos**
   - Usuário envia foto corporal
   - Bot armazena a foto de forma segura
   - Bot compara com fotos anteriores (se disponíveis)
   - Bot fornece orientações para próximas fotos

5. **Relatórios Semanais**
   - Bot gera relatório semanal automaticamente
   - Relatório inclui gráficos de progresso
   - Bot envia insights e sugestões de ajustes

6. **Recursos Premium**
   - Usuário pode ativar modo premium
   - Bot disponibiliza recursos exclusivos
   - Relatórios mais detalhados são gerados

## Componentes Principais

### Gerenciador de Banco de Dados
Responsável por estabelecer conexão com o banco SQLite e fornecer métodos para operações CRUD.

### Calculadora de Calorias
Implementa algoritmos para cálculo de gasto calórico basal e total com base nos dados do usuário.

### Analisador de Refeições
Processa texto natural para identificar alimentos e calcular valores nutricionais.

### Analisador de Fotos
Implementa funcionalidades básicas para armazenamento e comparação de fotos.

### Gerador de Relatórios
Cria relatórios semanais com gráficos e insights baseados nos dados coletados.

### Gerenciador de Mensagens
Controla o envio de lembretes, sugestões e mensagens motivacionais.

## Considerações Técnicas

### Bibliotecas Principais
- python-telegram-bot: Para interação com a API do Telegram
- SQLite3: Para gerenciamento do banco de dados
- NLTK ou spaCy: Para processamento de linguagem natural
- Matplotlib ou Plotly: Para geração de gráficos
- Pillow: Para manipulação básica de imagens

### Segurança
- Dados sensíveis dos usuários serão armazenados de forma segura
- Fotos serão armazenadas com acesso restrito
- Implementação de validação de entrada para prevenir injeção SQL

### Escalabilidade
- Arquitetura modular permite adicionar novos recursos facilmente
- Banco de dados SQLite pode ser migrado para PostgreSQL se necessário
- Componentes independentes facilitam manutenção e testes
