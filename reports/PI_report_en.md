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

---
**Author:** Carlos Janon AI Engineering 01
**Date:** February 2026