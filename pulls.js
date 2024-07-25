// pulls.js
const axios = require('axios');
const Sentiment = require('sentiment');
const sentiment = new Sentiment();

async function getNewsData(api_key, start_date, end_date, news_source, subject) {
    try {
        const response = await axios.get('https://newsapi.org/v2/everything', {
            params: {
                apiKey: api_key,
                from: start_date,
                to: end_date,
                sources: news_source,
                q: subject,
                language: 'en'
            }
        });

        // Process response
        const articles = response.data.articles.map(article => {
            const result = sentiment.analyze(article.content || '');
            return {
                date: article.publishedAt,
                title: article.title,
                polarity: result.score,
                subjectivity: result.comparative // Using comparative score as a proxy for subjectivity
            };
        });

        return articles;
    } catch (error) {
        console.error('Error fetching news data:', error);
        return null;
    }
}

module.exports = { getNewsData };
