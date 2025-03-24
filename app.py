import streamlit as st
import requests
import os

st.title("News Summarization & TTS Application")

company_name = st.text_input("Enter Company Name (e.g., Tesla):")
if st.button("Analyze"):
    if company_name:
        # Call API
        response = requests.post("http://localhost:5000/analyze", json={"company_name": company_name})
        data = response.json()
        
        st.write(f"### Analysis for {data['Company']}")
        for article in data["Articles"]:
            st.write(f"**Title**: {article['title']}")
            st.write(f"**Summary**: {article['summary']}")
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write(f"**Topics**: {', '.join(article['topics'])}")
            st.write("---")
        
        st.write("### Comparative Analysis")
        st.write(data["Comparative Sentiment Score"])
        
        st.audio(data["Audio"], format="audio/mp3")
    else:
        st.error("Please enter a company name.")
