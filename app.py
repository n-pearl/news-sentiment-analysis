from flask import Flask, request, render_template
import pulls
import plotly
import plotly.express as px
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    api_key = request.form['api_key']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    news_source = request.form.get('news_source', '')
    subject = request.form.get('subject', '')
    
    articles = pulls.fetch_news(api_key, start_date, end_date, news_source, subject)
    sentiment_df = pulls.analyze_sentiments(articles)
    
    fig_polarity, fig_subjectivity = pulls.generate_graphs(sentiment_df)
    
    graph_polarity = json.dumps(fig_polarity, cls=plotly.utils.PlotlyJSONEncoder)
    graph_subjectivity = json.dumps(fig_subjectivity, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('results.html', tables=[sentiment_df.to_html(classes='data')], titles=sentiment_df.columns.values, graph_polarity=graph_polarity, graph_subjectivity=graph_subjectivity)

if __name__ == "__main__":
    app.run(debug=True)
