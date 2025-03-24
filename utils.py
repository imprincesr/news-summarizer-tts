import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
import os

# News Extraction
def fetch_news(company_name):
    query = f"{company_name} news"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.select("div.SoaBEf")[:10]:  # Top 10 results
        title = item.select_one("div.MBeuO").text
        link = item.select_one("a")["href"]
        summary = item.select_one("div.GiPYOd").text
        articles.append({"title": title, "link": link, "summary": summary})
    return articles

# Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def summarize_text(text):
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)[0]["summary_text"]
    return summary

# Sentiment Analysis
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    label = result["label"].capitalize()
    if label == "Positive":
        return "Positive"
    elif label == "Negative":
        return "Negative"
    else:
        return "Neutral"

# Comparative Analysis
def comparative_analysis(articles):
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    topics = {}
    
    for article in articles:
        sentiment_dist[article["sentiment"]] += 1
        for topic in article["topics"]:
            topics[topic] = topics.get(topic, 0) + 1
    
    common_topics = [t for t, count in topics.items() if count > 1]
    comparisons = []
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            comparisons.append({
                "comparison": f"Article {i+1} vs Article {j+1}",
                "details": f"{articles[i]['sentiment']} vs {articles[j]['sentiment']}"
            })
    
    return {
        "Sentiment Distribution": sentiment_dist,
        "Common Topics": common_topics,
        "Comparisons": comparisons
    }

# Text-to-Speech
def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="hi", slow=False)
    tts.save(f"output/{filename}")
    return f"output/{filename}"