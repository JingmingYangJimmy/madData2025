const express = require('express');
const cors = require('cors');
const fs = require('fs');
const { exec } = require('child_process'); // Import child_process to run the Python script

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

  // Ensure genre is an array
  if (!Array.isArray(barValues.genre)) {
    barValues.genre = [];
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

  // Execute the Python script to process the movie preferences
  exec('python3 get_user_preference.py', (err, stdout, stderr) => {
    if (err) {
      console.error(`Error executing Python script: ${err}`);
      return res.status(500).json({ error: 'Failed to process movie preferences' });
    }

    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }

    console.log("Python script output:", stdout); // Log the output from Python script

    let rankedMovies;
    try {
      rankedMovies = JSON.parse(stdout); // Parse the JSON output from Python
    } catch (error) {
      console.error("Error parsing Python script output:", error);
      return res.status(500).json({ error: 'Failed to parse movie data' });
    }

    // Send back the response with both the stored data and the ranked movies
    res.json({
      message: 'Data stored and movie preferences calculated successfully',
      storedData,
      rankedMovies,
    });
  });
});

// Start Server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
