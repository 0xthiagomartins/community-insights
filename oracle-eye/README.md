# 🔄 Oracle Eye Service

> **Continuous message collection from Telegram communities**

The Oracle Eye Service is responsible for **automatically collecting messages** from configured Telegram groups and storing them in a shared database for processing by the Neural Core.

---

## 🎯 **Purpose**

- **Continuous Operation**: Runs independently in the background
- **Message Collection**: Automatically extracts text and links from Telegram
- **Data Storage**: Saves messages to shared SQLite database
- **Checkpoint System**: Efficient collection based on last message ID

---

## 🏗️ **Architecture**

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
```

---

## 🚀 **Quick Start**

```bash
# 1. Navigate to Oracle Eye directory
cd oracle-eye

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.example .env
# Edit .env with your Telegram credentials

# 5. Start the service
python src/main.py
```

---

## ⚙️ **Configuration**

### **Required Environment Variables**
```bash
# Telegram API (get from https://my.telegram.org/)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=your_phone

# Collection settings
COLLECTION_INTERVAL=86400          # 24 hours in seconds
COLLECTION_ENABLED=true
MAX_MESSAGES_PER_COLLECTION=1000

# Database (shared with Neural Core)
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

---

## 📁 **Project Structure**

```
oracle-eye/
├── src/
│   ├── main.py                 # Service entry point
│   ├── services/               # Collection services
│   │   ├── telegram_collector.py
│   │   └── database.py
│   ├── models/                 # SQLModel data models
│   └── utils/                  # Configuration
├── requirements.txt            # Python dependencies
├── env.example                # Environment template
└── README.md                  # This file
```

---

## 🔄 **Operation**

### **Continuous Collection Loop**
1. **Start**: Service initializes and connects to Telegram
2. **Collect**: Extracts messages from all active projects
3. **Store**: Saves messages to shared database
4. **Wait**: Sleeps for configured interval (default: 24 hours)
5. **Repeat**: Continues collection cycle indefinitely

### **Checkpoint System**
- Remembers last collected message ID per project
- Only collects new messages since last collection
- Prevents duplicate collection and improves efficiency

---

## 📊 **Monitoring**

### **Logs**
- **Location**: `../shared/logs/oracle_eye.log`
- **Level**: INFO with structured formatting
- **Rotation**: Automatic log file management

### **Health Checks**
- Database connection status
- Telegram API connectivity
- Collection cycle completion
- Error handling and recovery

---

## 🛠️ **Development**

### **Testing**
```bash
# Activate environment
source venv/bin/activate

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### **Adding New Features**
- **New Collection Sources**: Extend `telegram_collector.py`
- **Data Processing**: Add new models in `models/`
- **Configuration**: Extend `utils/config.py`

---

## 🔗 **Integration**

### **With Neural Core**
- **Communication**: Via shared SQLite database
- **Data Flow**: Oracle Eye writes → Neural Core reads
- **No Direct Calls**: Loose coupling through database

### **Shared Resources**
- **Database**: `../shared/database/`
- **Logs**: `../shared/logs/`
- **Sessions**: `../shared/sessions/` (Telethon)

---

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Telegram API Limits**: Respect rate limits and collection intervals
2. **Database Lock**: Ensure only one instance runs per database
3. **Session Expiry**: Telethon sessions may need re-authentication

### **Recovery**
- **Automatic**: Service attempts recovery on errors
- **Manual**: Restart service if persistent issues
- **Logs**: Check logs for detailed error information

---

## 📈 **Performance**

### **Optimization Tips**
- **Collection Interval**: Adjust based on message volume
- **Batch Processing**: Process messages in batches
- **Database Indexing**: Ensure proper database indexes
- **Memory Management**: Monitor memory usage during collection

---

**Oracle Eye runs independently, ensuring continuous data collection for the crypto insights system! 🔄**
