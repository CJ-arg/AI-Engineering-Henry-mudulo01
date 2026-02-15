# Technical Report: Legal Derivation AI Assistant

## 1. Architectural Vision
The project is designed as a modular pipeline following the "Separation of Concerns" principle. Each query passes through three distinct stages:
- **Validation Stage**: Uses OpenAI's Moderation API to ensure safety compliance.
- **Inference Stage**: Processes the query using a specialized legal prompt and the `gpt-4o-mini` model.
- **Audit Stage**: Calculates business metrics (latency, tokens, cost) and persists them in a JSON database.



## 2. Prompting Techniques
I implemented **Few-Shot Prompting** as the primary strategy.
- **Why?**: Legal triage requires a specific classification tone. By providing examples of "Labor Law" vs "Civil Law", the model's accuracy increases significantly compared to Zero-Shot.
- **Output Control**: I utilized **JSON Mode** to enforce a strict data contract, ensuring fields like `branch`, `specialist`, and `actions` are always present and correctly typed.

## 3. Metrics Summary
Each execution is recorded with the following data points:
- **Latency (ms)**: To monitor system responsiveness.
- **Token Usage**: Tracking both prompt and completion to understand model efficiency.
- **Estimated Cost**: Calculated using current pricing ($0.15/1M input, $0.60/1M output) to maintain budget control.

## 4. Challenges & Future Improvements
- **Imports in Python**: Managing relative imports between `src/` and `tests/` was solved by using `__init__.py` files and standardizing the execution from the root directory.
- **Future Scope**: Implementation of a **RAG (Retrieval-Augmented Generation)** system would allow the assistant to quote specific legal articles from national codes, moving from a general advisor to a specialized jurisdiction expert.

## 5. Multi-Model Orchestration & Cost-Efficiency
To optimize operational overhead, I transitioned the architecture from a single-model inference to a **hybrid multi-agent pipeline**. 
- **The Filter Agent (Groq/Llama 3.3)**: Acts as a high-speed legal triage layer. It classifies whether a query has legal merit before reaching paid endpoints. This agent handles trivial or non-legal queries with sub-second latency and zero API cost.
- **The Specialist Agent (OpenAI/GPT-4o-mini)**: Serves as the high-reasoning legal consultant. It is only invoked for queries validated by the triage layer, ensuring that expensive compute resources are reserved for complex legal analysis.
- **Unified Observability**: The system now tracks `llm_used` per query, allowing for clear auditing of cost-savings and model performance across different query types.

---
**Author:** Carlos Janon AI Engineering 01
**Date:** February 2026