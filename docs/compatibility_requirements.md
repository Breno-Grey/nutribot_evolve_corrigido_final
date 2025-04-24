# Requisitos de Compatibilidade - NutriBot Evolve

Este documento detalha os requisitos específicos de compatibilidade para o NutriBot Evolve, especialmente em relação à biblioteca python-telegram-bot.

## Versões Suportadas

O NutriBot Evolve foi projetado para funcionar com duas versões principais da biblioteca python-telegram-bot:

### Versão 13.x (Recomendada para a maioria dos usuários)
- Versão específica recomendada: **13.7**
- Características: Usa a API baseada em `Updater` e callbacks síncronos
- Compatibilidade: Mais ampla, funciona na maioria dos ambientes Python 3.6+

### Versão 20.x+
- Versão específica recomendada: **20.0** ou superior
- Características: Usa a API baseada em `Application` e funções assíncronas (async/await)
- Requisito adicional: Python 3.7+ (obrigatório para suporte a async/await)

## Detecção e Correção Automática

O NutriBot Evolve inclui ferramentas para detectar e corrigir automaticamente problemas de compatibilidade:

1. **Script de Verificação de Compatibilidade**
   ```bash
   python compatibility_check.py
   ```
   Este script:
   - Detecta a versão do python-telegram-bot instalada
   - Seleciona automaticamente o arquivo main.py apropriado
   - Oferece a opção de instalar a versão correta se necessário

2. **Script de Teste de Compatibilidade**
   ```bash
   python test_compatibility.py
   ```
   Este script realiza testes abrangentes para verificar se o bot é compatível com seu ambiente atual.

## Solução de Problemas de Compatibilidade

### Erro: "cannot import name 'Application' from 'telegram.ext'"

Este erro ocorre quando você está usando a versão 13.x do python-telegram-bot, mas o código está escrito para a versão 20.x+.

**Solução:**
```bash
python compatibility_check.py
```

### Erro: "cannot import name 'Updater' from 'telegram.ext'"

Este erro ocorre quando você está usando a versão 20.x+ do python-telegram-bot, mas o código está escrito para a versão 13.x.

**Solução:**
```bash
python compatibility_check.py
```

### Erro: "async def" ou "await" causando erro de sintaxe

Este erro ocorre quando você está usando Python 3.6 ou anterior com código escrito para Python 3.7+ (que usa async/await).

**Solução:**
1. Atualize para Python 3.7+ (recomendado), ou
2. Execute `python compatibility_check.py` para usar a versão 13.x do código

## Instalação Manual de Versões Específicas

Se preferir instalar manualmente uma versão específica:

### Para instalar a versão 13.7:
```bash
pip install python-telegram-bot==13.7
```

### Para instalar a versão 20.0+:
```bash
pip install python-telegram-bot>=20.0
```

Após a instalação manual, execute:
```bash
python compatibility_check.py
```
para garantir que o arquivo main.py correto seja selecionado.

## Verificação da Versão Instalada

Para verificar qual versão do python-telegram-bot está instalada:
```bash
pip show python-telegram-bot
```

## Notas Adicionais

- O NutriBot Evolve mantém duas versões do arquivo principal: `main_v13.py` (para versão 13.x) e `main_v20.py` (para versão 20.x+)
- O script de compatibilidade seleciona automaticamente a versão correta com base na biblioteca instalada
- Recomendamos usar a versão 13.7 para maior compatibilidade, a menos que você precise especificamente dos recursos da versão 20.x+
