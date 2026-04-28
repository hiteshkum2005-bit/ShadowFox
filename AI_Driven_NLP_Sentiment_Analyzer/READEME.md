# AI-Driven NLP Sentiment Analyzer

## 1. Project Overview
This project implements an advanced Natural Language Processing (NLP) pipeline using **LangChain** and **Google Gemini 2.0**. Unlike traditional sentiment tools, this system uses Large Language Models (LLMs) to detect sarcasm, emotional intensity, and complex reasoning.

## 2. LM Selection
- **Model:** `gemini-2.0-flash`
- **Reasoning:** Selected for its high reasoning capabilities in 2026, low latency, and superior performance in detecting "implicit" sentiment (sarcasm) compared to older BERT-based models.

## 3. Research Questions
1. **Sarcasm Detection:** Can the LLM accurately identify irony when positive keywords (e.g., "Great", "Wonderful") are used in a negative context?
2. **Explainability:** How well can the model provide human-readable reasoning for its sentiment scores?
3. **Structured Extraction:** Can we consistently transform unstructured reviews into valid JSON/Dataframes for business analysis?

## 4. Implementation Details
The project is built in a Jupyter Notebook using:
- **Pydantic:** To enforce a strict data schema for the AI output.
- **LCEL (LangChain Expression Language):** To chain the prompt and the model efficiently.
- **Pandas:** To visualize the final sentiment analysis in a structured table.

## 5. Key Findings & Insights
- **Context over Keywords:** The model successfully identified sarcasm in cases where traditional models failed.
- **Nuance:** The system distinguished between "Mixed" and "Neutral" sentiments, providing a more granular 1-10 scoring system.
- **Efficiency:** Using a "Flash" model allowed for near-instant analysis without sacrificing accuracy.

## 6. Ethical Considerations
- **Data Privacy:** This project is designed to redact PII (Personally Identifiable Information) before processing.
- **Bias Awareness:** Recognizes that sentiment varies across cultures; the "Reasoning" field helps audit the AI for potential biases.

## 7. How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Get a Google AI Studio API Key.
3. Open `notebooks/sentiment_analysis.ipynb` and run the cells.