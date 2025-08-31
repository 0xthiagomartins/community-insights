# Getting Started

Welcome! 🎉  
This guide will help you set up and start using the **Crypto Community Insights Agent**.  
In just a few minutes, you'll start monitoring Telegram communities with AI-powered summaries.

---

## 1. Prerequisites

Before starting, make sure you have:

- ✅ A Telegram account  
- ✅ The Telegram group/channel you want to monitor  
- ✅ A link to the project's documentation (website, whitepaper, GitHub, etc.)
- ✅ An OpenAI API key (or other LLM provider)
- ✅ (Optional) A Twitter/X account if you want automatic thread generation  

---

## 2. Setup

1. **Project Setup**  
   - Provide the Telegram group link you want to monitor
   - Add a link to the project's documentation
   - The system will analyze the documentation once to understand the project context

2. **Configure AI Services**  
   - Add your OpenAI API key
   - System uses ChatGPT by default (other models in future updates)

3. **Start Monitoring**  
   - The system begins continuous message collection automatically
   - Messages are stored in SQLite database
   - You can request summaries anytime from available chats

---

## 3. System Workflow

**Continuous (Our System):**
- Messages are automatically collected from Telegram groups
- Stored in SQLite with timestamps
- No processing costs incurred during collection

**On-Demand (When You Want):**
- Select a date range for summarization
- System estimates the cost based on message count
- You can adjust the range if cost is too high
- Summary is generated with context from previous summaries

---

## 4. Example Usage

**Setting up a project:**
```bash
# Setup monitoring for Uniswap
setup_project(
    telegram_group="https://t.me/uniswap",
    project_docs="https://docs.uniswap.org",
    project_name="Uniswap"
)
```

**Requesting a summary:**
```bash
# Get summary for last 7 days
summary = request_summary(
    project_name="Uniswap",
    date_range=("2024-01-01", "2024-01-07")
)

# System shows: "Estimated cost: $2.50 for 1,200 messages"
# You can proceed or adjust the date range
```

**Output Example:**
```
📊 Uniswap Summary (Jan 1-7, 2024)

🔑 Key Updates:
- New governance proposal #123 submitted
- Mobile app beta testing expanded to 10,000 users
- Partnership with DeFi protocol announced

💰 Cost Report:
- Messages processed: 1,200
- Actual cost: $2.45
- Cost per message: $0.002
```

---

## 5. Key Features

- **Cost Estimation**: Know the cost before processing
- **Checkpoint System**: Each summary builds on previous ones
- **Project Context**: One-time analysis of project documentation
- **Flexible Ranges**: Choose any date range for summarization
- **SQLite Storage**: Efficient local data storage

---

## 6. Next Steps

- Monitor your first project
- Request summaries when you need them
- Adjust date ranges based on cost estimates
- Share insights via optional Twitter/X threads

---

✨ That's it! You're ready to start monitoring crypto communities efficiently.
