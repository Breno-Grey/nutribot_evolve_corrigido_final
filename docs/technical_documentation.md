# Documentação Técnica - NutriBot Evolve

## Visão Geral

O NutriBot Evolve é um bot para Telegram desenvolvido para auxiliar usuários em suas jornadas de dieta e nutrição. O bot oferece funcionalidades como cálculo de necessidades calóricas, registro de refeições, análise de fotos corporais, sugestões de refeições, relatórios de progresso e recursos premium.

## Arquitetura

O NutriBot Evolve segue uma arquitetura modular organizada em camadas:

```
nutribot_evolve/
├── database/           # Camada de acesso a dados
│   ├── db_manager.py   # Gerenciador de conexão com banco de dados
│   ├── user_repository.py  # Operações de usuários
│   ├── meal_repository.py  # Operações de refeições
│   └── photo_repository.py # Operações de fotos
├── handlers/           # Manipuladores de comandos do Telegram
│   ├── onboarding_handler.py  # Manipulador de cadastro
│   ├── meal_handler.py        # Manipulador de refeições
│   ├── suggestion_handler.py  # Manipulador de sugestões
│   ├── photo_handler.py       # Manipulador de fotos
│   ├── report_handler.py      # Manipulador de relatórios
│   └── premium_handler.py     # Manipulador de recursos premium
├── utils/              # Utilitários e lógica de negócio
│   ├── calorie_calculator.py  # Calculador de calorias
│   ├── conversation_manager.py # Gerenciador de conversação
│   ├── meal_analyzer.py       # Analisador de refeições
│   ├── meal_suggester.py      # Sugestor de refeições
│   ├── photo_analyzer.py      # Analisador de fotos
│   └── report_generator.py    # Gerador de relatórios
├── photos/             # Diretório para armazenar fotos
├── reports/            # Diretório para armazenar relatórios
├── config.py           # Configurações do bot
├── main.py             # Ponto de entrada da aplicação
├── test.py             # Script de testes
└── optimize.py         # Script de otimizações
```

## Componentes Principais

### 1. Banco de Dados

O NutriBot Evolve utiliza SQLite como banco de dados, com as seguintes tabelas:

- **users**: Armazena informações dos usuários (dados pessoais, metas, preferências)
- **meals**: Registra as refeições dos usuários (tipo, descrição, valores nutricionais)
- **photos**: Armazena referências às fotos corporais dos usuários
- **conversations**: Gerencia estados de conversação para fluxos interativos

### 2. Módulos Principais

#### Onboarding e Cálculo Calórico
- Coleta dados do usuário (idade, peso, altura, gênero, nível de atividade)
- Calcula TMB (Taxa Metabólica Basal) usando a fórmula de Mifflin-St Jeor
- Ajusta calorias com base no nível de atividade e objetivo (TDEE)
- Calcula distribuição de macronutrientes com base no tipo de dieta

#### Registro de Refeições
- Permite registro de refeições por texto natural
- Analisa descrições de refeições para extrair informações nutricionais
- Calcula e armazena valores calóricos e macronutrientes
- Fornece visualização do consumo diário

#### Sugestões de Refeições
- Oferece sugestões personalizadas com base no tipo de dieta
- Fornece receitas adaptadas para diferentes objetivos
- Inclui mensagens motivacionais personalizadas

#### Análise de Fotos Corporais
- Armazena fotos de forma segura
- Permite comparação visual entre fotos
- Fornece análise básica de qualidade da imagem
- Gera sugestões para melhorar as fotos

#### Relatórios e Recursos Premium
- Gera relatórios semanais de consumo calórico e macronutrientes
- Cria gráficos de progresso
- Oferece recursos premium como relatórios mensais detalhados e exportação em PDF
- Inclui planos de treino personalizados e acesso a consultas com nutricionistas

### 3. Fluxos de Interação

O bot utiliza um sistema de gerenciamento de estados de conversação para manter fluxos interativos, como:

- Fluxo de onboarding (coleta de dados iniciais)
- Fluxo de registro de refeições
- Fluxo de envio de fotos

## Requisitos Técnicos

### Dependências

- Python 3.6+
- python-telegram-bot
- matplotlib
- Pillow
- numpy
- sqlite3 (embutido no Python)

### Configuração

O arquivo `config.py` contém as configurações principais:

- Token do bot do Telegram
- Mensagens padrão
- Configurações de banco de dados
- Constantes do sistema

## Otimizações Implementadas

- Cache em memória para cálculos frequentes
- Índices de banco de dados para consultas comuns
- Medição de tempo para funções críticas
- Cache de estados de conversação para melhorar tempo de resposta

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

- Novos comandos podem ser adicionados criando novos manipuladores
- Novos tipos de dieta podem ser adicionados no calculador de calorias
- Novas sugestões de refeições podem ser adicionadas no banco de dados
- Recursos premium adicionais podem ser implementados no manipulador premium

## Limitações Conhecidas

- A análise de fotos corporais é básica e não utiliza IA avançada
- A análise de refeições por texto tem precisão limitada
- O sistema de lembretes não utiliza notificações programadas

## Segurança

- Dados sensíveis dos usuários são armazenados localmente
- Fotos são armazenadas em diretórios específicos por usuário
- Não há compartilhamento de dados entre usuários

## Manutenção

Para manutenção do sistema:

- Execute `test.py` regularmente para verificar a integridade
- Execute `optimize.py` para otimizar o desempenho
- Faça backup regular do banco de dados
