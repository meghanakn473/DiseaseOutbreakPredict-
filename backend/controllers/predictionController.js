const axios = require('axios');
const Outbreak = require('../models/OutbreakModel');

exports.predictOutbreak = async (req, res) => {
  const { location, historicalData } = req.body;

  // Validate input data
  if (!location || !historicalData || historicalData.length === 0) {
    return res.status(400).json({ error: 'Missing required data: location or historicalData' });
  }

  try {
    // Send data to ML service
    const response = await axios.post('http://localhost:5001/predict', { location, historicalData });
    const prediction = response.data;

    console.log('ML service response:', prediction);

    // Create and save new Outbreak record
    const newOutbreak = new Outbreak({
      location: location,
      cases: prediction.cases,
      riskLevel: prediction.riskLevel,
    });

    await newOutbreak.save();

    // Respond with the saved outbreak data
    res.status(200).json(newOutbreak);
  } catch (error) {
    console.error('Error during prediction:', error);
    res.status(500).json({ error: 'Prediction failed', message: error.message });
  }
};
