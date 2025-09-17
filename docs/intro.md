# Crypto Community Insights Agent

## Overview

**Solution:** AI agent that monitors crypto communities on Telegram and generates intelligent summaries of the most important discussions.

**Problem:** Crypto communities generate hundreds of messages per day. It's impossible to keep up manually, missing opportunities and staying out of the loop.

**Solution:** Two independent services - automatic message collection (Oracle Eye) + AI processing (Neural Core) - communicating via shared database.

---

## What it does

1. **Oracle Eye Service**: Automatically collects messages from public Telegram groups
2. **Neural Core Service**: Processes data via LangChain to identify what's important
3. **Shared Database**: Enables loose coupling between services
4. **Structured Output**: Easy-to-read summaries in markdown format
5. **Cost Control**: Transparent cost estimation before processing
6. **Simple Interface**: Command line interface for user interaction

---

## Service Architecture

### **🔄 Oracle Eye (Service 1)**
- **Purpose**: Continuous message collection
- **Operation**: Runs independently in background
- **Technology**: Telethon, SQLModel, Background Scheduler
- **Communication**: Writes to shared database

### **🤖 Neural Core (Service 2)**
- **Purpose**: AI processing and user interface
- **Operation**: Runs on-demand via CLI commands
- **Technology**: LangChain, Typer, SQLModel
- **Communication**: Reads from shared database

---

## Target audience

- **Investors** who need to track projects
- **Analysts** who monitor crypto communities
- **Content creators** who share project updates
- **Contributors** who follow project discussions

---

## Competitive advantage

- **Service Independence**: Each service runs in its own Python environment
- **Full Automation**: Oracle Eye collects messages continuously
- **Smart AI**: CrewAI optimizes processing in Neural Core
- **Cost Transparency**: Know the cost before processing
- **Loose Coupling**: Services communicate only through database
- **Scalability**: Deploy services on different machines if needed

---

## Result

Instead of reading 1000+ messages per week, you receive a structured summary with the most important points, saving time and not missing relevant information. The system operates reliably with independent services that can be maintained and scaled separately.
