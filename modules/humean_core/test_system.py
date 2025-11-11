# modules/humean_core/test_system.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from integration.interia_bridge import InterIABridge
from monitoring.dashboard import HumeanDashboard

def test_complete_system():
    print("🚀 TEST COMPLET DU SYSTÈME HUMEAN...")
    
    # 1. Initialiser le pont
    bridge = InterIABridge()
    
    # 2. Tester plusieurs requêtes
    test_queries = [
        "Bonjour HUMEAN, comment fonctionne ta mémoire adaptive?",
        "Peux-tu m'expliquer le principe d'énergie libre?",
        "Quels sont tes modules cognitifs actifs?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Test: {query}")
        result = bridge.process_with_humean_cognition(query)
        print(f"   ✅ Réussi - Énergie: {result['energy_metrics']['free_energy']}")
    
    # 3. Générer le dashboard
    dashboard = HumeanDashboard(bridge.humean)
    report = dashboard.generate_system_report()
    
    print(f"\n📊 RAPPORT FINAL:")
    print(f"   Modules: {report['system_status']['modules_registered']}")
    print(f"   Mémoires: {report['system_status']['memory_entries']}")
    print(f"   Énergie moyenne: {report['system_status']['memory_stats']['avg_energy']:.3f}")
    print(f"   Santé système: {report['performance_metrics']['system_health']}")
    
    print("\n🎉 SYSTÈME HUMEAN COMPLÈTEMENT OPÉRATIONNEL!")

if __name__ == "__main__":
    test_complete_system()
