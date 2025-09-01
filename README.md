# 🧠 Crypto Community Insights Agent

> **Transform crypto community noise into actionable insights through AI.**

An AI-powered agent that monitors Telegram communities, estimates costs, and generates intelligent summaries on-demand using cutting-edge AI technology.

---

## 🎯 **Value Proposition**

### **The Problem**
Crypto projects evolve rapidly, and communities generate **hundreds of messages per day**. It's **impossible to keep up manually**, leading to:
- **Missing opportunities** and staying out of the loop
- **Information overload** from endless scrolling
- **Unpredictable costs** with AI processing
- **Time wasted** on manual community monitoring

### **The Solution**
Our agent provides **automated message collection and cost-controlled AI summarization**:
- **Automatic collection** of messages via Telegram (Telethon)
- **Intelligent AI processing** via CrewAI for optimal results
- **Transparent cost control** before processing
- **Simple command-line interface** for easy interaction

---

## 🚀 **Overview**

This project solves the crypto community monitoring challenge by **automating message collection and providing intelligent summarization** on demand.

- 📱 **Daily Collection**: Automatically extracts messages from selected Telegram groups
- 💾 **Smart Storage**: SQLite database with SQLModel ORM for efficient data management
- 💰 **Cost Control**: Estimates LLM processing costs before summarization
- 🤖 **AI Intelligence**: CrewAI orchestrates the summarization process
- 📊 **Structured Output**: Clean, organized summaries in markdown format
- ⚡ **Real-time Processing**: On-demand summaries for any date range

---

## ✨ **Key Features**

### **Core MVP Features**
- **🔄 Automatic Message Collection**: Daily collection from public Telegram groups using Telethon
- **💰 Cost Estimation**: Calculates expected processing costs before summarization
- **🤖 AI-Powered Summaries**: CrewAI generates intelligent, structured summaries
- **📊 Flexible Date Ranges**: Choose any period for summarization based on cost estimates
- **💾 Local Database**: SQLite storage with SQLModel for efficient data management
- **💻 Command Line Interface**: Simple Typer-based CLI for all operations

### **Future Features (Phase 2+)**
- **📚 Project Analysis**: One-time analysis of project documentation for better context
- **🔗 Message Linking**: Direct links to important Telegram messages
- **🐦 Twitter Threads**: Automatic generation of shareable content
- **📈 Analytics Dashboard**: Metrics and insights from community monitoring

---

## 🏗️ **Architecture**

