const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// API Route
app.post('/api/store-values', (req, res) => {
  const { barValues } = req.body;

  // Check if barValues exists and is an object (not an array)
  if (!barValues || typeof barValues !== 'object') {
    return res.status(400).json({ error: 'Invalid input' });
  }

  // Read existing data or create an empty array
  let storedData = [];
  if (fs.existsSync('data.json')) {
    storedData = JSON.parse(fs.readFileSync('data.json', 'utf-8'));
  }

  // Append new data
  storedData.push({ barValues, timestamp: new Date().toISOString() });

  // Write updated data back to file
  fs.writeFileSync('data.json', JSON.stringify(storedData, null, 2));

  console.log('Data stored in file:', storedData);
  res.json({ message: 'Data stored successfully', storedData });
});

// Start Server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
