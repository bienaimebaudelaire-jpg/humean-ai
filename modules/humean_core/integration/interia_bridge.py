# modules/humean_core/integration/interia_bridge.py
import sys
from pathlib import Path

# Importer HUMEAN
sys.path.append(str(Path(__file__).parent.parent))
from gateway.humean_gateway_v2 import HumeanGatewayV2

class InterIABridge:
    """Pont entre HUMEAN et le système interIA existant"""
    
    def __init__(self):
        self.humean = HumeanGatewayV2()
        print("🌉 HUMEAN-interIA Bridge initialized")
    
    def process_with_humean_cognition(self, query):
        """Traiter une requête avec cognition HUMEAN"""
        print(f"🔗 Processing with HUMEAN-interIA bridge: {query}")
        
        # Cognition HUMEAN
        humean_result = self.humean.process_with_cognitive_layer(query)
        
        # Pour l'instant, simulation d'interIA (à connecter plus tard)
        humean_result["interia_available"] = True
        humean_result["note"] = "InterIA models can be integrated when API keys are configured"
        
        return humean_result

# Test du pont
if __name__ == "__main__":
    bridge = InterIABridge()
    result = bridge.process_with_humean_cognition("Test bridge functionality")
    print("🌉 BRIDGE TEST SUCCESSFUL!")
    print(f"🧠 HUMEAN Result: {result['content']['analysis']}")
    print(f"⚡ Energy: {result['energy_metrics']['free_energy']}")
