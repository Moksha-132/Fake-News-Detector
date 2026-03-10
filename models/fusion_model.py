def predict_fusion(text_score, image_score, video_score, social_score):
    """
    Fuses all modalities to make a final prediction.
    Using weighted average.
    """
    weights = {
        'text': 0.40,
        'image': 0.25,
        'video': 0.20,
        'social': 0.15
    }
    
    total_weight = sum(weights.values())
    
    final_score = (
        text_score * weights['text'] +
        image_score * weights['image'] +
        video_score * weights['video'] +
        social_score * weights['social']
    ) / total_weight
    
    prediction = "Real News" if final_score >= 0.5 else "Fake News"
    
    return {
        "prediction": prediction,
        "confidence": final_score,
        "modality_scores": {
            "text": text_score,
            "image": image_score,
            "video": video_score,
            "social": social_score
        }
    }
