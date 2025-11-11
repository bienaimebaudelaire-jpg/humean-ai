# modules/humean_core/config/humean_config_manager.py
import json
import os
from pathlib import Path

class HumeanConfigManager:
    """Gestionnaire central de configuration HUMEAN"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or Path(__file__).parent / "humean_config.json"
        self.local_config_path = Path(__file__).parent.parent.parent / "config_local.json"
        self.config = self._load_secure_config()
    
    def _load_secure_config(self):
        """Charger la configuration sécurisée"""
        # Charger la config publique
        with open(self.config_path, 'r', encoding='utf-8') as f:
            public_config = json.load(f)
        
        # Charger les clés depuis le fichier local (si existe)
        if self.local_config_path.exists():
            with open(self.local_config_path, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
            
            # Fusionner les clés API
            for service, config in local_config.get("apis", {}).items():
                if service in public_config["apis"]:
                    public_config["apis"][service]["api_key"] = config.get("api_key", "NOT_CONFIGURED")
                    public_config["apis"][service]["enabled"] = True
        
        return public_config
    
    def save_config(self, config=None):
        """Sauvegarder UNIQUEMENT la configuration publique"""
        config_to_save = config or self.config
        
        # Ne sauvegarder que la config publique (sans vraies clés)
        public_config = config_to_save.copy()
        for service in ["gemini", "huggingface", "openrouter"]:
            if service in public_config["apis"]:
                public_config["apis"][service]["api_key"] = f"YOUR_{service.upper()}_API_KEY_HERE"
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(public_config, f, indent=2, ensure_ascii=False)
        print("💾 Configuration publique sauvegardée (sans clés secrètes)")
    
    def update_local_api_key(self, service, api_key):
        """Mettre à jour une clé API dans le fichier local sécurisé"""
        # Charger ou créer le fichier local
        if self.local_config_path.exists():
            with open(self.local_config_path, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
        else:
            local_config = {"apis": {}}
        
        # Mettre à jour la clé
        if "apis" not in local_config:
            local_config["apis"] = {}
        
        local_config["apis"][service] = {"api_key": api_key}
        
        # Sauvegarder le fichier local
        with open(self.local_config_path, 'w', encoding='utf-8') as f:
            json.dump(local_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Clé {service} sauvegardée dans config_local.json (SÉCURISÉ)")
        print("🚨 NE COMMITTEZ JAMAIS config_local.json !")
        
        # Recharger la configuration
        self.config = self._load_secure_config()
        self.show_config_status()
    
    def get_available_engines(self):
        """Obtenir les moteurs cognitifs disponibles"""
        available = []
        apis = self.config["apis"]
        
        if apis["ollama"]["enabled"]:
            available.append("ollama")
        
        for service in ["gemini", "huggingface", "openrouter"]:
            if (apis[service]["enabled"] and 
                apis[service].get("api_key") and 
                apis[service]["api_key"] != f"YOUR_{service.upper()}_API_KEY_HERE"):
                available.append(service)
        
        return available
    
    def show_config_status(self):
        """Afficher le statut de configuration"""
        print("\n📊 STATUT CONFIGURATION HUMEAN")
        print("=" * 40)
        
        engines = self.get_available_engines()
        print(f"🎯 Moteurs disponibles: {engines}")
        
        for service, config in self.config["apis"].items():
            if service == "ollama":
                status = "✅ ACTIVÉ" if config["enabled"] else "❌ DÉSACTIVÉ"
            else:
                has_valid_key = config.get("api_key") and config["api_key"] != f"YOUR_{service.upper()}_API_KEY_HERE"
                status = "✅ ACTIVÉ" if config["enabled"] and has_valid_key else "🔧 CONFIGURER"
            
            print(f"   {service.upper():12} : {status}")

# Interface sécurisée
def interactive_config():
    """Configuration interactive sécurisée"""
    config_mgr = HumeanConfigManager()
    
    print("🎛️  CONFIGURATION SÉCURISÉE HUMEAN")
    print("=" * 45)
    print("🚨 Les clés API sont stockées dans config_local.json")
    print("💡 Ce fichier est ignoré par Git pour la sécurité\n")
    
    config_mgr.show_config_status()
    
    while True:
        print("\n🔧 Options:")
        print("   1. Mettre à jour une clé API (sécurisé)")
        print("   2. Afficher le statut")
        print("   3. Quitter")
        
        choice = input("\nChoisir une option (1-3): ").strip()
        
        if choice == "1":
            print("\n🎯 Mise à jour clé API (sécurisée):")
            print("   - gemini")
            print("   - huggingface") 
            print("   - openrouter")
            
            service = input("Service: ").strip().lower()
            if service in ["gemini", "huggingface", "openrouter"]:
                api_key = input(f"Clé API {service}: ").strip()
                config_mgr.update_local_api_key(service, api_key)
            else:
                print("❌ Service non valide")
                
        elif choice == "2":
            config_mgr.show_config_status()
            
        elif choice == "3":
            print("✅ Configuration sécurisée sauvegardée")
            break
            
        else:
            print("❌ Option non valide")

if __name__ == "__main__":
    interactive_config()
