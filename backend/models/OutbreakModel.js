const mongoose = require('mongoose');

const OutbreakSchema = new mongoose.Schema({
  location: String,
  cases: Number,
  riskLevel: String,
  date: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Outbreak', OutbreakSchema);
