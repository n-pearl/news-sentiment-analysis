import requests
import logging
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
import plotly.express as px

logger = logging.getLogger(__name__)


def fetch_news(api_key, start_date, end_date, news_source=None, subject=None):
    logger.info(f"Fetching news data from {start_date} to {end_date} for source: {news_source} and subject: {subject}")
    try:
        url = f"https://newsapi.org/v2/everything?q={subject}&from={start_date}&to={end_date}&apiKey={api_key}"
        if news_source:
            url += f"&sources={news_source}"
        
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json()
        logger.info("Articles fetched successfully")
        return articles
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise


def analyze_sentiments(articles):
    try:
        data = []
        for article in articles:
            published_at = article.get('publishedAt')
            content = article.get('content')
            title = article.get('title', 'No Title')
            link = article.get('url')
            description = article.get('description')
            if content and published_at:
                analysis = TextBlob(content)
                polarity = analysis.sentiment.polarity #type: ignore
                subjectivity = analysis.sentiment.subjectivity #type: ignore
                data.append({
                    'title': title,
                    'published_at': published_at,
                    'link': link,
                    'description': description,
                    'polarity': polarity,
                    'subjectivity': subjectivity
                })
                logger.info('Sentiment analysis performed successfully')
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        raise
    
    if data:
        df = pd.DataFrame(data)
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    else:
        print("No valid articles found")
        return pd.DataFrame()
    

def generate_graphs(df):
    fig_polarity = px.line(df, x='published_at', y='polarity', title='Polarity Over Time')
    fig_subjectivity = px.line(df, x='published_at', y='subjectivity', title='Subjectivity Over Time')
    return fig_polarity, fig_subjectivity


def print_articles(df):
    if df.empty:
        print("No data to display")
    else:
        print("\nNews Articles with Sentiment Analysis:")
        for index, article in df.iterrows():
            print(f"\nTitle: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Polarity: {article['polarity']}, Subjectivity: {article['subjectivity']}")
            print(f"Description: {article['description']}")
            print(f"Published At: {article['published_at']}")