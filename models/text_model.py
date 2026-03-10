import requests
import re

def analyze_text(text):
    """
    Sends the text to a local Ollama instance running Llama 3.2.
    Expects Ollama to be running at http://localhost:11434
    """
    if not text or not text.strip():
        return 0.5, "No text provided."

    url = "http://localhost:11434/api/generate"
    
    prompt = f"Analyze the following news text and determine if it is likely fake or real. Provide reasoning and a credibility score from 0.0 to 1.0 (where 1.0 is highly credible/real, and 0.0 is completely fake). Format the response to start with the score on the first line, followed by the reasoning on subsequent lines.\n\nText: {text}"
    
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=180)
        response.raise_for_status()
        result_text = response.json().get('response', '')
        
        # Parse score and reasoning
        lines = result_text.strip().split('\n')
        score = 0.5
        reasoning = result_text
        
        try:
            # Try to extract a float score from the first piece of text
            match = re.search(r'0\.\d+|1\.0', lines[0])
            if match:
                score = float(match.group())
            else:
                # search the whole text just in case
                match = re.search(r'(?:score|credibility).*?(0\.\d+|1\.0)', result_text, re.IGNORECASE)
                if match:
                    score = float(match.group(1))
        except Exception:
            pass
            
        return score, reasoning
        
    except Exception as e:
        print(f"Error calling text model: {e}")
        return 0.5, f"Could not reach Llama 3.2 model. Error: {e}"
