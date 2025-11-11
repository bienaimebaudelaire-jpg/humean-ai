# modules/humean_core/integration/real_huggingface_bridge.py
import requests
import json
from pathlib import Path

class RealHuggingFaceBridge:
    """Vrai connecteur Hugging Face utilisant ta clé API"""
    
    def __init__(self):
        self.config = self._load_config()
        self.api_key = self.config["apis"]["huggingface"]["api_key"]
        self.model = "microsoft/DialoGPT-medium"  # Modèle simple et fiable
        print("🔗 Real HuggingFace Bridge initialized")
    
    def _load_config(self):
        """Charger la configuration"""
        config_path = Path(__file__).parent.parent / "config" / "humean_config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_response(self, prompt, context=None):
        """Générer une réponse avec Inference API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Construire les inputs
            inputs = self._build_inputs(prompt, context)
            
            payload = {
                "inputs": inputs,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            # URL CORRECTE pour Inference API
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{self.model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result[0]['generated_text'] if isinstance(result, list) else str(result)
                
                return {
                    "success": True,
                    "response": generated_text,
                    "model_used": self.model,
                    "engine": "huggingface"
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}",
                    "engine": "huggingface"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "engine": "huggingface"
            }
    
    def _build_inputs(self, prompt, context):
        """Construire les inputs pour le modèle"""
        if context:
            context_text = " ".join([str(ctx) for ctx in context])
            return f"Contexte: {context_text} Question: {prompt} Réponse:"
        else:
            return f"Question: {prompt} Réponse:"

# Test du vrai bridge Hugging Face
if __name__ == "__main__":
    print("🧪 TESTING REAL HUGGINGFACE BRIDGE...")
    
    bridge = RealHuggingFaceBridge()
    
    test_prompt = "Explain AI in simple terms"
    result = bridge.generate_response(test_prompt)
    
    if result["success"]:
        print(f"✅ HuggingFace Response:")
        print(f"   Model: {result['model_used']}")
        print(f"   Response: {result['response'][:200]}...")
    else:
        print(f"❌ HuggingFace Error: {result['error']}")
