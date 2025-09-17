# Project Roadmap — Crypto Community Insights Agent

This roadmap shows the **planned development steps** to build the AI-powered Telegram insights agent with **decoupled services**.

---

## Phase 1 — Core MVP (6 weeks)

**Goal:** Build two independent services that communicate via shared database.

### **Oracle Eye Service (Python Environment 1)**
- [ ] **Telegram integration** via Telethon (read messages from public groups)
- [ ] **SQLite database schema** for storing messages and metadata
- [ ] **Automatic message collection** - daily collection with checkpoint system
- [ ] **Background scheduler** for continuous operation
- [ ] **Independent service** that runs continuously

### **Neural Core Service (Python Environment 2)**
- [ ] **Cost estimation function** - calculates LLM processing cost based on message count
- [ ] **LangChain integration** - intelligent AI orchestration for summarization
- [ ] **CLI interface** with Typer for user interaction
- [ ] **On-demand processing** - runs only when CLI commands are executed

**Estimated order:**  
1. Oracle Eye: Telegram integration + database design
2. Oracle Eye: Automatic collection system
3. Neural Core: Cost estimation function
4. Neural Core: CrewAI summarization pipeline
5. Neural Core: CLI interface
6. Integration testing with shared database

**Key Features:**
- **Decoupled services** - each runs in its own Python environment
- **Shared database** - enables loose coupling between services
- **Automatic collection** and storage in SQLite (Oracle Eye)
- **Cost estimation** before processing (Neural Core)
- **On-demand summarization** with date range selection (Neural Core)
- **CrewAI processing** for optimal AI orchestration (Neural Core)
- **Simple markdown output** without complex context

---

## Phase 2 — Enhanced Features (Future)

**Goal:** Improve functionality with advanced features while maintaining service independence.

### **Oracle Eye Enhancements**
- [ ] **Advanced scheduling** options and monitoring
- [ ] **Performance optimization** for large message volumes
- [ ] **Health monitoring** and automatic recovery

### **Neural Core Enhancements**
- [ ] Store previous summaries in the database for context
- [ ] Project documentation analysis for better understanding
- [ ] Message linking to original Telegram messages
- [ ] Twitter/X thread generation from summaries

**Dependencies:** Phase 1 fully implemented and validated

---

## Phase 3 — Automation & Delivery (Future)

**Goal:** Fully automated workflow and delivery options.

- [ ] **Oracle Eye**: Advanced scheduler / cron job for continuous message collection
- [ ] **Neural Core**: Delivery via email, Telegram, or web dashboard
- [ ] **Shared**: Advanced analytics and metrics

---

## Phase 4 — Advanced Features (Future)

**Goal:** Enhance user experience and insights while maintaining service independence.

- [ ] **Multi-community tracking** across both services
- [ ] **Personalized notifications & alerts**
- [ ] **Analytics dashboard** (trends, governance metrics, sentiment)
- [ ] **Mobile app or web app interface**

---

## Service Independence Benefits

- **🔄 Independent Development**: Teams can work on each service separately
- **🚀 Independent Deployment**: Deploy updates to one service without affecting the other
- **🧪 Independent Testing**: Test each service in isolation
- **📊 Independent Scaling**: Scale services based on different resource needs
- **🔧 Independent Maintenance**: Update dependencies and configurations separately

---

## Notes

- **MVP focus:** Two independent services communicating via shared database
- **Phase 1 priority:** Get both services working independently with real data
- **Service communication:** Only through shared database, no direct API calls
- **Cost estimation** is critical for user decision-making on summarization ranges
- **Project analysis** and advanced features moved to Phase 2+
