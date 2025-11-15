const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');

const app = express();
const RANDOM_GESTURE = 'A'; // Random gesture required for authentication (A, B, or L)
const PORT = 3000;
const BACKEND_URL = 'http://localhost:5000';

app.use(bodyParser.json({ limit: '50mb' }));

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the main HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'iii.html'));
});

// Route to serve the login page
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Handle image upload and authentication
app.post('/upload', async (req, res) => {
    const { image } = req.body;
    console.log('Received image');

    try {
        // Forward image to Flask backend for processing
        const response = await axios.post(`${BACKEND_URL}/process-image`, 
            { image: image },
            { headers: { 'Content-Type': 'application/json' } }
        );

        console.log('Response from backend:', response.data);
        const { name, gesture, distance } = response.data;

        // Check if both face recognition and gesture match
        if (name === 'HadiMhanna' && gesture === RANDOM_GESTURE) {
            console.log('Authentication successful!');
            res.redirect('/welcome');
        } else {
            console.log(`Authentication failed. Name: ${name}, Gesture: ${gesture}, Expected: ${RANDOM_GESTURE}`);
            res.redirect('/');
        }
    } catch (error) {
        console.error('Error processing image:', error.response ? error.response.data : error.message);
        res.status(500).send('Error processing image');
    }
});

// Route to serve the welcome page after successful authentication
app.get('/welcome', (req, res) => {
    console.log('User authenticated');
    res.sendFile(path.join(__dirname, 'views', 'welcome.html'));
});

app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
    console.log(`Connecting to backend at ${BACKEND_URL}`);
});
