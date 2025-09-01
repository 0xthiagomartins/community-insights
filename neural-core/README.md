# 🤖 Neural Core Service

> **AI-powered processing and command-line interface for crypto insights**

The Neural Core Service provides **intelligent AI processing** and a **user-friendly CLI interface** for generating insights from collected Telegram messages.

---

## 🎯 **Purpose**

- **AI Processing**: CrewAI-powered summarization and analysis
- **User Interface**: Typer-based command-line interface
- **Cost Control**: Estimates and manages processing costs
- **Data Access**: Reads from shared database (populated by Oracle Eye)

---

## 🏗️ **Architecture**

```
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
```

---

## 🚀 **Quick Start**

```bash
# 1. Navigate to Neural Core directory
cd neural-core

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.example .env
# Edit .env with your OpenAI API key

# 5. Start CLI interface
python -m cli.main
```

---

## ⚙️ **Configuration**

### **Required Environment Variables**
```bash
# OpenAI API (for CrewAI)
OPENAI_API_KEY=your_openai_key

# Cost control
MAX_COST_PER_SUMMARY=10.00        # Maximum cost per summary

# Database (shared with Oracle Eye)
DATABASE_URL=sqlite:///../shared/database/crypto_insights.db
```

---

## 📁 **Project Structure**

```
neural-core/
├── src/
│   ├── main.py                 # Service entry point
│   ├── cli/                    # Command-line interface
│   │   ├── main.py            # CLI application
│   │   └── commands.py        # Command implementations
│   ├── services/               # AI processing services
│   │   └── ai_processor.py
│   ├── models/                 # SQLModel data models
│   └── utils/                  # Configuration
├── requirements.txt            # Python dependencies
├── env.example                # Environment template
└── README.md                  # This file
```

---

## 💻 **CLI Commands**

### **Project Management**
```bash
# Setup new project for monitoring
setup-project --name "Uniswap" --group "uniswap"

# List all configured projects
list-projects

# Update project configuration
update-project --project "Uniswap" --new-group "uniswap_v2"
```

### **AI Processing**
```bash
# Estimate processing cost
estimate-cost --project "Uniswap" --days 7

# Generate summary
generate-summary --project "Uniswap" --days 7

# Save summary to file
generate-summary --project "Uniswap" --days 7 --output summary.md
```

---

## 🤖 **AI Processing**

### **CrewAI Integration**
- **Agent Orchestration**: Intelligent coordination of AI agents
- **Context Management**: Efficient handling of large message volumes
- **Quality Optimization**: Best practices for summarization

### **Cost Estimation**
- **Token Counting**: Accurate estimation of input/output tokens
- **Provider Support**: OpenAI, Anthropic, and other LLM providers
- **Cost Control**: Prevents unexpected expenses

### **Summary Generation**
- **Structured Output**: Clean, organized markdown summaries
- **Relevance Filtering**: AI identifies important content
- **Noise Reduction**: Filters spam and irrelevant messages

---

## 🔗 **Integration**

### **With Oracle Eye**
- **Communication**: Via shared SQLite database
- **Data Flow**: Oracle Eye writes → Neural Core reads
- **No Direct Calls**: Loose coupling through database

### **Shared Resources**
- **Database**: `../shared/database/`
- **Logs**: `../shared/logs/`

---

## 📊 **Monitoring**

### **Logs**
- **Location**: `../shared/logs/neural_core.log`
- **Level**: INFO with structured formatting
- **Content**: CLI operations, AI processing, cost tracking

### **Performance Metrics**
- **Processing Time**: Summary generation duration
- **Cost Accuracy**: Estimated vs actual costs
- **User Interactions**: CLI command usage patterns

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

### **Adding New Commands**
1. **Define Function**: Add new command function in `commands.py`
2. **Register Command**: Add to `main.py` with `@app.command()`
3. **Implement Logic**: Use existing services or create new ones
4. **Add Tests**: Ensure proper testing coverage

### **Extending AI Processing**
- **New Models**: Add support for additional LLM providers
- **Custom Agents**: Extend CrewAI with specialized agents
- **Output Formats**: Support additional output formats beyond markdown

---

## 🚨 **Troubleshooting**

### **Common Issues**
1. **OpenAI API Limits**: Check API key and rate limits
2. **Database Access**: Ensure shared database is accessible
3. **Memory Usage**: Large message volumes may require optimization

### **Recovery**
- **API Errors**: Automatic retry with exponential backoff
- **Database Issues**: Graceful error handling and user feedback
- **Cost Limits**: Automatic cancellation if cost exceeds limits

---

## 📈 **Performance**

### **Optimization Tips**
- **Batch Processing**: Process multiple projects efficiently
- **Caching**: Cache frequently accessed data
- **Async Operations**: Use async/await for I/O operations
- **Memory Management**: Monitor memory usage during AI processing

---

## 🔮 **Future Enhancements**

### **Planned Features**
- **Project Analysis**: One-time documentation analysis for context
- **Message Linking**: Direct links to original Telegram messages
- **Twitter Threads**: Automatic social media content generation
- **Analytics Dashboard**: Metrics and insights visualization

---

**Neural Core provides intelligent AI processing with a simple CLI interface for crypto community insights! 🤖**
