# Project Roadmap — Crypto Community Insights Agent

This roadmap shows the **planned development steps** to build the AI-powered Telegram insights agent.

---

## Phase 1 — Core MVP (6 weeks)

**Goal:** Collect Telegram messages automatically, estimate costs, and generate summaries on-demand using CrewAI.

- [ ] Telegram integration via Telethon (read messages from public groups)
- [ ] SQLite database schema for storing messages and metadata
- [ ] **Cost estimation function** - calculates LLM processing cost based on message count
- [ ] **Automatic message collection** - daily collection with checkpoint system
- [ ] **CrewAI integration** - intelligent AI orchestration for summarization
- [ ] **Basic CLI interface** with Typer for user interaction

**Estimated order:**  
1. Telegram integration (Telethon)
2. Database design
3. Cost estimation function
4. Automatic collection system
5. CrewAI summarization pipeline
6. CLI interface

**Key Features:**
- **Automatic message collection** and storage in SQLite
- **Cost estimation** before processing (100 messages vs 100,000 messages)
- **On-demand summarization** with date range selection
- **CrewAI processing** for optimal AI orchestration
- **Simple markdown output** without complex context

---

## Phase 2 — Enhanced Features (Future)

**Goal:** Improve functionality with advanced features.

- [ ] Store previous summaries in the database for context
- [ ] Project documentation analysis for better understanding
- [ ] Message linking to original Telegram messages
- [ ] Twitter/X thread generation from summaries

**Dependencies:** Phase 1 fully implemented and validated

---

## Phase 3 — Automation & Delivery (Future)

**Goal:** Fully automated workflow and delivery options.

- [ ] Scheduler / cron job for continuous message collection
- [ ] Delivery via email, Telegram, or web dashboard
- [ ] Advanced analytics and metrics

---

## Phase 4 — Advanced Features (Future)

**Goal:** Enhance user experience and insights.

- [ ] Multi-community tracking
- [ ] Personalized notifications & alerts
- [ ] Analytics dashboard (trends, governance metrics, sentiment)
- [ ] Mobile app or web app interface

---

## Notes

- **MVP focus:** Automatic collection + CrewAI summarization + cost control
- **Phase 1 priority:** Get core functionality working with real data
- **Cost estimation** is critical for user decision-making on summarization ranges
- **Project analysis** and advanced features moved to Phase 2+
