# Cost Estimation Function

The Crypto Community Insights Agent includes a simple **cost estimation function** that calculates the expected cost of LLM processing based on the number of messages to be summarized.

---

## How It Works

The cost estimation function:

1. **Receives raw messages** extracted from Telegram
2. **Counts total tokens** from all messages in the selected date range
3. **Adds estimated output tokens** for the summary
4. **Calculates processing cost** using current LLM pricing
5. **Returns cost estimate** to help user decide on summarization range

---

## Function Parameters

```python
def estimate_summarization_cost(
    messages: List[Message],
    llm_provider: str = "openai",
    model: str = "gpt-4-turbo"
) -> CostEstimate:
    """
    Estimate the cost of summarizing a collection of Telegram messages.
    
    Args:
        messages: List of raw messages from Telegram
        llm_provider: "openai" or "anthropic"
        model: Specific model name (e.g., "gpt-4-turbo", "claude-3-sonnet")
    
    Returns:
        CostEstimate with total_cost, message_count, cost_per_message
    """
```

---

## Example Usage

### Scenario 1: Small Chat (100 messages)
```python
# Input: 100 messages from a small community
cost = estimate_summarization_cost(messages, "openai", "gpt-4-turbo")
# Output: CostEstimate(total_cost=0.25, message_count=100, cost_per_message=0.0025)
```

### Scenario 2: Large Chat (100,000 messages)
```python
# Input: 100,000 messages from a large community
cost = estimate_summarization_cost(messages, "openai", "gpt-4-turbo")
# Output: CostEstimate(total_cost=250.00, message_count=100000, cost_per_message=0.0025)
```

---

## Cost Estimation Logic

1. **Simple Token Counting**
   - Count total tokens from all messages in the selected date range
   - Add estimated output tokens (~500 tokens for summary)
   - Add context overhead if using previous summaries

2. **Pricing (OpenAI GPT-4 Turbo)**
   - Input tokens: $0.01 per 1K tokens
   - Output tokens: $0.03 per 1K tokens

3. **Simple Cost Calculation**
   ```
   Total Cost = (Total Input Tokens × $0.01/1K) + (Estimated Output Tokens × $0.03/1K)
   ```

---

## User Decision Flow

1. **User selects date range** for summarization
2. **System counts total tokens** in that range
3. **Cost estimation function** calculates expected cost
4. **User sees cost estimate** and can:
   - Proceed with full range
   - Reduce range to lower cost
   - Cancel summarization

---

## Supported Providers

### OpenAI
- GPT-4 Turbo: $0.01/1K input, $0.03/1K output
- GPT-3.5 Turbo: $0.0005/1K input, $0.0015/1K output

### Anthropic
- Claude 3 Sonnet: $0.003/1K input, $0.015/1K output
- Claude 3 Haiku: $0.00025/1K input, $0.00125/1K output

---

## Integration with Checkpoint System

The cost estimation works with the checkpoint summarization system:

- **Previous summaries** are included in context (adds token overhead)
- **New messages only** are counted for cost estimation
- **Context overhead** is added for continuity
- **Total cost** includes both new processing and context inclusion 