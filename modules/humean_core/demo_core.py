"""
DÉMONSTRATION HUMEAN CORE
"""

import sys
import os

# Ajouter le chemin actuel
sys.path.append(os.path.dirname(__file__))

print("🧠 DÉMO HUMEAN CORE")
print("=" * 50)

try:
    from humean_core import HumeanCore
    print("✅ HumeanCore importé avec succès!")
    
    # Initialisation
    print("🚀 Initialisation...")
    humean = HumeanCore()
    
    # Statut
    status = humean.get_system_status()
    print("📊 Statut système:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Tests de requêtes
    test_queries = [
        "Bonjour, comment ça va ?",
        "Peux-tu m'expliquer l'IA générative ?", 
        "Quelle est la capitale de la France ?",
        "Merci pour ton aide !"
    ]
    
    print("\n🎯 TESTS DE REQUÊTES:")
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i} ---")
        print(f"👤: {query}")
        
        response = humean.process_query(query)
        
        print(f"🤖: {response['response']}")
        print(f"📋 Métadonnées: {response['metadata']}")
    
    # Statut final
    print("\n" + "=" * 50)
    final_status = humean.get_system_status()
    print("📈 STATISTIQUES FINALES:")
    print(f"   • Conversations: {final_status['conversation_count']}")
    print(f"   • Mode: {final_status['system_state']['current_mode']}")
    print(f"   • Statut: {final_status['status']}")
    
    print("\n🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
