# Instruções de Instalação - NutriBot Evolve

Este documento contém as instruções para instalar e configurar o NutriBot Evolve, um bot de dieta e nutrição para Telegram.

## Requisitos do Sistema

- Python 3.6 ou superior
- Pip (gerenciador de pacotes Python)
- Acesso à internet
- Conta no Telegram
- Token de bot do Telegram (obtido através do @BotFather)

## Método de Instalação Rápida (Recomendado)

O NutriBot Evolve possui scripts de instalação simplificada que automatizam todo o processo.

### 1. Baixar o Projeto

Baixe e extraia o arquivo ZIP do projeto ou clone o repositório:

```bash
git clone https://github.com/seu-usuario/nutribot-evolve.git
cd nutribot-evolve
```

### 2. Verificar Compatibilidade (Importante)

Execute primeiro o script de verificação de compatibilidade:

```bash
python compatibility_check.py
```

Este script irá:
- Detectar a versão do python-telegram-bot instalada
- Selecionar automaticamente o arquivo main.py apropriado
- Oferecer a opção de instalar a versão correta se necessário

### 3. Executar o Script de Instalação

Em seguida, execute o script de instalação que irá configurar tudo automaticamente:

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

## Dependências

O NutriBot Evolve requer as seguintes bibliotecas Python:

- python-telegram-bot==13.7
- matplotlib==3.5.1
- numpy==1.22.3
- Pillow==9.0.1

Todas estas dependências são instaladas automaticamente pelo script de instalação ou manualmente através do arquivo `requirements.txt`.

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

## Configurações Adicionais (Opcional)

### Personalização de Mensagens

Você pode personalizar as mensagens do bot editando as constantes no arquivo `config.py`.

### Configuração de Logging

Para ajustar o nível de logging, modifique a configuração no arquivo `main.py`:

```python
# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Altere para logging.DEBUG para mais detalhes
)
```

## Implantação em Produção

Para implantar o bot em um servidor de produção:

1. Configure um servidor com Python instalado
2. Clone o repositório no servidor
3. Instale as dependências conforme descrito acima
4. Configure o bot para iniciar automaticamente:
   - Usando systemd (Linux):
     ```
     [Unit]
     Description=NutriBot Evolve Telegram Bot
     After=network.target

     [Service]
     User=seu_usuario
     WorkingDirectory=/caminho/para/nutribot-evolve
     ExecStart=/caminho/para/python /caminho/para/nutribot-evolve/main.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```
   - Salve como `/etc/systemd/system/nutribot.service`
   - Ative com:
     ```bash
     sudo systemctl enable nutribot
     sudo systemctl start nutribot
     ```

## Atualizações

Para atualizar o bot para uma nova versão:

1. Faça backup do banco de dados:
   ```bash
   cp nutribot.db nutribot.db.backup
   ```

2. Atualize o código:
   ```bash
   git pull
   ```

3. Instale novas dependências, se houver:
   ```bash
   pip install -r requirements.txt
   ```

4. Reinicie o bot

## Suporte

Se encontrar problemas durante a instalação, entre em contato:

- Email: suporte@nutribotevolve.com
- Telegram: @NutriBot_Suporte
