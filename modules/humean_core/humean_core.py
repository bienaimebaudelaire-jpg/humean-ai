"""
HUMEAN CORE - Version fonctionnelle minimale
"""

class HumeanCore:
    """Cœur du système Humean AI - Version minimale"""
    
    def __init__(self, config_path=None):
        print("🚀 HumeanCore initialisé!")
        self.conversation_history = []
        self.system_state = {
            "active": True,
            "current_mode": "balanced"
        }
    
    def process_query(self, user_input, user_context=None):
        """Traite une requête utilisateur"""
        print(f"📥 Traitement: {user_input}")
        
        # Simuler une réponse intelligente
        response = f"Je suis Humean AI. J'ai reçu votre message : '{user_input}'. Comment puis-je vous aider aujourd'hui ?"
        
        # Ajouter à l'historique
        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": "2024-01-01T00:00:00"  # Simplifié pour le test
        })
        
        return {
            "response": response,
            "metadata": {
                "success": True,
                "conversation_count": len(self.conversation_history),
                "mode": "minimal"
            }
        }
    
    def get_system_status(self):
        """Retourne l'état du système"""
        return {
            "system_state": self.system_state,
            "conversation_count": len(self.conversation_history),
            "status": "operational",
            "version": "minimal_v1"
        }
    
    def set_mode(self, mode):
        """Change le mode"""
        if mode in ["balanced", "creative", "analytical"]:
            self.system_state["current_mode"] = mode
            return True
        return False

# Singleton pattern
_humean_instance = None

def get_humean_core(config_path=None):
    global _humean_instance
    if _humean_instance is None:
        _humean_instance = HumeanCore(config_path)
    return _humean_instance

if __name__ == "__main__":
    # Test autonome
    print("🧠 HumeanCore - Test autonome")
    core = HumeanCore()
    print("Status:", core.get_system_status())
    
    # Test requête
    result = core.process_query("Bonjour !")
    print("Réponse:", result["response"])
    print("Métadonnées:", result["metadata"])
