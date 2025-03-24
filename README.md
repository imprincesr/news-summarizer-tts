# News Summarization & TTS Application

## Overview
This web-based application extracts news articles for a given company, summarizes them, performs sentiment analysis, conducts comparative analysis, and generates a Hindi TTS output.

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `python api.py`
4. Run the app: `streamlit run app.py`

## Dependencies
- beautifulsoup4
- requests
- transformers
- gtts
- streamlit
- flask

## Models
- Summarization: `facebook/bart-large-cnn`
- Sentiment Analysis: `distilbert-base-uncased-finetuned-sst-2-english`
- TTS: Google Text-to-Speech (gTTS)

## API Usage
- Endpoint: `POST /analyze`
- Payload: `{"company_name": "Tesla"}`
- Test with Postman or curl.

## Deployment
Deployed on Hugging Face Spaces: [Link](#)

## Assumptions & Limitations
- News fetched from Google News (top 10 results).
- Topics are placeholders; enhance with topic modeling for better results.
- Limited to non-JS websites due to BeautifulSoup.

## Video Demo
[Link to video demo](#)"# news-summarizer-tts" 
