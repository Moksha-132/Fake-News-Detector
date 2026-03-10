
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image

try:
    # Load model globally to avoid reloading for every request
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()
    
    # Standard ImageNet transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    models_loaded = True
except Exception as e:
    print(f"Warning: Could not load image model: {e}")
    models_loaded = False

def analyze_image(image_path):
    """
    Simulates image credibility scoring based on internal ResNet features.
    In a real system, this would be a fine-tuned Deepfake/Manipulation detection model.
    """
    if not image_path or not models_loaded:
        return 0.5  # Neutral if no image
        
    try:
        input_image = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        with torch.no_grad():
            output = model(input_batch)
        
        # Refined Heuristic:
        # High confidence in ImageNet classes usually suggests a standard real-world object/scene.
        # Low confidence (confused model) often suggests manipulated, synthetic, or unnatural compositions.
        # We use a threshold centered around 0.30.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob = probabilities.max().item()
        
        score = 0.5 + (top_prob - 0.30) * 1.5
        
        # Clamp between 0.05 and 0.95
        return max(0.05, min(0.95, score))

    except Exception as e:
        print(f"Error processing image: {e}")
        return 0.5
