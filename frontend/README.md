# Frontend README

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Run the Server

```bash
# Production mode
npm start

# Development mode (auto-restart on changes)
npm run dev
```

Server will start on **http://localhost:3000**

## Routes

- **GET /** - Main landing page (`iii.html`)
- **GET /login** - Login page with webcam capture (`index.html`)
- **POST /upload** - Handles image upload and authentication
- **GET /welcome** - Success page after authentication (`welcome.html`)

## Configuration

Edit `server.js` to change:

```javascript
const RANDOM_GESTURE = 'A';  // Required gesture: 'A', 'B', or 'L'
const PORT = 3000;           // Frontend port
const BACKEND_URL = 'http://localhost:5000';  // Backend API URL
```

## Dependencies

- **express**: Web framework
- **axios**: HTTP client for backend communication
- **body-parser**: Parse JSON request bodies
- **nodemon** (dev): Auto-restart on file changes

## Public Assets

- `/public/css/`: Stylesheets
- `/public/images/`: Logo and gesture reference images
- `/views/`: HTML templates
