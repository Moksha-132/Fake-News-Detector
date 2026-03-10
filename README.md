# Multimodal Fake News Detection System

## Overview
This project is a Multimodal Fake News Detection system that analyzes different types of information from a news post to determine whether the news is Fake or Real.

The system analyzes:
- News text
- Images
- Videos
- Social media signals

It combines the results from all these inputs to produce a final credibility score and prediction.

---

## Features

- Text analysis using Llama 3.2
- Image analysis using ResNet50
- Video frame analysis using OpenCV
- Social media credibility analysis
- Multimodal fusion model for final prediction
- Web interface built with Flask and Tailwind CSS

---

## Technology Stack

### Backend
- Python
- Flask

### Natural Language Processing
- Llama 3.2 (via Ollama)

### Computer Vision
- PyTorch
- Torchvision (ResNet50)
- OpenCV

### Frontend
- HTML
- Tailwind CSS
- JavaScript

---

## Project Structure

fake_news_detection/
│
├── app.py
├── requirements.txt
│
├── models/
│ ├── text_model.py
│ ├── image_model.py
│ ├── video_model.py
│ ├── social_model.py
│ └── fusion_model.py
│
├── templates/
│ ├── index.html
│ └── result.html
│
├── static/
│ ├── css/
│ ├── js/
│ └── uploads/


---

## How It Works

1. The user provides:
   - News text
   - Image
   - Video
   - Social media details

2. The system processes each input:
   - Llama 3.2 analyzes the text.
   - ResNet50 analyzes the image.
   - OpenCV extracts frames from the video.
   - Social signals evaluate the credibility of the source.

3. All scores are combined using a fusion model.

4. The system outputs:
   - Fake or Real prediction
   - Confidence score
   - Explanation

---

## Installation

### Clone the repository
git clone https://github.com/Moksha-132/fake-news-detection.git
cd fake-news

### Install dependencies
pip install -r requirements.txt

### Run the application
python app.py

Open in browser:
http://localhost:5000


---

## Example Input

- News text
- Image upload
- Video upload
- Social signals:
  - Shares
  - Followers
  - Account age

---

## Output

The system returns:
- Prediction: Fake News / Real News
- Confidence Score
- AI Explanation

---

## Developed By

Lakshmi Moksha Boya
