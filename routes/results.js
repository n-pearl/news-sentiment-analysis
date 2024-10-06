const express = require('express');
const router = express.Router();
const { getNewsData } = require('../pulls');

router.post('/', async (req, res) => {
    const { start_date, end_date, news_source, subject } = req.body;

    const newsData = await getNewsData(start_date, end_date, news_source, subject);
    
    if (!newsData) {
        return res.status(500).send("Error fetching news data");
    }

    const graphPolarity = {
        data: [
            {
                x: newsData.map(article => new Date(article.date)),
                y: newsData.map(article => article.polarity),
                type: 'scatter'
            }
        ],
        layout: {
            title: 'Polarity over Time'
        }
    };

    const graphAvgPolarityPerWord = {
        data: [
            {
                x: newsData.map(article => new Date(article.date)),
                y: newsData.map(article => article.AvgPolarityPerWord),
                type: 'scatter'
            }
        ],
        layout: {
            title: 'AvgPolarityPerWord over Time'
        }
    };

    res.render('results', {
        tables: newsData,
        graphPolarity: JSON.stringify(graphPolarity),
        graphAvgPolarityPerWord: JSON.stringify(graphAvgPolarityPerWord)
    });
});

module.exports = router;