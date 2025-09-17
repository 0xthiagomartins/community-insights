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
# Terminal 2
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

# Gerar resumo com IA
python src/main.py generate-summary --project "NomeProjeto" --days 7

# Salvar resumo em arquivo
python src/main.py generate-summary --project "NomeProjeto" --days 7 --output "resumo.md"
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
