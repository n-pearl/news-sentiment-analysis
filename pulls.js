const axios = require('axios');
const Sentiment = require('sentiment');
const dotenv = require('dotenv');

dotenv.config();

const sentiment = new Sentiment();
const API_KEY = process.env.API_KEY;

async function getNewsData(start_date, end_date, news_source, subject) {
    try {
        const params = {
            apiKey: API_KEY,
            from: start_date,
            to: end_date,
            sources: news_source,
            q: subject,
            language: 'en'
        };

        console.log('Request parameters:', params);

        const response = await axios.get('https://newsapi.org/v2/everything', {
            params: params
        });

        const articles = response.data.articles.map(article => {
            const result = sentiment.analyze(article.content || '');
            return {
                date: new Date(article.publishedAt),
                title: article.title,
                polarity: result.score,
                AvgPolarityPerWord: result.comparative
            };
        });

        return articles;
    } catch (error) {
        console.error('Error fetching news data:', error.response ? error.response.data : error.message);
        return null;
    }
}

module.exports = { getNewsData };
