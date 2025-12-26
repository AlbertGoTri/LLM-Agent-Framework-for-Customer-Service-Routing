# LLM Agent Framework for Customer Service Routing

A Python framework that uses Large Language Models (LLMs) to intelligently route customer queries to specialized agents.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AlbertGoTri/LLM-Agent-Framework-for-Customer-Service-Routing.git
cd LLM-Agent-Framework-for-Customer-Service-Routing
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
Edit the `environment.env` file with your API keys:
```env
GOOGLE_API_KEY=your-google-api-key
GROQ_API_KEY=your-groq-api-key
```

### 5. Run the chat system
```bash
python src/main.py groq    # Using Groq (Llama 3.1 8B)
python src/main.py google  # Using Google (Gemini 2.5 Flash)
```

### 6. Run the evaluation
```bash
python evaluation/evaluate.py groq
python evaluation/evaluate.py google
```

## Project Structure

```
NordHealth-Assignment/
├── src/                      # Source code
│   ├── main.py               # Entry point - interactive chat
│   ├── router.py             # LLM-based query router
│   └── agents.py             # FAQ and Order agents
├── evaluation/               # Evaluation module
│   ├── evaluate.py           # Evaluation script
│   ├── test_data.py          # Test dataset (30 queries)
│   └── results/              # JSON output files
├── environment.env           # API keys
├── requirements.txt          # Dependencies
└── README.md
```

## Evaluation

### Evaluation Criteria

| Criterion   | Description                                | Weight |
|-------------|--------------------------------------------|--------|
| Accuracy    | Percentage of correctly classified intents | High   |
| Latency     | Average response time in milliseconds      | Medium |
| Error Rate  | Number of failed API calls                 | Medium |
| Cost        | Free tier availability and limits          | Medium |

### Model Comparison Results

| Provider | Model                | Tests | Accuracy | Avg Latency | Errors |
|----------|----------------------|-------|----------|-------------|--------|
| Google   | gemini-2.5-flash     | 15    | 100.00%  | 627 ms      | 0      |
| Groq     | llama-3.1-8b-instant | 30    | 96.67%   | 180 ms      | 1      |

**Notes:**
- Google Gemini was only tested on 15 out of 30 queries due to daily quota limitations (20 requests/day on the free tier).
- Groq was tested on the full 30-query dataset. The single error was an edge case query ("What happens if my package is lost?") that was ambiguously classified as ORDER instead of FAQ.
- No other LLMs were tested because no free API keys were available for other providers.

## Conclusion

**Best Model: Google Gemini 2.5 Flash**

Gemini achieved 100% accuracy on all tested queries, correctly classifying every FAQ intent. However, it has significant limitations:
- Restricted to 20 requests/day on the free tier
- Higher latency (627 ms vs 180 ms)

**Alternative: Groq Llama 3.1 8B Instant**

Groq achieved 96.67% accuracy with only one edge case misclassification. It offers:
- Generous free tier with no daily limits encountered
- Faster inference (~3.5x faster than Gemini)
- Full evaluation completed without rate limiting

**Recommendation:** For production use with a paid plan, Gemini is recommended due to its higher accuracy. For development or free-tier usage, Groq is the practical choice due to its generous quotas and fast response times.