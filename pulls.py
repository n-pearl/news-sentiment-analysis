import json
from flask import redirect, url_for, flash
import plotly
import requests
import plotly.graph_objs as go
from textblob import TextBlob
from markupsafe import Markup
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news(api_key, start_date, end_date, news_source, subject):
    try:
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': subject,
            'from': start_date,
            'to': end_date,
            'apiKey': api_key,
            'language': 'en',
            'sources': news_source if news_source else None
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return articles
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        flash(str(e))
        return redirect(url_for('index'))

def analyze_sentiment(articles):
    logging.info('Starting sentiment analysis')
    polarity = []
    subjectivity = []
    rows = []
    for article in articles:
        text = article.get('content')
        if text:
            logging.debug(f'Analyzing article: {article["title"]}')
            blob = TextBlob(text)
            polarity.append(blob.polarity)
            subjectivity.append(blob.subjectivity)
            rows.append(f"<tr><td>{article['title']}</td><td>{blob.polarity}</td><td>{blob.subjectivity}</td></tr>")
        else:
            logging.warning(f'No content found for article: {article["title"]}')

    if not polarity:  # Ensure there's at least one data point
        logging.info('No valid articles found, setting default values')
        polarity = [0]
        subjectivity = [0]

    polarity_graph = {
        'data': [go.Scatter(x=list(range(len(polarity))), y=polarity, mode='lines')],
        'layout': {'title': 'Polarity Over Time'}
    }
    subjectivity_graph = {
        'data': [go.Scatter(x=list(range(len(subjectivity))), y=subjectivity, mode='lines')],
        'layout': {'title': 'Subjectivity Over Time'}
    }

    # Serialize Plotly graph objects
    polarity_graph_json = json.dumps(polarity_graph, cls=plotly.utils.PlotlyJSONEncoder)
    subjectivity_graph_json = json.dumps(subjectivity_graph, cls=plotly.utils.PlotlyJSONEncoder)

    table_html = Markup(f"<table><tr><th>Title</th><th>Polarity</th><th>Subjectivity</th></tr>{''.join(rows)}</table>")
    logging.info('Completed sentiment analysis')
    logging.debug(f"Polarity Graph JSON: {polarity_graph_json}")
    logging.debug(f"Subjectivity Graph JSON: {subjectivity_graph_json}")
    return table_html, polarity_graph_json, subjectivity_graph_json