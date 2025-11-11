# modules/humean_core/config/free_apis_setup.py
"""
GUIDE DE CONFIGURATION DES APIs GRATUITES POUR HUMEAN
À exécuter PENDANT le téléchargement d'Ollama
"""

import json
from pathlib import Path

FREE_APIS_CONFIG = {
    "google_gemini": {
        "url": "https://aistudio.google.com/",
        "steps": [
            "1. Aller sur Google AI Studio",
            "2. Se connecter avec compte Google", 
            "3. Cliquer sur 'Get API Key'",
            "4. Copier la clé dans humean_config.json"
        ],
        "free_quota": "1500 requêtes/heure",
        "model": "gemini-1.5-flash",
        "api_key_placeholder": "YOUR_GEMINI_API_KEY_HERE"
    },
    
    "huggingface": {
        "url": "https://huggingface.co/settings/tokens",
        "steps": [
            "1. Créer compte Hugging Face",
            "2. Aller dans Settings > Access Tokens",
            "3. Créer un nouveau token (read)",
            "4. Copier dans humean_config.json"
        ],
        "free_quota": "10,000 req/mois",
        "api_key_placeholder": "YOUR_HF_API_KEY_HERE"
    },
    
    "openrouter": {
        "url": "https://openrouter.ai/",
        "steps": [
            "1. Aller sur OpenRouter",
            "2. Se connecter avec GitHub",
            "3. Aller dans Settings > API Keys", 
            "4. Créer et copier la clé"
        ],
        "free_models": ["google/gemma-7b-it:free"],
        "api_key_placeholder": "YOUR_OPENROUTER_API_KEY_HERE"
    }
}

def print_setup_instructions():
    print("🚨 GUIDE DE CONFIGURATION DES APIs GRATUITES")
    print("=" * 50)
    print("📝 PENDANT QU'OLLAMA TÉLÉCHARGE, CONFIGURE CES APIs:\n")
    
    for service, config in FREE_APIS_CONFIG.items():
        print(f"🎯 {service.upper()}:")
        print(f"   📍 {config['url']}")
        for step in config['steps']:
            print(f"   ✅ {step}")
        print(f"   🆓 Quota: {config.get('free_quota', 'N/A')}")
        print(f"   🔑 Clé API: {config['api_key_placeholder']}")
        print()
    
    print("💡 Après obtention des clés, utilisez:")
    print("   python modules/humean_core/config/humean_config_manager.py")
    print("   config_mgr.update_api_key('gemini', 'ta_cle_ici')")

def create_config_template():
    """Créer un template de configuration"""
    config_template = {
        "version": "0.3",
        "system": {
            "name": "HUMEAN Cognitive System",
            "mode": "development"
        },
        "apis": {
            "ollama": {
                "enabled": True,
                "base_url": "http://localhost:11434",
                "default_model": "llama3.2:3b"
            },
            "gemini": {
                "enabled": False,
                "api_key": "YOUR_GEMINI_API_KEY_HERE",
                "model": "gemini-1.5-flash"
            },
            "huggingface": {
                "enabled": False,
                "api_key": "YOUR_HF_API_KEY_HERE",
                "model": "mistralai/Mistral-7B-Instruct-v0.3"
            },
            "openrouter": {
                "enabled": False,
                "api_key": "YOUR_OPENROUTER_API_KEY_HERE",
                "free_model": "google/gemma-7b-it:free"
            }
        }
    }
    
    config_path = Path(__file__).parent / "humean_config_template.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Template créé: {config_path}")

if __name__ == "__main__":
    print_setup_instructions()
    create_config_template()
    
    print("\n🎯 ACTION IMMÉDIATE:")
    print("1. Ouvre les liens dans ton navigateur")
    print("2. Obtiens les clés API gratuites") 
    print("3. Utilise le gestionnaire de configuration pour les ajouter")
