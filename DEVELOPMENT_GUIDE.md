# 🚀 Development Guide - Crypto Community Insights

> **Complete guide for developing and maintaining the decoupled services**

This guide explains how to work with the **Oracle Eye** and **Neural Core** services, which run independently in separate Python environments.

---

## 🏗️ **Architecture Overview**

The system is built as **two independent services** that communicate through a shared database:

```
┌─────────────────────────────────────────────────────────────┐
│                    ORACLE EYE SERVICE                       │
│                 (Python Environment 1)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              AUTOMATIC COLLECTION                       │ │
│  │                                                         │ │
│  │ • Telethon (Telegram API)                              │ │
│  │ • Background Scheduler                                  │ │
│  │ • SQLModel + SQLite                                     │ │
│  │ • Continuous Message Collection                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    NEURAL CORE SERVICE                     │
│                 (Python Environment 2)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              AI PROCESSING & CLI                        │ │
│  │                                                         │ │
│  │ • CrewAI (AI Orchestration)                            │ │
│  │ • Typer (Command Line Interface)                       │ │
│  │ • Cost Estimation                                      │ │
│  │ • Summary Generation                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    SHARED DATABASE                         │
│                 (SQLite + SQLModel)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              DATA EXCHANGE LAYER                        │ │
│  │                                                         │ │
│  │ • Messages Storage                                     │ │
│  │ • Projects Configuration                               │ │
│  │ • Summaries Archive                                    │ │
│  │ • Cross-Service Communication                          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 **Getting Started**

### **1. Initial Setup**

```bash
# Clone the repository
git clone <repository-url>
cd crypto-insights

# Create shared directories
mkdir -p shared/database shared/logs shared/sessions
```

### **2. Oracle Eye Setup (Python Environment 1)**

```bash
# Navigate to Oracle Eye
cd oracle-eye

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your Telegram credentials
```

### **3. Neural Core Setup (Python Environment 2)**

```bash
# Navigate to Neural Core
cd ../neural-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your OpenAI API key
```

---

## 🔄 **Service Operation**

### **Oracle Eye (Background Service)**

```bash
# Start continuous collection
cd oracle-eye
source venv/bin/activate
python src/main.py

# The service will:
# 1. Connect to Telegram via Telethon
# 2. Start collecting messages from configured groups
# 3. Store messages in shared database
# 4. Continue collection cycle indefinitely
```

### **Neural Core (CLI Interface)**

```bash
# Start CLI interface
cd neural-core
source venv/bin/activate
python -m cli.main

# Available commands:
# setup-project --name "Project" --group "telegram_group"
# list-projects
# estimate-cost --project "Project" --days 7
# generate-summary --project "Project" --days 7
# update-project --project "Project" --new-name "NewName"
```

---

## 🛠️ **Development Workflow**

### **Independent Development**

Each service can be developed independently:

- **Oracle Eye**: Focus on collection efficiency, error handling, and monitoring
- **Neural Core**: Focus on AI processing, CLI UX, and cost optimization
- **Shared Models**: Update database models in both services simultaneously

### **Testing Strategy**

```bash
# Test Oracle Eye independently
cd oracle-eye
source venv/bin/activate
pytest tests/

# Test Neural Core independently
cd ../neural-core
source venv/bin/activate
pytest tests/

# Integration testing (both services running)
# Terminal 1: Start Oracle Eye
cd oracle-eye && python src/main.py

