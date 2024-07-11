from flask import Flask, request, render_template, redirect, url_for, flash
import logging
import pulls
import plotly
import plotly.express as px
import json
import os

app = Flask(__name__)
app.secret_key = 'cookies'

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info('Rendering index page')
    url = url_for('index')
    print(f'The url for this page is: {url}')
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        api_key = request.form['api_key']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        news_source = request.form.get('news_source', '')
        subject = request.form.get('subject', '')

        logger.info(f"Received request with API key: {api_key}, start date: {start_date}, end date: {end_date}, news source: {news_source}, subject: {subject}")
        
        articles = pulls.fetch_news(api_key, start_date, end_date, news_source, subject)
        sentiment_df = pulls.analyze_sentiments(articles)
        
        fig_polarity, fig_subjectivity = pulls.generate_graphs(sentiment_df)
        
        graph_polarity = json.dumps(fig_polarity, cls=plotly.utils.PlotlyJSONEncoder)
        graph_subjectivity = json.dumps(fig_subjectivity, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('results.html', tables=[sentiment_df.to_html(classes='data')], titles=sentiment_df.columns.values, graph_polarity=graph_polarity, graph_subjectivity=graph_subjectivity)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        flash(str(e))
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port= int(os.environ.get('PORT', 5000)))
