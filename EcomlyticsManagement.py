import streamlit as st
import pandas as pd
#from scraper import scrape_amazon_reviews
#from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import PIL.Image as Image


# Load the Ecomlytics logo
logo = Image.open("Logo/Ecomlytics1.png")
    
# Sidebar content
st.sidebar.image(logo, width=150)  # Adjust the width to your preference
st.sidebar.title("Ecomlytics")
st.sidebar.write("Your partner in e-commerce analytics.")
# Function to analyze sentiment
def analyze_sentiment(reviews):
    sentiments = []
    for review in reviews:
        blob = TextBlob(review)
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)
    return sentiments

# Streamlit app
st.title("Customer Sentiment Analysis")

st.sidebar.header("Input")
product_url = st.sidebar.text_input("Enter Product URL")

if product_url:
    st.sidebar.text("Scraping reviews...")
    reviews_df = scrape_amazon_reviews(product_url)
    st.sidebar.text("Analyzing sentiments...")
    
    # Perform sentiment analysis
    reviews_df['Sentiment'] = analyze_sentiment(reviews_df['Review'])
    
    # Show results
    st.write("### Reviews and Sentiments")
    st.write(reviews_df)

    # Visualize sentiment distribution
    st.write("### Sentiment Distribution")
    fig, ax = plt.subplots()
    sns.histplot(reviews_df['Sentiment'], bins=20, kde=True, ax=ax)
    ax.set_title('Sentiment Distribution')
    ax.set_xlabel('Sentiment Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Display common complaints
    st.write("### Common Complaints")
    complaints = reviews_df[reviews_df['Sentiment'] < 0]['Review'].tolist()
    st.write("\n".join(complaints))

    # Display product improvement areas
    st.write("### Product Improvement Areas")
    improvement_areas = [review for review in complaints if "improve" in review or "better" in review]
    st.write("\n".join(improvement_areas))

    # Visualize sentiment breakdown
    st.write("### Sentiment Breakdown by Review")
    fig, ax = plt.subplots()
    sns.boxplot(x='Sentiment', data=reviews_df, ax=ax)
    ax.set_title('Sentiment Score Distribution')
    ax.set_xlabel('Sentiment Score')
    st.pyplot(fig)
