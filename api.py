from flask import Flask, request, jsonify
from utils import fetch_news, summarize_text, analyze_sentiment, comparative_analysis, generate_tts

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_company():
    data = request.get_json()
    company_name = data.get("company_name")
    
    # Fetch and process news
    articles = fetch_news(company_name)
    for article in articles:
        article["summary"] = summarize_text(article["summary"])
        article["sentiment"] = analyze_sentiment(article["summary"])
        article["topics"] = ["Company News"]  # Placeholder (can be enhanced with topic modeling)
    
    # Comparative analysis
    comparison = comparative_analysis(articles)
    
    # Generate TTS
    final_summary = f"{company_name} की खबरों का विश्लेषण: सकारात्मक {comparison['Sentiment Distribution']['Positive']}, नकारात्मक {comparison['Sentiment Distribution']['Negative']}, तटस्थ {comparison['Sentiment Distribution']['Neutral']}।"
    audio_file = generate_tts(final_summary)
    
    # Response
    result = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": comparison,
        "Audio": audio_file
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)