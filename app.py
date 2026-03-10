import os
import uuid
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Import models
from models.text_model import analyze_text
from models.image_model import analyze_image
from models.video_model import analyze_video
from models.social_model import analyze_social
from models.fusion_model import predict_fusion

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB limit

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm'}

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract Text
        news_text = request.form.get('news_text', '')
        
        # Extract Social Data
        shares = request.form.get('shares', 0)
        followers = request.form.get('followers', 0)
        account_age = request.form.get('account_age', 0)
        
        # Handle File Uploads
        image_path = None
        video_path = None
        
        if 'image' in request.files:
            img_file = request.files['image']
            if img_file and allowed_file(img_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                ext = img_file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"img_{uuid.uuid4().hex}.{ext}")
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img_file.save(image_path)
                
        if 'video' in request.files:
            vid_file = request.files['video']
            if vid_file and allowed_file(vid_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                ext = vid_file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"vid_{uuid.uuid4().hex}.{ext}")
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                vid_file.save(video_path)
        
        # Run Modality Models
        text_score, text_explanation = analyze_text(news_text)
        image_score = analyze_image(image_path)
        video_score = analyze_video(video_path)
        social_score = analyze_social(shares, followers, account_age)
        
        # Fusion
        result = predict_fusion(text_score, image_score, video_score, social_score)
        result['explanation'] = text_explanation
        
        # Return success
        return jsonify(result)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
