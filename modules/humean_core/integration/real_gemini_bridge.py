# modules/humean_core/integration/real_gemini_bridge.py
import google.generativeai as genai
import os
import json
from pathlib import Path

class RealGeminiBridge:
    """Vrai connecteur Gemini utilisant ta clé API"""
    
    def __init__(self):
        self.config = self._load_config()
        self._configure_gemini()
        print("🔗 Real Gemini Bridge initialized")
    
    def _load_config(self):
        """Charger la configuration"""
        config_path = Path(__file__).parent.parent / "config" / "humean_config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _configure_gemini(self):
        """Configurer Gemini avec ta vraie clé"""
        gemini_config = self.config["apis"]["gemini"]
        api_key = gemini_config["api_key"]
        
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            genai.configure(api_key=api_key)
            print("✅ Gemini configured with real API key")
        else:
            print("❌ Gemini API key not configured")
    
    def generate_response(self, prompt, context=None):
        """Générer une réponse avec le vrai Gemini"""
        try:
            # Utiliser gemini-2.0-flash (le bon modèle)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Construire le prompt avec contexte
            full_prompt = self._build_prompt(prompt, context)
            
            # Générer la réponse
            response = model.generate_content(full_prompt)
            
            return {
                "success": True,
                "response": response.text,
                "model_used": "gemini-2.0-flash",
                "engine": "gemini"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "engine": "gemini"
            }
    
    def _build_prompt(self, prompt, context):
        """Construire le prompt complet"""
        system_prompt = """Tu es HUMEAN, un système cognitif avancé basé sur le principe d'énergie libre.
        Tes réponses doivent être techniques, précises et montrer une compréhension cognitive profonde."""
        
        if context:
            context_text = "\n".join([f"- {ctx}" for ctx in context])
            return f"{system_prompt}\n\nContexte:\n{context_text}\n\nQuestion: {prompt}"
        else:
            return f"{system_prompt}\n\nQuestion: {prompt}"

# Test du vrai bridge Gemini
if __name__ == "__main__":
    print("🧪 TESTING REAL GEMINI BRIDGE...")
    
    bridge = RealGeminiBridge()
    
    test_prompt = "Explique le concept d'énergie libre en cognition artificielle"
    result = bridge.generate_response(test_prompt)
    
    if result["success"]:
        print(f"✅ Gemini Response:")
        print(f"   Model: {result['model_used']}")
        print(f"   Response: {result['response'][:200]}...")
    else:
        print(f"❌ Gemini Error: {result['error']}")
