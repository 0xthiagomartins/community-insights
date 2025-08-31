# Project Roadmap — Crypto Community Insights Agent

This roadmap shows the **planned development steps** to build the AI-powered Telegram insights agent.

---

## Phase 1 — Core MVP

**Goal:** Collect Telegram messages, estimate costs, and generate summaries on-demand.  

- [ ] Telegram integration (read messages from selected groups)  
- [ ] SQLite database schema for storing messages and metadata  
- [ ] **Cost estimation function** - calculates LLM processing cost based on message count
- [ ] **Project analysis setup** - one-time analysis of project documentation for context
- [ ] **Checkpoint-based summarization** - summarize specific date ranges with context from previous summaries
- [ ] Basic LLM summarization pipeline (LangChain)  
- [ ] Command-line script to run collection + summary  

**Estimated order:**  
1. Telegram integration  
2. Database design  
3. Cost estimation function
4. Project analysis setup
5. Checkpoint summarization system
6. Summarization pipeline  
7. CLI script  

**Key Features:**
- **Continuous message extraction** and storage in SQLite
- **Cost estimation** before processing (100 messages vs 100,000 messages)
- **On-demand summarization** with date range selection
- **Context-aware summaries** using previous checkpoint data
- **One-time project analysis** from documentation links

---

## Phase 2 — Enhanced Context & Continuity

**Goal:** Improve summarization quality with better context handling.  

- [ ] Store previous summaries in the database  
- [ ] Enhance LLM prompts to consider previous checkpoints  
- [ ] Update digest generation to include continuity and cross-period insights  

**Dependencies:** Phase 1 fully implemented  

---

## Phase 3 — Highlight Linking & Thread Drafts

**Goal:** Add **message links** and **Twitter/X thread generation**.  

- [ ] Extract message links for key highlights  
- [ ] Create thread drafting module based on digest  
- [ ] Optional: export thread draft in JSON/Markdown for review  

**Dependencies:** Phase 1 & Phase 2 completed  

---

## Phase 4 — Automation & Delivery

**Goal:** Fully automated weekly workflow and delivery options.  

- [ ] Scheduler / cron job for continuous message collection  
- [ ] Delivery via email, Telegram, or web dashboard  
- [ ] Optional: auto-preview for thread drafts  

---

## Phase 5 — Advanced Features (Future)

**Goal:** Enhance user experience and insights.  

- [ ] Multi-community tracking  
- [ ] Personalized notifications & alerts  
- [ ] Analytics dashboard (trends, governance metrics, sentiment)  
- [ ] Mobile app or web app interface  

---

## Notes

- Each phase builds on the previous, so the **priority is linear**.  
- MVP can be released internally once Phase 1 is stable.  
- **Cost estimation** is critical for user decision-making on summarization ranges.
- **Project analysis** runs only once per monitored project.
