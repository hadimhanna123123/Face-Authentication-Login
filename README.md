# 🔐 Gesture & Face Recognition Authentication System

A multi-factor biometric authentication system that combines **face recognition** and **hand gesture detection** to verify user identity. Users must show their face **and** perform a specific hand gesture (A, B, or L) to successfully authenticate.

## 🎯 Overview

This project implements a dual-authentication mechanism where:

1. **Face Recognition**: Uses FaceNet (InceptionResnetV1) with pre-trained VGGFace2 weights to generate face embeddings and compare them against stored user embeddings
2. **Gesture Detection**: Uses MediaPipe Hands to detect hand landmarks and a trained Random Forest classifier to recognize hand gestures (A, B, or L signs)

When a user attempts to log in via webcam, both their face and gesture must match the expected values for authentication to succeed.

## 🏗️ Architecture

The project is split into two main components:

### Backend (Python/Flask)
- **Port**: 5000
- **Framework**: Flask with CORS enabled
- **ML Models**:
  - MTCNN for face detection
  - InceptionResnetV1 (FaceNet) for face embeddings
  - MediaPipe Hands for hand landmark detection
  - Custom-trained Random Forest classifier for gesture recognition
- **Endpoints**:
  - `POST /process-image`: Receives base64-encoded image, returns face name, gesture detected, and confidence distance

### Frontend (Node.js/Express)
- **Port**: 3000
- **Framework**: Express.js
- **Features**:
  - Webcam capture using `webcam-easy` library
  - Real-time image capture and upload
  - Routes for login, main page, and welcome page
- **Endpoints**:
  - `GET /`: Main landing page
  - `GET /login`: Login page with webcam capture
  - `POST /upload`: Forwards captured image to backend, handles authentication logic
  - `GET /welcome`: Success page after authentication

### Authentication Flow

```
User opens browser
    ↓
Navigate to http://localhost:3000/login
    ↓
Webcam activates → User shows face + gesture (A, B, or L)
    ↓
Click "Take Photo" → Image captured as base64
    ↓
Frontend sends image to backend (POST /process-image)
    ↓
Backend performs:
  1. Face detection (MTCNN)
  2. Face recognition (FaceNet embeddings)
  3. Gesture detection (MediaPipe + Random Forest)
    ↓
Backend returns: { name, gesture, distance }
    ↓
Frontend validates:
  - name == 'HadiMhanna'
  - gesture == expected gesture (A, B, or L)
    ↓
✅ Success → Redirect to /welcome
❌ Failure → Redirect to /
```

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask server with ML inference
│   ├── requirements.txt       # Python dependencies
│   ├── data.pt               # Stored face embeddings (PyTorch tensor)
│   └── model.p               # Trained gesture recognition model (pickle)
│
├── frontend/
│   ├── server.js             # Express.js server
│   ├── package.json          # Node.js dependencies
│   ├── views/
│   │   ├── index.html        # Login page with webcam
│   │   ├── iii.html          # Landing page
│   │   └── welcome.html      # Success page
│   └── public/
│       ├── css/              # Stylesheets
│       └── images/           # Logo and gesture reference images (A, B, L)
│
└── README.md                 # This file
```

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+** (with pip)
- **Node.js 16+** (with npm)
- **Webcam** (for capturing images)

### 1. Clone/Download the Repository

```bash
cd c:\Users\user\Desktop\LAU\Spring2023\Authenticator\TEst
```

### 2. Backend Setup (Python/Flask)

#### Option A: Using a Virtual Environment (Recommended)

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If torch/facenet-pytorch fail, install CPU-only torch first:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install facenet-pytorch

# Run the Flask server
python app.py
```

#### Option B: Using Conda

```powershell
cd backend
conda create -n gesture-auth python=3.10
conda activate gesture-auth
pip install -r requirements.txt
python app.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 3. Frontend Setup (Node.js/Express)

Open a **new terminal/PowerShell window**:

```powershell
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start the Express server
npm start

