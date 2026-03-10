import cv2
import os

def analyze_video(video_path):
    """
    Extracts frames and evaluates video credibility.
    """
    if not video_path or not os.path.exists(video_path):
        return 0.5
        
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return 0.5
            
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count == 0:
            return 0.5
            
        # For simplicity in this demo, just check video quality metrics or read 
        # a few frames to run through the image model (simulated here)
        fps = cap.get(cv2.CAP_PROP_FPS)
        resolution = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        cap.release()
        
        # Pseudo heuristic: Extremely low res or weird frame rates might be suspicious
        score = 0.7  # Base assumption
        if resolution[0] < 480 or resolution[1] < 360:
            score -= 0.2
        if fps < 15 and fps > 0:
            score -= 0.1
            
        # Clamp between 0 and 1
        return max(0.0, min(1.0, score))
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return 0.5
