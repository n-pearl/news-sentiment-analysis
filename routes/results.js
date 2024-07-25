// routes/results.js
const express = require('express');
const router = express.Router();
const { getNewsData } = require('../pulls');

router.post('/', async (req, res) => {
    const { api_key, start_date, end_date, news_source, subject } = req.body;

    const newsData = await getNewsData(api_key, start_date, end_date, news_source, subject);
    
    if (!newsData) {
        return res.status(500).send("Error fetching news data");
    }

    // Prepare graph data
    const graphPolarity = {
        data: [
            {
                x: newsData.map(article => article.date),
                y: newsData.map(article => article.polarity),
                type: 'scatter'
            }
        ],
        layout: {
            title: 'Polarity over Time'
        }
    };

    const graphSubjectivity = {
        data: [
            {
                x: newsData.map(article => article.date),
                y: newsData.map(article => article.subjectivity),
                type: 'scatter'
            }
        ],
        layout: {
            title: 'Subjectivity over Time'
        }
    };

    console.log('Graph Polarity:', JSON.stringify(graphPolarity)); // Debugging log
    console.log('Graph Subjectivity:', JSON.stringify(graphSubjectivity)); // Debugging log

    res.render('results', {
        tables: newsData,
        graphPolarity: JSON.stringify(graphPolarity),
        graphSubjectivity: JSON.stringify(graphSubjectivity)
    });
});

module.exports = router;