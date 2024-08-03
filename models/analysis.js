// models/Analysis.js
const mongoose = require('mongoose');

const AnalysisSchema = new mongoose.Schema({
    api_key: String,
    start_date: Date,
    end_date: Date,
    news_source: String,
    subject: String,
    polarity: Number,
    AvgPolarityPerWord: Number
});

module.exports = mongoose.model('Analysis', AnalysisSchema);
