# Project Analysis System

The Crypto Community Insights Agent includes a **one-time project analysis system** that understands the project context from documentation to improve summarization quality.

---

## What is Project Analysis?

When you start monitoring a new Telegram group, you provide a link to the project's documentation (website, whitepaper, GitHub, etc.). The system analyzes this documentation once to understand:

- **Project purpose and goals**
- **Key terminology and concepts**
- **Team structure and roles**
- **Technical architecture**
- **Community governance model**
- **Recent developments and roadmap**

This analysis is stored permanently and used as context for all future summaries.

---

## How It Works

### 1. Documentation Input
```python
def setup_project_monitoring(
    telegram_group: str,
    project_docs_url: str,
    project_name: str
) -> ProjectAnalysis:
    """
    Set up monitoring for a new project.
    
    Args:
        telegram_group: Telegram group/channel link
        project_docs_url: URL to project documentation
        project_name: Human-readable project name
    
    Returns:
        ProjectAnalysis with extracted context
    """
```

### 2. Analysis Process
1. **Documentation Scraping**: Extracts text from the provided URL
2. **Content Analysis**: LLM processes the documentation to understand the project
3. **Context Extraction**: Identifies key concepts, terminology, and structure
4. **Storage**: Saves analysis in SQLite database
5. **Reuse**: Analysis is used in all future summarization prompts

### 3. Context Integration
The extracted project context is included in every summarization prompt:

```
Context: This is a DeFi lending protocol focused on cross-chain liquidity. 
Key concepts: liquidity pools, yield farming, governance tokens.
Recent focus: mobile app development and partnership announcements.

Summarize the following Telegram messages with this context in mind...
```

---

## Example Analysis Output

### Input: Uniswap Documentation
**Extracted Context:**
- **Project Type**: Decentralized exchange (DEX)
- **Key Concepts**: Automated market making (AMM), liquidity pools, impermanent loss
- **Governance**: UNI token holders vote on proposals
- **Recent Focus**: Layer 2 scaling, mobile app development
- **Technical Stack**: Smart contracts on Ethereum, Polygon, Arbitrum

### Usage in Summarization
When summarizing Uniswap Telegram messages, the system will:
- Understand discussions about "impermanent loss" and "liquidity pools"
- Recognize governance proposal discussions
- Contextualize technical updates about scaling solutions
- Provide more accurate and relevant summaries

---

## Database Schema

```sql
CREATE TABLE project_analyses (
    id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    telegram_group TEXT NOT NULL,
    docs_url TEXT NOT NULL,
    analysis_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE summaries (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    date_range_start DATE,
    date_range_end DATE,
    summary_text TEXT,
    cost_estimate REAL,
    actual_cost REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project_analyses(id)
);
```

---

## Benefits

### 1. Better Summarization Quality
- **Context-aware** summaries that understand project-specific terminology
- **Accurate interpretation** of technical discussions
- **Relevant highlights** based on project goals and focus areas

### 2. Efficiency
- **One-time analysis** per project, not per summary
- **Reusable context** for all future summaries
- **Reduced token usage** by not re-analyzing project basics

### 3. Consistency
- **Standardized understanding** of each project
- **Consistent terminology** across summaries
- **Aligned focus** with project objectives

---

## Supported Documentation Sources

- **Project Websites**: Official project websites and landing pages
- **Whitepapers**: Technical documentation and tokenomics
- **GitHub Repositories**: Code documentation and README files
- **Medium/Blog Posts**: Project updates and announcements
- **Documentation Sites**: Technical docs, API references, etc.

---

## Analysis Limitations

- **Static Analysis**: Only analyzes documentation at setup time
- **Manual Updates**: Project analysis doesn't auto-update
- **URL Dependency**: Requires accessible documentation URL
- **Language Support**: Currently optimized for English documentation

---

## Future Enhancements

- **Periodic Re-analysis**: Auto-update project context quarterly
- **Multi-language Support**: Analyze documentation in multiple languages
- **Dynamic Context**: Include recent developments in context
- **Community Feedback**: Allow users to refine project understanding 