import json
from flask import redirect, url_for, flash
import plotly
import requests
import plotly.graph_objs as go
from textblob import TextBlob
from markupsafe import Markup
import logging
from urllib.parse import quote


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news(api_key, start_date, end_date, news_source, subject):
    try:
        subject_encoded = quote(subject)
        news_source_encoded = quote(news_source)
        url = (f'https://newsapi.org/v2/everything?q={subject_encoded}&language=en&'
               f'from={start_date}&to={end_date}&sources={news_source_encoded}&apiKey={api_key}')
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] != 'ok':
            raise ValueError(f"Error from news API: {data['message']}")
        return data['articles']
    except Exception as e:
        logger.error(f"Failed to fetch news articles: {e}")
        raise

def analyze_sentiment(articles):
    logging.info('Starting sentiment analysis')
    polarity = []
    subjectivity = []
    for article in articles:
        text = article.get('content')
        if text:
            logging.debug(f'Analyzing article: {article["title"]}')
            blob = TextBlob(text)
            polarity.append(blob.polarity)
            subjectivity.append(blob.subjectivity)
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

    polarity_graph_json = json.dumps(polarity_graph, cls=plotly.utils.PlotlyJSONEncoder)
    subjectivity_graph_json = json.dumps(subjectivity_graph, cls=plotly.utils.PlotlyJSONEncoder)

    logging.info('Completed sentiment analysis')
    logging.debug(f"Polarity Graph JSON: {polarity_graph_json}")
    logging.debug(f"Subjectivity Graph JSON: {subjectivity_graph_json}")
    return polarity_graph_json, subjectivity_graph_json, polarity, subjectivity

def generate_tables(articles, polarity, subjectivity):
    table_html = """
    <table id='articles-table'>
        <thead>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>URL</th>
                <th>Polarity</th>
                <th>Subjectivity</th>
            </tr>
        </thead>
        <tbody>
    """
    for article, pol, subj in zip(articles, polarity, subjectivity):
        table_html += f"""
            <tr>
                <td>{Markup.escape(article['title'])}</td>
                <td>{Markup.escape(article['description'])}</td>
                <td><a href='{article['url']}' target='_blank'>Link</a></td>
                <td>{pol}</td>
                <td>{subj}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """
    return table_html