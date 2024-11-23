
import streamlit as st
import json
import google.generativeai as genai
from app.reddit_data_extraction import RedditDataExtractor
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the variables
google_api_key = os.getenv("GOOGLE_API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
search_api_key = os.getenv("SEARCH_API_KEY")

# Function to load Reddit data
def load_reddit_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to extract Reddit text for summarization
def extract_reddit_text(data):
    extracted_data = []
    for post in data:
        post_content = f"Title: {post['title']}\n"
        post_content += f"Body: {post['selftext']}\n"
        post_content += "Comments:\n"
        for comment in post.get("comments", []):
            if isinstance(comment, dict):
                post_content += f"- {comment['comment_body']} (Score: {comment['comment_score']})\n"
        extracted_data.append(post_content)
    return extracted_data

# Function to generate a summary using Gemini LLM
def generate_summary(extracted_data, context_question, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = (
        f"The following is data extracted from Reddit. Based on the question below, "
        f"generate a concise and accurate summary and do not mention that you referred first, second or third post, just provide a general summary:\n\n"
        f"also at the end, generate final conclusion on the sentiment of the extracted reddit data on whether it is positive, negative, or neutral"
        f"Question: {context_question}\n\n"
    )
    for data in extracted_data:
        prompt += f"Post:\n{data}\n\n"

    prompt += "Provide a detailed summary:"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("Reddit Data Extraction and Summarization")
st.write("Enter your question to extract Reddit data and generate a detailed summary and sentiment analysis.")

# User inputs
question = st.text_input("Enter your question:")

if st.button("Generate Summary"):
    if question and google_api_key and search_engine_id and reddit_client_id and reddit_client_secret and reddit_user_agent:
        with st.spinner("Extracting Reddit data..."):
            # Initialize Reddit data extractor
            extractor = RedditDataExtractor(
                search_engine_id=search_engine_id,
                reddit_client_id=reddit_client_id,
                reddit_client_secret=reddit_client_secret,
                reddit_user_agent=reddit_user_agent,
                search_api_key=search_api_key
            )

            # Extract Reddit URLs and data
            reddit_urls = extractor.get_reddit_urls(query=question, max_results=10)
            if reddit_urls:
                extractor.fetch_reddit_data_from_urls(reddit_urls, max_comments_per_post=10, output_file="reddit_data.json")
                st.success("Reddit data extracted successfully!")

                with st.spinner("Generating summary..."):
                    reddit_data = load_reddit_data("reddit_data.json")
                    extracted_data = extract_reddit_text(reddit_data)
                    summary = generate_summary(extracted_data, question, google_api_key)
                    st.success("Summary generated successfully!")

                    st.subheader("Summary and Sentiment Analysis")
                    st.write(summary)
            else:
                st.error("No Reddit URLs found for the given question.")
    else:
        st.error("Please fill in all the fields.")
