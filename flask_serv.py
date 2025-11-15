from flask import Flask, request, jsonify,make_response
from flask_cors import CORS
import base64
import io
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
user='HadiMhanna'
import torch
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains and routes

@app.route('/process-image', methods=['POST'])
def process_image():
    if not request.json or 'image' not in request.json:
        app.logger.error("No image data in request")
        return jsonify({'error': 'No image data provided'}), 400

    data = request.json['image']
    try:
        # Decode the image data
        image_data = base64.b64decode(data.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        app.logger.error("Failed to process image: %s", str(e))
        return jsonify({'error': 'Failed to process image'}), 500

    # Process the image with your ML model
    if image.mode != 'RGB':
        image = image.convert('RGB')

    result = run_your_model(image)
    output= jsonify(result)
    ress=make_response(output,201)
    ress.headers["Content-Type"] = "application/json"
    return ress

def run_your_model(image):
    # getting embedding matrix of the given img
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
    resnet = InceptionResnetV1(pretrained='vggface2').eval() # initializing resnet for face img to embeding conversion
    face, prob = mtcnn(image, return_prob=True) # returns cropped face and probability
    print(prob)
    emb = resnet(face.unsqueeze(0)).detach() # detech is to make required gradient false
    
    saved_data = torch.load('data.pt') # loading data.pt file
    embedding_list = saved_data[0] # getting embedding data
    name_list = saved_data[1] # getting list of names
    dist_list = [] # list of matched distances, minimum distance is used to identify the person
    
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
        
    idx_min = dist_list.index(min(dist_list))
    ddist=min(dist_list)
    print(ddist)
    if(ddist>0.7):
        return {'name':'Others','distance':ddist}
    else:
        return {'name':name_list[idx_min],'distance': min(dist_list)}

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Set debug=True for development to get debug output
