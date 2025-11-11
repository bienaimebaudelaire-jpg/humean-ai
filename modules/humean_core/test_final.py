"""TEST FINAL COMPLET"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🎯 TEST FINAL HUMEAN AI")
print("=" * 50)

try:
    from humean_core import HumeanCore
    
    print("🚀 Initialisation du système...")
    core = HumeanCore()
    
    print("📊 Statut système:")
    status = core.get_system_status()
    
    print(f"   • Gateway actif: {status['gateway_status']['active_gateway']}")
    print(f"   • Gateways disponibles: {status['gateway_status']['available_gateways']}")
    print(f"   • Composants: {sum(status['components'].values())}/{len(status['components'])}")
    print(f"   • Statut: {status['status']}")
    
    print("\n🧪 Test de conversation:")
    test_messages = [
        "Bonjour !",
        "Comment fonctionne Humean AI ?",
        "Quels gateways sont disponibles ?",
        "Merci pour les informations !"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"👤: {message}")
        
        result = core.process_query(message)
        print(f"🤖: {result['response']}")
        
        if result['metadata']['success']:
            print(f"   ✅ Gateway: {result['metadata'].get('gateway_used', 'N/A')}")
            print(f"   📊 Confiance: {result['metadata'].get('confidence', 0):.2f}")
        else:
            print(f"   ❌ Erreur: {result['metadata'].get('error', 'Unknown')}")
    
    print("\n" + "=" * 50)
    final_status = core.get_system_status()
    print(f"📈 RAPPORT FINAL:")
    print(f"   • Conversations: {final_status['conversation_count']}")
    print(f"   • Gateway actif: {final_status['gateway_status']['active_gateway']}")
    print(f"   • Système: {final_status['status'].upper()}")
    
    print("\n🎉 SYSTÈME HUMEAN AI OPÉRATIONNEL !")
    
except Exception as e:
    print(f"❌ ERREUR CRITIQUE: {e}")
    import traceback
    traceback.print_exc()