### **High-Level System Design**
```
┌─────────────────────────────────────────────────────────────┐
│                    SINGLE PYTHON ENVIRONMENT                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │   SERVICE 1     │    │           SERVICE 2             │ │
│  │  ORACLE EYE     │    │      NEURAL CORE                │ │
│  │                 │    │                                 │ │
│  │ • Telethon      │    │ • CrewAI                        │ │
│  │ • Scheduler     │    │ • Cost Estimation               │ │
│  │ • SQLModel      │    │ • Summary Generation            │ │
│  │ • Background    │    │ • CLI Interface                 │ │
│  └─────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Data Flow**
```
Telegram Groups → Telethon Collection → SQLModel ORM → CrewAI Processing → Markdown Output
```

---

## 💰 **Business Model**

### **Target Audience**
- **🎯 Investors** who need to monitor multiple crypto projects
- **📊 Market Analysts** who track community sentiment and updates
- **📝 Content Creators** who share project updates with their audience
- **🔧 Project Contributors** who want to stay informed about discussions

### **Competitive Advantages**
- **🚀 Full Automation**: No manual intervention required for message collection
- **🤖 Optimized AI**: CrewAI provides superior summarization quality
- **💰 Cost Transparency**: Know the exact cost before processing
- **⚡ Setup in Minutes**: Simple configuration and immediate operation
- **🔒 Privacy First**: Local data storage, no external dependencies

---

## 🛠️ **Technology Stack**

### **Core Technologies**
- **📱 Telegram Integration**: [Telethon](https://docs.telethon.dev/) (official API)
- **🤖 AI Orchestration**: [CrewAI](https://docs.crewai.com/) (intelligent agent coordination)
- **💻 User Interface**: [Typer](https://typer.tiangolo.com/) (modern CLI framework)
- **🗄️ Database**: [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic)
- **💾 Storage**: SQLite (local, efficient, no external dependencies)

### **Development Tools**
- **🐍 Python 3.8+**: Modern Python with async/await support
- **📦 Package Management**: pip with requirements.txt
- **🔧 Configuration**: python-dotenv for environment variables
- **📝 Logging**: Structured logging with rotation

---

## 🚀 **Development Roadmap**

### **Phase 1 - MVP (6 weeks)**
- ✅ **Week 1-2:** Basic structure + CLI interface
- **Week 3-4:** Automatic collection + AI processing
- **Week 5-6:** Validation + adjustments

### **Phase 2 - Enhanced Features (Future)**
- **📚 Project Documentation Analysis**: Better context understanding
- **🔗 Message Linking**: Direct access to original messages
- **🐦 Twitter Thread Generation**: Shareable content creation
- **📊 Advanced Analytics**: Metrics and insights dashboard

---

## 📊 **Success Metrics**

### **Technical Metrics**
- ✅ **Automatic Collection**: Daily message collection working reliably
- ✅ **Summary Quality**: High-quality, actionable summaries
- ✅ **Cost Accuracy**: Estimates within 10% of actual costs
- ✅ **Performance**: Fast processing and response times

### **Business Metrics**
- ⏰ **Time Saved**: Hours of manual reading eliminated per user
- 📈 **Information Quality**: Better insights from community monitoring
- 💰 **Cost Efficiency**: Predictable and controlled AI processing costs
- 🎯 **User Adoption**: Active usage and positive feedback

---

## 🚀 **Getting Started**

### **Quick Start**
```bash
# 1. Clone the repository
git clone <repository-url>
cd crypto-insights

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run the system
python src/main.py
```

### **Basic Usage**
```bash
# Setup a project for monitoring
setup-project --name "Uniswap" --group "uniswap"

# Generate a summary for the last 7 days
generate-summary --project "Uniswap" --days 7

# Estimate processing cost
estimate-cost --project "Uniswap" --days 7
```

---

## 🔧 **Configuration**

### **Required Environment Variables**
```bash
# Telegram API (get from https://my.telegram.org/)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=your_phone

# OpenAI API (for CrewAI)
OPENAI_API_KEY=your_openai_key

# Optional configurations
COLLECTION_INTERVAL=86400          # 24 hours in seconds
MAX_COST_PER_SUMMARY=10.00        # Maximum cost per summary
DATABASE_URL=sqlite:///crypto_insights.db
```

---

## 📁 **Project Structure**
```
crypto-insights/
├── src/
│   ├── main.py                 # Main entry point
│   ├── services/               # Core services
│   ├── models/                 # SQLModel data models
│   ├── utils/                  # Utilities and config
│   └── cli/                    # Command-line interface
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
└── README.md                  # This file
```

---

## 🧪 **Testing**

### **Testing Oracle Eye**
```bash
# Activate Oracle Eye environment
cd oracle-eye
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### **Testing Neural Core**
```bash
# Activate Neural Core environment
cd neural-core
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### **Integration Testing**
```bash
# Test both services with shared database
# 1. Start Oracle Eye in one terminal
cd oracle-eye
python src/main.py

# 2. Test Neural Core in another terminal
cd neural-core
python -m cli.main setup-project --name "Test" --group "test_group"
```

---

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements
- Pull request process
- Development setup

---

This project represents a **unique opportunity** to automate crypto community intelligence using cutting-edge AI technology. By combining **Telethon automation**, **CrewAI intelligence**, and **SQLModel efficiency**, we create a powerful tool that can **scale rapidly** and generate **significant value** for users who need to track multiple projects simultaneously.
