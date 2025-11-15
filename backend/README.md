# Backend README

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate    # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

Server will start on **http://localhost:5000**

## API Endpoints

### POST /process-image

Processes an uploaded image for face recognition and gesture detection.

**Request Body:**
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Response:**
```json
{
  "name": "HadiMhanna",
  "gesture": "A",
  "distance": 0.3996541500091553
}
```

**Status Codes:**
- `201`: Success
- `400`: No image data provided
- `500`: Processing error

## Model Files

- **data.pt**: Contains face embeddings and names
- **model.p**: Trained gesture recognition model

## Dependencies

See `requirements.txt` for full list. Key packages:
- `flask`: Web framework
- `torch`: Deep learning
- `facenet-pytorch`: Face recognition
- `mediapipe`: Hand gesture detection
- `opencv-python`: Image processing
