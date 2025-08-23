const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');
const app = express();
const port = 3000;

app.use(bodyParser.json({ limit: '50mb' }));

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the main HTML page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'iii.html')); 
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/upload', async (req, res) => {
    const { image } = req.body; 
    console.log('Received image');
    
    try {
        const response = await axios.post('http://localhost:5000/process-image', { image: image }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Response from Flask:', response.data);
        console.log(response.data['name']);

        if (response.data['name'] == 'HadiMhanna') {
            console.log(' i am here')
            res.redirect('/welcome');
        } else {
            res.redirect('/');
        }

    } catch (error) {
        console.error('Error processing image:', error.response ? error.response.data : error.message);
        res.status(500).send('Error processing image');
    }
});

app.get('/welcome', (req, res) => {
    console.log('i am in welcome')
    res.sendFile(path.join(__dirname, 'welcome.html'));
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
