# NutriBot Evolve - README

## Visão Geral

O NutriBot Evolve é um bot de dieta e nutrição para Telegram que ajuda os usuários a alcançarem seus objetivos de saúde. O bot oferece funcionalidades como cálculo de necessidades calóricas, registro de refeições, análise de fotos corporais, sugestões de refeições personalizadas, relatórios de progresso e recursos premium.

## Funcionalidades Principais

- **Onboarding personalizado**: Coleta de dados do usuário para cálculo preciso de necessidades calóricas
- **Registro de refeições**: Entrada de texto natural para registrar alimentos consumidos
- **Análise calórica**: Cálculo automático de calorias e macronutrientes
- **Sugestões de refeições**: Recomendações personalizadas com base no tipo de dieta
- **Análise de fotos corporais**: Acompanhamento visual de progresso com comparação de fotos
- **Relatórios**: Visualização gráfica de consumo calórico e macronutrientes
- **Recursos premium**: Relatórios avançados, planos de treino e consultas com nutricionistas

## Estrutura do Projeto

```
nutribot_evolve/
├── database/           # Camada de acesso a dados
├── handlers/           # Manipuladores de comandos do Telegram
├── utils/              # Utilitários e lógica de negócio
├── docs/               # Documentação
├── photos/             # Diretório para armazenar fotos
├── reports/            # Diretório para armazenar relatórios
├── config.py           # Configurações do bot
├── main.py             # Ponto de entrada da aplicação
├── test.py             # Script de testes
└── optimize.py         # Script de otimizações
```

## Documentação

A documentação completa está disponível no diretório `docs/`:

- [Documentação Técnica](docs/technical_documentation.md): Arquitetura, componentes e aspectos técnicos
- [Manual do Usuário](docs/user_manual.md): Guia completo para usuários finais
- [Instruções de Instalação](docs/installation_guide.md): Como configurar e executar o bot

## Requisitos

- Python 3.6+
- python-telegram-bot
- matplotlib
- Pillow
- numpy
- Token de bot do Telegram (obtido através do @BotFather)

## Instalação Rápida

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o token do bot no arquivo `config.py`
4. Execute o bot: `python main.py`

Para instruções detalhadas, consulte o [Guia de Instalação](docs/installation_guide.md).

## Testes

Execute o script de testes para verificar a integridade do sistema:

```bash
python test.py
```

## Otimizações

Execute o script de otimizações para melhorar o desempenho:

```bash
python optimize.py
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para suporte ou dúvidas, entre em contato:
- Email: contato@nutribotevolve.com
- Telegram: @NutriBot_Suporte
