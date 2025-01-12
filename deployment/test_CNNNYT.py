import pandas as pd
import requests
import random

# read in the text data from a text file: cnnTest.txt
with open("/home/jupyter-mckayqsnell/FinalProject/nytTest.txt", "r") as file:
    article_text = file.read()
    
# make sure data is read for json payload (the quotes)
article_text = article_text.replace("\n", " ").replace('"', "'")
    
api_url = "http://127.0.0.1:5000/summarize"

payload = {
    "article": article_text
}

response = requests.post(api_url, json=payload)

if response.status_code == 200:
    data = response.json()
    summary = data.get("summary", "No summary returned")
    print(f"--- Article {1} ---")
    print("Original Article (truncated):", article_text[:200], "...")
    print("Summary:", summary)
    print()
else:
    print(f"Failed to summarize article {1}. Status code: {response.status_code}")
    print("Response text:", response.text)
    print()