# Terminal 2: Test Neural Core
cd neural-core && python -m cli.main setup-project --name "Test" --group "test"
```

### **Database Schema Changes**

When updating database models:

1. **Update both services** with new model definitions
2. **Test migrations** in development environment
3. **Deploy both services** simultaneously to avoid schema conflicts
4. **Monitor logs** for any database-related errors

---

## 📁 **File Organization**

### **Oracle Eye Structure**
```
oracle-eye/
├── src/
│   ├── main.py                 # Service entry point
│   ├── services/
│   │   ├── telegram_collector.py  # Telegram integration
│   │   └── database.py           # Database operations
│   ├── models/                  # SQLModel data models
│   └── utils/
│       └── config.py            # Configuration management
├── requirements.txt             # Python dependencies
├── env.example                 # Environment template
└── README.md                   # Service documentation
```

### **Neural Core Structure**
```
neural-core/
├── src/
│   ├── main.py                 # Service entry point
│   ├── cli/
│   │   ├── main.py            # CLI application
│   │   └── commands.py        # Command implementations
│   ├── services/
│   │   └── ai_processor.py    # AI processing logic
│   ├── models/                 # SQLModel data models
│   └── utils/
│       └── config.py          # Configuration management
├── requirements.txt            # Python dependencies
├── env.example                # Environment template
└── README.md                  # Service documentation
```

### **Shared Resources**
```
shared/
├── database/                   # SQLite database files
├── logs/                       # Service logs
└── sessions/                   # Telethon session files
```

---

## 🔧 **Configuration Management**

### **Environment Variables**

Each service has its own `.env` file:

**Oracle Eye (.env)**
```bash
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=your_phone
COLLECTION_INTERVAL=86400
COLLECTION_ENABLED=true
MAX_MESSAGES_PER_COLLECTION=1000
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

**Neural Core (.env)**
```bash
OPENAI_API_KEY=your_openai_key
MAX_COST_PER_SUMMARY=10.00
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

### **Database Configuration**

Both services point to the same database:
- **Path**: `../shared/database/crypto_insights.db`
- **Schema**: Managed by SQLModel
- **Access**: Read/Write for Oracle Eye, Read for Neural Core

---

## 🚨 **Common Development Scenarios**

### **Adding New Features**

1. **Identify Service**: Determine which service should handle the feature
2. **Update Models**: Add new database models if needed
3. **Implement Logic**: Add business logic in appropriate service
4. **Update CLI**: Add new commands if user interaction is needed
5. **Test Independently**: Test in isolation first
6. **Integration Test**: Test with both services running

### **Debugging Issues**

1. **Check Logs**: Each service has its own log file
2. **Database State**: Verify data consistency between services
3. **Service Status**: Ensure both services are running
4. **Configuration**: Verify environment variables are correct
5. **Dependencies**: Check if all packages are installed

### **Performance Optimization**

1. **Oracle Eye**: Optimize collection frequency and batch sizes
2. **Neural Core**: Optimize AI processing and caching
3. **Database**: Add indexes and optimize queries
4. **Memory**: Monitor memory usage in both services

---

## 📊 **Monitoring and Logging**

### **Log Files**

- **Oracle Eye**: `../shared/logs/oracle_eye.log`
- **Neural Core**: `../shared/logs/neural_core.log`

### **Key Metrics**

- **Collection Rate**: Messages collected per hour
- **Processing Time**: Summary generation duration
- **Cost Accuracy**: Estimated vs actual costs
- **Error Rates**: Failed operations and recovery

---

## 🔮 **Future Enhancements**

### **Service Independence Benefits**

- **Independent Scaling**: Scale services based on different needs
- **Independent Deployment**: Update one service without affecting the other
- **Independent Testing**: Test services in isolation
- **Independent Monitoring**: Monitor each service's performance separately

### **Planned Improvements**

- **API Layer**: Add REST API for web interface
- **Message Queues**: Use Redis/RabbitMQ for better decoupling
- **Microservices**: Split into smaller, focused services
- **Containerization**: Docker support for easier deployment

---

## 🎯 **Best Practices**

### **Development**

1. **Keep Services Independent**: Avoid direct service-to-service calls
2. **Shared Database Only**: Use database as the single communication point
3. **Consistent Models**: Keep data models synchronized between services
4. **Error Handling**: Implement robust error handling in both services
5. **Logging**: Use structured logging for better debugging

### **Deployment**

1. **Environment Isolation**: Keep Python environments completely separate
2. **Configuration Management**: Use environment-specific .env files
3. **Database Backups**: Regular backups of shared database
4. **Service Monitoring**: Monitor both services independently
5. **Rollback Strategy**: Plan for rolling back individual services

---

**This architecture provides maximum flexibility and maintainability while ensuring reliable operation of both services! 🚀**
