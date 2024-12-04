const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('./config/db');
const apiRoutes = require('./routes/apiRoutes');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Routes
app.use('/api', apiRoutes);

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
