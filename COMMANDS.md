# 🚀 Community Insights - Comandos e Guia de Uso

## 📋 **Visão Geral**

Sistema de dois serviços independentes que se comunicam via arquivos compartilhados:

- **Oracle Eye**: Coleta mensagens do Telegram (roda em background)
- **Neural Core**: Interface CLI para processamento de IA

---

## 🎯 **Fluxo Completo de Teste**

### **1. Iniciar Oracle Eye (Background)**
```bash
# Terminal 1
cd oracle-eye
venv\Scripts\activate
python src/main.py
```

### **2. Configurar Projeto**
```bash
# Terminal 2
cd neural-core
venv\Scripts\activate
python src/main.py setup-project --name "Taraxa" --group "@taraxa_project"
```

### **3. Solicitar Coleta Imediata**
```bash
# Terminal 2
python src/main.py collect-now --project "Taraxa"
```

### **4. Verificar Status da Coleta**
```bash
# Terminal 2
python src/main.py check-status --project "Taraxa"
```

### **5. Gerar Resumo com IA**
```bash
# Terminal 2 - Resumo com metadata e citações (sempre incluído)
python src/main.py generate-summary --project "Taraxa" --days 7
```

---

## 📚 **Comandos Disponíveis**

### **Neural Core CLI**

#### **Configuração de Projetos**
```bash
# Criar novo projeto
python src/main.py setup-project --name "NomeProjeto" --group "@grupo_telegram"

# Listar todos os projetos
python src/main.py list-projects

# Atualizar projeto
python src/main.py update-project --project "NomeProjeto" --new-name "NovoNome"
```

#### **Coleta de Mensagens**
```bash
# Solicitar coleta imediata (bypass schedule)
python src/main.py collect-now --project "NomeProjeto"

# Verificar status da coleta
python src/main.py check-status --project "NomeProjeto"
```

#### **Processamento de IA**
```bash
# Estimar custo do processamento
python src/main.py estimate-cost --project "NomeProjeto" --days 7

# Gerar resumo com IA (sempre inclui metadata e citações)
python src/main.py generate-summary --project "NomeProjeto" --days 7

# Salvar resumo em arquivo
python src/main.py generate-summary --project "NomeProjeto" --days 7 --output "resumo.md"
```

---

## 📊 **Sistema de Metadata e Citações**

### **O que é o Sistema de Metadata?**
O sistema **sempre gera metadata** que adiciona **rastreabilidade e análise de relevância** aos resumos:

- **Scoring de Relevância**: Cada mensagem recebe um score de 0-100
- **Categorização**: Mensagens são classificadas (announcement, development, community, spam)
- **Citações**: Mensagens de alta relevância são citadas no resumo
- **Estatísticas**: Breakdown detalhado da qualidade das mensagens

### **Como Usar:**
```bash
# Resumo com metadata e citações (sempre incluído)
python src/main.py generate-summary --project "Taraxa" --days 7
```

### **O que o Metadata Inclui:**
- **Total de mensagens** analisadas
- **Breakdown de relevância** (alta, média, baixa)
- **Categorias** de mensagens
- **Top keywords** encontradas
- **Citações** das mensagens mais relevantes
- **Estatísticas** de qualidade

### **Exemplo de Output:**
```
==================================================
 SUMMARY
==================================================
## Key Announcements
- Staking program launch...
- Partnership announcement...

==================================================
 METADATA
==================================================
Total Messages: 777
High Relevance: 45
Medium Relevance: 200
Low Relevance: 532
Average Score: 52.3
High Relevance %: 5.8%

Categories:
  community: 650
  announcement: 45
  development: 82

Top Keywords:
  staking: 12
  partnership: 8
  governance: 6

High-Relevance Citations: 20
  1. Score: 95 - announcement
     Author: @taraxa_official
     Preview: We're excited to announce our new staking program...
```

---

## 🔧 **Configuração**

