import os
import torch
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = Flask(__name__)

# custom model and tokenizer
model_dir = "/home/jupyter-mckayqsnell/FinalProject/fine-tuned-llama-model"
tokenizer = AutoTokenizer.from_pretrained(model_dir, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto")

# pipeline for generation
summarizer = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    max_new_tokens=400,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(force=True)
    article_text = data.get("article", None)
    if article_text is None:
        return jsonify({"error": "Missing required parameter 'article'"}), 400
    
    prompt = f"Summarize the following article:\n\n{article_text}\n\nSummary:"
    output = summarizer(prompt, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = output[0]['generated_text']
    summary_start = generated_text.find("Summary:") + len("Summary:")
    summary = generated_text[summary_start:].strip()
    
    return jsonify({"summary": summary})

@app.route("/")
def index():
    return "Model is online. Use /summarize to get summaries."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
    
