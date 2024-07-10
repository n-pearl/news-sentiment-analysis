import requests
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
import plotly.express as px

# Function to fetch news articles
def fetch_news(api_key, start_date, end_date, news_source = None, subject = None):
    url = "https://newsapi.org/v2/everything"
    query = subject if subject else ""
    params = {
        'q': query,
        'from': start_date,
        'to': end_date,
        'sortBy': 'publishedAt',
        'apiKey': api_key,
        'language': 'en',
    }
    if news_source:
        params['sources'] = news_source

    response = requests.get(url, params=params)
    articles = response.json().get('articles', [])
    
    return articles

# Function to analyze sentiments
def analyze_sentiments(articles):
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
    
    if data:
        df = pd.DataFrame(data)
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    else:
        print("No valid articles found")
        return pd.DataFrame()  # Return an empty DataFrame if no valid articles are found
    
# Function to generate and return graphs
def generate_graphs(df):
    fig_polarity = px.line(df, x='published_at', y='polarity', title='Polarity Over Time')
    fig_subjectivity = px.line(df, x='published_at', y='subjectivity', title='Subjectivity Over Time')
    return fig_polarity, fig_subjectivity

# Function to print articles in a readable format
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

# Example usage
#if __name__ == "__main__":
#    START_DATE = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
#    END_DATE = datetime.now().strftime('%Y-%m-%d')
#    NEWS_SOURCE = 'cnn'  # Example: 'cnn', 'bbc-news', etc.
#    SUBJECT = 'tesla'
#    key = ''
#    
#    articles = fetch_news(START_DATE, END_DATE, key, NEWS_SOURCE, SUBJECT)
#    sentiment_df = analyze_sentiments(articles)
#    print_articles(sentiment_df)
