# modules/humean_core/integration/ollama_bridge.py
import requests
import json
from pathlib import Path

class OllamaBridge:
    """Pont direct vers Ollama pour l'indépendance cognitive"""
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.available_models = self._get_available_models()
        print(f"🔗 Ollama Bridge: {len(self.available_models)} models available")
    
    def _get_available_models(self):
        """Récupérer les modèles Ollama installés"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return []
        except:
            print("❌ Ollama non détecté - installer Ollama d'urgence!")
            return []
    
    def generate_response(self, prompt, model=None, system_prompt=None):
        """Générer une réponse via Ollama"""
        if not self.available_models:
            return {"error": "Aucun modèle Ollama disponible"}
        
        # Choisir le modèle par défaut
        target_model = model or self.available_models[0]
        
        try:
            payload = {
                "model": target_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            }
            
            # Ajouter le prompt système si fourni
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "model": target_model,
                    "response": result.get("response", ""),
                    "context": result.get("context", []),
                    "total_duration": result.get("total_duration", 0)
                }
            else:
                return {"error": f"Ollama error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}
    
    def chat_completion(self, messages, model=None):
        """Interface chat completion compatible OpenAI"""
        if not self.available_models:
            return {"error": "No Ollama models available"}
        
        target_model = model or self.available_models[0]
        
        try:
            payload = {
                "model": target_model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 500
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "model": target_model,
                    "choices": [{
                        "message": {
                            "content": result["message"]["content"],
                            "role": "assistant"
                        }
                    }]
                }
            else:
                return {"error": f"Ollama chat error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Chat connection failed: {str(e)}"}

# Test du bridge Ollama
if __name__ == "__main__":
    print("🧪 TESTING OLLAMA BRIDGE...")
    
    bridge = OllamaBridge()
    
    if bridge.available_models:
        print(f"✅ Models disponibles: {bridge.available_models}")
        
        # Test 1: Génération simple
        print("\n🔍 Test 1: Génération simple")
        result = bridge.generate_response(
            "Explique le concept d'énergie libre en cognition artificielle en 3 phrases.",
            system_prompt="Tu es HUMEAN, un système cognitif avancé. Sois concis et technique."
        )
        
        if "error" not in result:
            print(f"🤖 {result['model']}: {result['response'][:200]}...")
        else:
            print(f"❌ Erreur: {result['error']}")
        
        # Test 2: Chat completion
        print("\n🔍 Test 2: Chat completion")
        messages = [
            {"role": "system", "content": "Tu es HUMEAN. Réponds de manière cognitive et réfléchie."},
            {"role": "user", "content": "Comment la mémoire adaptive améliore-t-elle un système IA?"}
        ]
        
        chat_result = bridge.chat_completion(messages)
        if "error" not in chat_result:
            response = chat_result["choices"][0]["message"]["content"]
            print(f"💬 {chat_result['model']}: {response[:200]}...")
        else:
            print(f"❌ Chat error: {chat_result['error']}")
            
    else:
        print("🚨 CRITIQUE: Installer Ollama d'urgence!")
        print("👉 Exécute: curl -fsSL https://ollama.com/install.sh | sh")
