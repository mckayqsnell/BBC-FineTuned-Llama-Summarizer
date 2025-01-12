import pandas as pd
import requests

df_merged = pd.read_csv("/home/jupyter-mckayqsnell/FinalProject/df_merged.csv")

# Sample 3 articles
sampled_articles = df_merged.sample(n=3, random_state=42).reset_index(drop=True)
#sampled_articles = df_merged.iloc[[0]].reset_index(drop=True)

api_url = "http://127.0.0.1:5000/summarize"

for i, row in sampled_articles.iterrows():
    article_text = row["Content"]

    payload = {
        "article": article_text
    }
    
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("summary", "No summary returned")
        print(f"--- Article {i+1} ---")
        print("Original Article (truncated):", article_text[:200], "...")
        print("Summary:", summary)
        print()
    else:
        print(f"Failed to summarize article {i+1}. Status code: {response.status_code}")
        print("Response text:", response.text)
        print()
