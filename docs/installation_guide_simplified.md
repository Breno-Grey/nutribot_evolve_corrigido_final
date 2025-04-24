# Instruções de Instalação Simplificadas - NutriBot Evolve

Este documento contém as instruções para instalar e configurar o NutriBot Evolve, um bot de dieta e nutrição para Telegram.

## Requisitos do Sistema

- Python 3.6 ou superior
- Pip (gerenciador de pacotes Python)
- Acesso à internet
- Conta no Telegram
- Token de bot do Telegram (obtido através do @BotFather)

## Método de Instalação Rápida (Recomendado)

O NutriBot Evolve agora possui um script de instalação simplificada que automatiza todo o processo.

### 1. Baixar o Projeto

Baixe e extraia o arquivo ZIP do projeto ou clone o repositório:

```bash
git clone https://github.com/seu-usuario/nutribot-evolve.git
cd nutribot-evolve
```

### 2. Executar o Script de Instalação

Execute o script de instalação que irá configurar tudo automaticamente:

```bash
python setup.py
```

Este script irá:
- Verificar a versão do Python
- Instalar todas as dependências necessárias
- Criar os diretórios necessários
- Inicializar o banco de dados
- Solicitar e configurar o token do bot
- Testar a instalação

### 3. Iniciar o Bot

Após a instalação bem-sucedida, inicie o bot com:

```bash
python main.py
```

## Método de Instalação Manual (Alternativo)

Se preferir instalar manualmente ou se o script de instalação automática falhar, siga estas etapas:

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Verificar Dependências (Opcional)

Para verificar se todas as dependências estão instaladas corretamente:

```bash
python check_dependencies.py
```

### 3. Inicializar o Banco de Dados

```bash
python initialize_database.py
```

### 4. Configurar o Token do Bot

Edite o arquivo `config.py` e substitua `"SEU_TOKEN_AQUI"` pelo token obtido do BotFather:

```python
# Token do bot do Telegram
BOT_TOKEN = "seu_token_aqui"
```

### 5. Iniciar o Bot

```bash
python main.py
```

## Solução de Problemas

### Erro ao Instalar Dependências

Se encontrar problemas ao instalar as dependências:

```bash
# Tente atualizar o pip primeiro
python -m pip install --upgrade pip

# Em alguns sistemas, pode ser necessário instalar pacotes adicionais
# No Ubuntu/Debian:
sudo apt-get install python3-dev libpng-dev libfreetype6-dev
```

### Erro ao Inicializar o Banco de Dados

Se o script de inicialização do banco de dados falhar:

1. Verifique se você tem permissões de escrita no diretório atual
2. Certifique-se de que os diretórios `photos` e `reports` existam ou crie-os manualmente:
   ```bash
   mkdir -p photos reports
   ```

### Erro ao Iniciar o Bot

Se o bot não iniciar corretamente:

1. Verifique se o token está configurado corretamente em `config.py`
2. Certifique-se de que todas as dependências estão instaladas
3. Verifique se o banco de dados foi inicializado corretamente

## Verificando a Instalação

Para verificar se a instalação foi bem-sucedida:

1. Execute o script de teste:
   ```bash
   python test.py
   ```

2. Abra o Telegram e inicie uma conversa com seu bot
3. Envie o comando `/start` e verifique se o bot responde

## Suporte

Se encontrar problemas durante a instalação, entre em contato:

- Email: suporte@nutribotevolve.com
- Telegram: @NutriBot_Suporte
