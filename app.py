from flask import Flask, request, render_template, redirect, url_for, flash
import logging
import pulls
import plotly
import plotly.express as px
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    api_key = request.form['api_key']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    news_source = request.form.get('news_source', '')
    subject = request.form['subject']
    
    try:
        logger.info(f"Received request with API key, start date: {start_date}, end date: {end_date}, news source: {news_source}, subject: {subject}")
        articles = pulls.get_news(api_key, start_date, end_date, news_source, subject)
        if not articles:
            raise ValueError("No articles found for the given parameters.")
        tables, graph_polarity, graph_subjectivity = pulls.analyze_sentiment(articles)
        logger.info("Rendering results page")
        return render_template('results.html', tables=tables, graph_polarity=graph_polarity, graph_subjectivity=graph_subjectivity)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        flash(f"Error: {str(e)}")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= int(os.environ.get('PORT', 5000)))