### **Oracle Eye (.env)**
```bash
# Telegram API
TELEGRAM_API_ID=seu_api_id
TELEGRAM_API_HASH=seu_api_hash
TELEGRAM_PHONE_NUMBER=seu_telefone

# Configurações de coleta
COLLECTION_INTERVAL=86400          # 24 horas
MAX_MESSAGES_PER_COLLECTION=1000

# Banco de dados compartilhado
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

### **Neural Core (.env)**
```bash
# OpenAI API
OPENAI_API_KEY=sua_chave_openai

# Controle de custos
DEFAULT_COST_PER_1K_TOKENS=0.002
DEFAULT_MODEL=gpt-3.5-turbo
MAX_COST_PER_SUMMARY=10.00

# Banco de dados compartilhado
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

---

## 📁 **Estrutura de Arquivos**

```
community-insights/
├── oracle-eye/                    # Serviço de coleta
│   ├── src/
│   ├── requirements.txt
│   └── .env
├── neural-core/                   # Serviço de IA
│   ├── src/
│   ├── requirements.txt
│   └── .env
└── shared/                        # Comunicação entre serviços
    ├── database/
    │   └── crypto_insights.db     # Banco SQLite compartilhado
    ├── commands/                  # Sistema de mensageria
    │   ├── collect_taraxa.json    # Comandos de coleta
    │   └── status_taraxa.json     # Status de processamento
    └── logs/                      # Logs dos serviços
```

---

## 🚨 **Troubleshooting**

### **Problemas Comuns**

1. **Erro de encoding Windows**: Ignorar (será resolvido na migração para Ubuntu)
2. **Projeto não encontrado**: Verificar se foi criado com `list-projects`
3. **Coleta não iniciou**: Verificar se Oracle Eye está rodando
4. **Erro de API**: Verificar credenciais no arquivo `.env`

### **Verificações**

```bash
# Verificar se Oracle Eye está rodando
# Terminal 1 deve mostrar logs de coleta

# Verificar projetos configurados
python src/main.py list-projects

# Verificar status de coleta
python src/main.py check-status --project "Taraxa"

# Verificar agendamento de coleta
python src/main.py check-schedule
python src/main.py check-schedule --project "Taraxa"
```

---

## ⏰ **Sistema de Agendamento Persistente**

### **Como Funciona:**

O Oracle Eye agora usa um **sistema de agendamento persistente** que resolve o problema de perda de timing quando o serviço cai:

1. **Persistência**: Cada projeto tem `next_collection_at` salvo no banco
2. **Verificação Contínua**: Oracle Eye verifica a cada minuto se há projetos prontos
3. **Recuperação Inteligente**: Se cair e subir novamente, continua de onde parou

### **Cenário de Recuperação:**

```
10:00 - Oracle Eye inicia, agenda próxima coleta para 10:00 do próximo dia
20:00 - Oracle Eye cai (após 10 horas)
08:00 - Oracle Eye sobe novamente
08:00 - Verifica: próxima coleta era 10:00, ainda não chegou
10:00 - Executa coleta automaticamente
10:00 - Agenda próxima coleta para 10:00 do próximo dia
```

### **Comandos de Verificação:**

```bash
# Ver agendamento de todos os projetos
python src/main.py check-schedule

# Ver agendamento de um projeto específico
python src/main.py check-schedule --project "Taraxa"
```

---

## 🎯 **Exemplo Completo - Projeto Taraxa**

```bash
# 1. Iniciar Oracle Eye
cd oracle-eye && venv\Scripts\activate && python src/main.py

# 2. Configurar Taraxa (novo terminal)
cd neural-core && venv\Scripts\activate
python src/main.py setup-project --name "Taraxa" --group "@taraxa_project"

# 3. Coletar mensagens
python src/main.py collect-now --project "Taraxa"

# 4. Verificar coleta
python src/main.py check-status --project "Taraxa"

# 5. Gerar resumo
python src/main.py generate-summary --project "Taraxa" --days 7
```

---

## 📝 **Notas Importantes**

- **Oracle Eye** deve rodar continuamente em background
- **Neural Core** é executado sob demanda via CLI
- **Banco de dados** é compartilhado entre os serviços
- **Sistema de comandos** permite comunicação assíncrona
- **Coleta imediata** bypassa o schedule de 24h
- **Custos** são estimados antes do processamento de IA
