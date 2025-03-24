import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
import os

# Utility Functions (moved from utils.py)
def fetch_news(company_name):
    query = f"{company_name} news"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.select("div.SoaBEf")[:10]:
        title = item.select_one("div.MBeuO").text
        link = item.select_one("a")["href"]
        summary = item.select_one("div.GiPYOd").text
        articles.append({"title": title, "link": link, "summary": summary})
    return articles

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def summarize_text(text):
    return summarizer(text, max_length=50, min_length=25, do_sample=False)[0]["summary_text"]

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]["label"].capitalize()
    return "Positive" if result == "Positive" else "Negative" if result == "Negative" else "Neutral"

def comparative_analysis(articles):
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_dist[article["sentiment"]] += 1
    return {"Sentiment Distribution": sentiment_dist}

def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="hi", slow=False)
    filepath = f"output/{filename}"
    tts.save(filepath)
    return filepath

# Streamlit UI
st.title("News Summarization & TTS Application")

company_name = st.text_input("Enter Company Name (e.g., Tesla):")
if st.button("Analyze"):
    if company_name:
        with st.spinner("Fetching and analyzing news..."):
            # Fetch and process news
            articles = fetch_news(company_name)
            for article in articles:
                article["summary"] = summarize_text(article["summary"])
                article["sentiment"] = analyze_sentiment(article["summary"])
                article["topics"] = ["Company News"]  # Placeholder
            
            # Comparative analysis
            comparison = comparative_analysis(articles)
            
            # Generate TTS
            final_summary = f"{company_name} की खबरों का विश्लेषण: सकारात्मक {comparison['Sentiment Distribution']['Positive']}, नकारात्मक {comparison['Sentiment Distribution']['Negative']}, तटस्थ {comparison['Sentiment Distribution']['Neutral']}।"
            audio_file = generate_tts(final_summary)
            
            # Display results
            st.write(f"### Analysis for {company_name}")
            for article in articles:
                st.write(f"**Title**: {article['title']}")
                st.write(f"**Summary**: {article['summary']}")
                st.write(f"**Sentiment**: {article['sentiment']}")
                st.write(f"**Topics**: {', '.join(article['topics'])}")
                st.write("---")
            
            st.write("### Comparative Analysis")
            st.write(comparison)
            
            st.audio(audio_file, format="audio/mp3")
    else:
        st.error("Please enter a company name.")