# Or use nodemon for auto-restart during development:
npm run dev
```

**Expected Output:**
```
Frontend server running on http://localhost:3000
Connecting to backend at http://localhost:5000
```

### 4. Access the Application

1. Open your browser and navigate to: **http://localhost:3000/login**
2. Allow webcam access when prompted
3. Position your face in view and make the required gesture (default: **A** sign)
4. Click **"Take Photo"**
5. If authentication succeeds, you'll be redirected to the welcome page

## 🧠 How It Works

### Face Recognition

1. **Face Detection**: MTCNN detects the face region in the captured image
2. **Embedding Generation**: InceptionResnetV1 converts the face into a 512-dimensional embedding vector
3. **Comparison**: The embedding is compared against pre-stored embeddings in `data.pt` using Euclidean distance
4. **Threshold**: If distance < 0.7, the face is recognized as a match

### Gesture Recognition

1. **Hand Detection**: MediaPipe Hands detects 21 hand landmarks
2. **Feature Extraction**: Normalized x, y coordinates of landmarks are used as features
3. **Classification**: Random Forest classifier predicts the gesture (A, B, or L)
4. **Labels**:
   - 0 → 'A'
   - 1 → 'B'
   - 2 → 'L'

### Multi-Factor Authentication

Both conditions must be met:
- **Face matches**: `name == 'HadiMhanna'`
- **Gesture matches**: `gesture == RANDOM_GESTURE` (configured in `frontend/server.js`)

## 🔧 Configuration

### Change Required Gesture

Edit `frontend/server.js`:

```javascript
const RANDOM_GESTURE = 'A'; // Change to 'B' or 'L'
```

### Change Backend URL

If running backend on a different host/port, edit `frontend/server.js`:

```javascript
const BACKEND_URL = 'http://localhost:5000'; // Update as needed
```

### Add New Users

To add new face embeddings:
1. Train a new FaceNet model or update `data.pt` with new embeddings
2. Ensure the name list in `data.pt` includes the new user

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'facenet_pytorch'`
- **Solution**: Install facenet-pytorch: `pip install facenet-pytorch`

**Problem**: `RuntimeError: CUDA not available` or torch installation fails
- **Solution**: Install CPU-only torch:
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
  ```

**Problem**: MediaPipe fails on Windows
- **Solution**: Use Python 3.8-3.11 (MediaPipe has limited support on newer versions)
- **Alternative**: Run backend in WSL (Windows Subsystem for Linux)

**Problem**: `FileNotFoundError: data.pt or model.p not found`
- **Solution**: Ensure `data.pt` and `model.p` are in the `backend/` directory

### Frontend Issues

**Problem**: `Cannot GET /welcome` or redirect issues
- **Solution**: Ensure both servers are running (backend on 5000, frontend on 3000)

**Problem**: Webcam not working
- **Solution**: 
  - Check browser permissions (allow camera access)
  - Use HTTPS or localhost (some browsers restrict webcam on HTTP)

**Problem**: CORS errors
- **Solution**: Backend already has CORS enabled via `flask-cors`. If issues persist, check firewall settings.

### Authentication Always Fails

**Problem**: Correct face/gesture but still rejected
- **Solution**: 
  - Check backend logs for distance value (should be < 0.7)
  - Verify gesture matches `RANDOM_GESTURE` in `frontend/server.js`
  - Ensure good lighting for face detection

## 📊 Model Files

- **`data.pt`**: PyTorch tensor containing:
  - `saved_data[0]`: List of face embeddings (512-dim vectors)
  - `saved_data[1]`: List of corresponding names
  
- **`model.p`**: Pickle file containing:
  - `model_dict['model']`: Trained Random Forest classifier for gestures

## 🛡️ Security Notes

- This is a **proof-of-concept** authentication system
- For production use, consider:
  - HTTPS/TLS encryption
  - Secure storage of embeddings (encrypted database)
  - Rate limiting on authentication attempts
  - Session management and JWT tokens
  - Liveness detection to prevent photo attacks

## 📝 Technologies Used

### Backend
- Flask (web framework)
- PyTorch (deep learning)
- facenet-pytorch (face recognition)
- MediaPipe (hand tracking)
- OpenCV (image processing)
- scikit-learn (gesture classification)

### Frontend
- Express.js (web server)
- Axios (HTTP client)
- webcam-easy (webcam capture)
- HTML/CSS/JavaScript

## 👨‍💻 Author

Created as part of LAU Spring 2023 coursework.

## 📄 License

This project is for educational purposes.

---

**Happy Authenticating! 🎉**
