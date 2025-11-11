# modules/humean_core/gateway/humean_gateway_ollama.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from memory.adaptive_memory import AdaptiveMemory

class HumeanGatewayOllama:
    """Gateway HUMEAN avec moteurs cognitifs"""
    
    def __init__(self):
        self.energy_log = []
        self.module_registry = {}
        self.memory_system = AdaptiveMemory(max_entries=100)
        self._initialize_default_modules()
        print("🧠 HUMEAN Gateway initialized")
    
    def _initialize_default_modules(self):
        """Initialiser les modules par défaut"""
        default_modules = {
            "cognitive_engine": ["reasoning", "analysis", "generation"],
            "memory_controller": ["short_term", "associative_recall"], 
            "energy_regulator": ["free_energy_minimization"]
        }
        
        for name, capabilities in default_modules.items():
            self.register_cognitive_module(name, capabilities)
    
    def register_cognitive_module(self, name, capabilities):
        """Enregistrer un module cognitif"""
        self.module_registry[name] = {
            "capabilities": capabilities,
            "energy_cost": 0.0,
            "activation_count": 0
        }
        print(f"✅ Module registered: {name}")
        return True
    
    def process_with_cognition(self, query):
        """Traiter avec cognition simulée"""
        print(f"⚡ HUMEAN Processing: {query}")
        
        # Simulation pour l'instant
        processed_result = {
            "original_query": query,
            "cognitive_response": f"HUMEAN analysis of: {query}",
            "analysis": "Cognitive processing completed",
            "modules_activated": len(self.module_registry)
        }
        
        energy_metrics = self._calculate_energy_metrics(processed_result)
        
        return {
            "content": processed_result,
            "energy_metrics": energy_metrics,
            "active_modules": list(self.module_registry.keys()),
            "humean_version": "v1.0",
            "status": "success"
        }
    
    def _calculate_energy_metrics(self, result):
        """Calcul des métriques énergétiques"""
        complexity = len(str(result)) / 1000
        modules_used = len(self.module_registry)
        
        return {
            "free_energy": round(complexity * modules_used, 4),
            "cognitive_load": round(complexity, 4),
            "efficiency_score": round(1.0 / (complexity + 0.1), 4),
            "modules_active": modules_used
        }
    
    def get_system_status(self):
        """Statut du système"""
        memory_stats = self.memory_system.get_stats()
        
        # Correction du bug - vérifier si avg_energy existe
        avg_energy = memory_stats.get("avg_energy", 0.0)
        
        return {
            "modules_registered": len(self.module_registry),
            "memory_entries": memory_stats["total_memories"],
            "avg_memory_energy": avg_energy,
            "gateway_version": "HUMEAN v1.0",
            "memory_stats": memory_stats,
            "active_modules": list(self.module_registry.keys())
        }

# TEST
if __name__ == "__main__":
    print("🚀 TESTING HUMEAN GATEWAY...")
    
    gw = HumeanGatewayOllama()
    
    test_queries = [
        "Explique le concept d'énergie libre",
        "Comment fonctionne la mémoire adaptive?",
        "Quels sont tes modules cognitifs?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        result = gw.process_with_cognition(query)
        print(f"   ✅ Succès - Énergie: {result['energy_metrics']['free_energy']}")
    
    status = gw.get_system_status()
    print(f"\n📊 STATUT SYSTÈME:")
    print(f"   Modules: {status['modules_registered']}")
    print(f"   Mémoires: {status['memory_entries']}")
    print(f"   Énergie moyenne: {status['avg_memory_energy']:.3f}")
    
    print("\n🎯 HUMEAN GATEWAY OPERATIONNEL!")
