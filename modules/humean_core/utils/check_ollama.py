# modules/humean_core/utils/check_ollama.py
import requests
import time
import sys
from pathlib import Path

def check_ollama_progress():
    """Vérifier la progression d'Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print("✅ OLLAMA EST OPÉRATIONNEL!")
                print("📦 Modèles installés:")
                for model in models:
                    print(f"   🎯 {model['name']}")
                return True
            else:
                print("⏳ Ollama installé mais aucun modèle encore téléchargé")
                print("💡 Les modèles se téléchargent en background...")
                return "downloading"
        else:
            print("❌ Ollama ne répond pas correctement")
            return False
    except Exception as e:
        print(f"❌ Ollama non accessible: {e}")
        print("💡 Assure-toi qu'Ollama est installé et démarré")
        return False

def monitor_download():
    """Surveiller le téléchargement"""
    print("🔍 Surveillance du téléchargement Ollama...")
    
    for i in range(30):  # Surveiller pendant 5 minutes max
        status = check_ollama_progress()
        
        if status is True:
            print("🎉 TÉLÉCHARGEMENT TERMINÉ!")
            break
        elif status is False:
            print("🚨 Problème détecté - vérifier l'installation")
            break
        else:
            # Still downloading
            print(f"⏳ En cours... ({i+1}/30)")
            time.sleep(10)  # Attendre 10 secondes
    
    print("\n📋 Prochaines étapes:")
    print("   1. Tester: python modules/humean_core/integration/ollama_bridge.py")
    print("   2. Intégrer: python modules/humean_core/gateway/humean_gateway_ollama.py")
    print("   3. Configurer les autres APIs gratuites")

if __name__ == "__main__":
    print("🔍 VÉRIFICATION OLLAMA")
    print("=" * 30)
    status = check_ollama_progress()
    
    if status == "downloading":
        monitor_now = input("\nSurveiller le téléchargement? (o/n): ").strip().lower()
        if monitor_now == 'o':
            monitor_download()
    elif not status:
        print("\n🚨 ACTION REQUISE:")
        print("   1. Installer Ollama: curl -fsSL https://ollama.com/install.sh | sh")
        print("   2. Démarrer: ollama serve")
        print("   3. Télécharger un modèle: ollama pull llama3.2:3b")
