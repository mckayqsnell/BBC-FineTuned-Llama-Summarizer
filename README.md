# News Summarization with Fine-Tuned Llama

This project focuses on **fine-tuning** a Llama 1B model to generate concise, high-quality summaries for news articles. By refining an already capable language model, the goal is to **retain key information** from articles while producing more **coherent** and **domain-specific** summaries.

## Project Overview

- **Dataset**: BBC News (2000+ articles), each with a reference summary. Articles are about 800–1000 tokens; summaries ~300–400 tokens.  
- **Objective**: Compare **base Llama 1B** vs. **fine-tuned** Llama 1B in summarizing news articles, measuring improvements in **BLEU** and **ROUGE** scores.

## Model & Fine-Tuning

- **Model**: Llama 1B, selected for feasible hardware constraints.  
- **Prompt Engineering**:  
  - **Training Prompt** includes article + reference summary; only the summary tokens contribute to the training loss (prompt tokens are ignored).  
  - **Inference Prompt**: “Summarize the following article:” + article content, then model generates the summary.  
- **Training Details**:  
  - **Batch size = 1** (memory limitations).  
  - **3 epochs** at `5e-5` learning rate.  
  - Dynamic truncation to fit long articles + reference summaries.

## Results

| Metric     | Base Llama | Fine-Tuned Llama |
|------------|------------|------------------|
| **BLEU**   | 0.290      | 0.450            |
| **ROUGE1** | 0.424      | 0.607            |
| **ROUGE2** | 0.280      | 0.556            |
| **ROUGEL** | 0.260      | 0.472            |
| **ROUGELsum** | 0.271      | 0.473            |

- Fine-tuning yields **significant** improvements in BLEU and ROUGE, indicating more **accurate** and **informative** summaries.

## Deployment

- **Flask API**:  
  - A simple endpoint `/summarize` accepts JSON with `"article"` text, returns the generated summary.  
  - Uses a **text-generation pipeline** with `max_new_tokens=400`, `temperature=0.7`, etc.  

```python
prompt = f"Summarize the following article:\n\n{article_text}\n\nSummary:"
output = summarizer(prompt)
