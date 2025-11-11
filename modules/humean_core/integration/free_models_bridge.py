# modules/humean_core/integration/free_models_bridge.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

class FreeModelsBridge:
    """Pont vers toutes les IA 100% gratuites"""
    
    def __init__(self):
        self.available_models = self._detect_available_models()
        print(f"🎯 Free Models Bridge: {len(self.available_models)} models detected")
    
    def _detect_available_models(self):
        """Détecter les modèles gratuits disponibles"""
        models = []
        
        # Vérifier Ollama
        if self._check_ollama():
            models.append("ollama")
        
        # Vérifier Hugging Face
        if self._check_huggingface():
            models.append("huggingface")
            
        # Gemini toujours disponible (API key facile)
        models.append("gemini")
        
        # OpenRouter gratuit
        models.append("openrouter")
        
        return models
    
    def _check_ollama(self):
        """Vérifier si Ollama est installé"""
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def _check_huggingface(self):
        """Vérifier l'accès Hugging Face"""
        try:
            import requests
            # Tester un modèle public
            r = requests.get("https://huggingface.co/api/models/microsoft/DialoGPT-medium", timeout=10)
            return r.status_code == 200
        except:
            return False
    
    def query_all_free_models(self, question):
        """Interroger tous les modèles gratuits disponibles"""
        responses = {}
        
        for model in self.available_models:
            try:
                if model == "ollama":
                    responses["ollama"] = self._ask_ollama(question)
                elif model == "huggingface":
                    responses["huggingface"] = self._ask_huggingface(question)
                elif model == "gemini":
                    responses["gemini"] = self._ask_gemini(question)
                elif model == "openrouter":
                    responses["openrouter"] = self._ask_openrouter(question)
                    
                print(f"✅ {model}: Response received")
            except Exception as e:
                print(f"❌ {model}: {e}")
                responses[model] = None
        
        return responses
    
    def _ask_ollama(self, question):
        """Ollama local"""
        try:
            import requests
            payload = {
                "model": "llama3.2:latest",
                "prompt": question,
                "stream": False
            }
            r = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
            return r.json().get("response", "No response")
        except:
            return "Ollama error"
    
    def _ask_gemini(self, question):
        """Gemini Flash gratuit"""
        try:
            # Note: Besoin d'une clé API Google AI Studio (gratuite)
            return "Gemini: Configure API key in humean_config.json"
        except:
            return "Gemini config needed"
    
    def _ask_huggingface(self, question):
        """Hugging Face models"""
        try:
            return "HF: Configure model endpoint"
        except:
            return "HF config needed"
    
    def _ask_openrouter(self, question):
        """OpenRouter free tier"""
        try:
            return "OpenRouter: Configure free API key"
        except:
            return "OpenRouter config needed"

# Test
if __name__ == "__main__":
    bridge = FreeModelsBridge()
    print("🧪 Testing free models bridge...")
    
    test_question = "What is cognitive architecture in AI systems?"
    responses = bridge.query_all_free_models(test_question)
    
    print(f"\n📊 Results from {len(responses)} free models:")
    for model, response in responses.items():
        print(f"   {model}: {response[:100]}...")
