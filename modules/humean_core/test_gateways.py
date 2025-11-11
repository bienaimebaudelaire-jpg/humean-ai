"""Test complet de HumeanCore avec Gateways"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

print("🧪 TEST COMPLET HUMEAN CORE + GATEWAYS")
print("=" * 60)

try:
    from humean_core import HumeanCore
    
    print("🚀 Initialisation...")
    core = HumeanCore()
    
    print("📊 Récupération du statut...")
    status = core.get_system_status()
    
    print("\n=== STATUT SYSTÈME ===")
    print(f"Gateway actif: {status.get('gateway_status', {}).get('active_gateway', 'Aucun')}")
    print(f"Gateways disponibles: {status.get('gateway_status', {}).get('available_gateways', [])}")
    print(f"Statut global: {status.get('status', 'Inconnu')}")
    print(f"Composants: {status.get('components', {})}")
    
    print("\n=== TEST REQUÊTE ===")
    test_query = "Bonjour, peux-tu me dire quelle gateway AI tu utilises ?"
    print(f"👤: {test_query}")
    
    result = core.process_query(test_query)
    print(f"🤖: {result['response']}")
    print(f"📋 Métadonnées: {result['metadata']}")
    
    print("\n=== TEST COMMUTATION GATEWAY ===")
    available = status.get('gateway_status', {}).get('available_gateways', [])
    if len(available) > 1:
        print(f"Gateways disponibles pour commutation: {available}")
        new_gateway = available[0]
        print(f"Tentative de commutation vers: {new_gateway}")
        success = core.switch_gateway(new_gateway)
        if success:
            new_status = core.get_system_status()
            print(f"✅ Nouveau gateway: {new_status['gateway_status']['active_gateway']}")
        else:
            print("❌ Échec de la commutation")
    else:
        print("ℹ️  Un seul gateway disponible - pas de commutation possible")
    
    print("\n🎉 TEST TERMINÉ AVEC SUCCÈS!")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
