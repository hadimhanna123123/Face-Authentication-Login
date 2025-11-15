from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import base64
import io
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import pickle
import cv2
import mediapipe as mp
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import torch

user = 'HadiMhanna'

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains and routes


def check_gesture(image):
    """Detect hand gesture (A, B, or L) from image using MediaPipe and trained model."""
    # Load the gesture recognition model
    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']

    # Load the labels dictionary
    labels_dict = {0: 'A', 1: 'B', 2: 'L'}

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.3)

    # Convert the PIL Image to a NumPy array and then to RGB
    image_np = np.array(image)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Process the image to detect hands and landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Prepare the data for model prediction
            data_aux = []
            x_ = [landmark.x for landmark in hand_landmarks.landmark]
            y_ = [landmark.y for landmark in hand_landmarks.landmark]

            for x, y in zip(x_, y_):
                data_aux.extend([x - min(x_), y - min(y_)])

            # Make prediction using the model
            prediction = model.predict([data_aux])
            predicted_character = labels_dict[int(prediction[0])]

            # Return the predicted character
            return predicted_character
    else:
        print("No hand landmarks detected.")
        return "No gesture detected"


def run_face_recognition(image):
    """Recognize face from image using FaceNet embeddings and compare with stored embeddings."""
    # Initialize MTCNN for face detection and InceptionResnetV1 for face embeddings
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    
    # Detect face and get embedding
    face, prob = mtcnn(image, return_prob=True)
    print(f"Face detection probability: {prob}")
    emb = resnet(face.unsqueeze(0)).detach()
    
    # Load stored face embeddings
    saved_data = torch.load('data.pt')
    embedding_list = saved_data[0]
    name_list = saved_data[1]
    
    # Calculate distance to all stored embeddings
    dist_list = []
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
        
    # Find closest match
    idx_min = dist_list.index(min(dist_list))
    min_distance = min(dist_list)
    print(f"Minimum distance: {min_distance}")
    
    # Get gesture prediction
    gesture_prediction = check_gesture(image)
    
    # Return result based on distance threshold
    if min_distance > 0.7:
        return {'name': 'Others', 'distance': min_distance, 'gesture': gesture_prediction}
    else:
        return {'name': name_list[idx_min], 'distance': min_distance, 'gesture': gesture_prediction}


@app.route('/process-image', methods=['POST'])
def process_image():
    """Process uploaded image for face recognition and gesture detection."""
    if not request.json or 'image' not in request.json:
        app.logger.error("No image data in request")
        return jsonify({'error': 'No image data provided'}), 400

    data = request.json['image']
    try:
        # Decode base64 image data
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        app.logger.error("Failed to process image: %s", str(e))
        return jsonify({'error': 'Failed to process image'}), 500

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Run face recognition and gesture detection
    result = run_face_recognition(image)
    print(result)
    
    output = jsonify(result)
    response = make_response(output, 201)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
