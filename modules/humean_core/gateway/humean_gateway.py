# modules/humean_core/gateway/humean_gateway.py
import json
import sys
from pathlib import Path

class HumeanGateway:
    """Gateway HUMEAN - Extension cognitive du système interIA"""
    
    def __init__(self):
        self.energy_log = []
        self.module_registry = {}
        self.memory_buffer = []
        print("🧠 HUMEAN Gateway initialized")
    
    def register_cognitive_module(self, name, capabilities):
        """Enregistrer un module cognitif HUMEAN"""
        self.module_registry[name] = {
            "capabilities": capabilities,
            "energy_cost": 0.0,
            "activation_count": 0
        }
        print(f"✅ HUMEAN Module registered: {name} -> {capabilities}")
        return True
    
    def process_with_cognitive_layer(self, query):
        """Traiter avec la couche cognitive HUMEAN"""
        print(f"⚡ HUMEAN Processing: {query}")
        
        # 1. Logique de traitement cognitive
        processed_result = self._cognitive_processing(query)
        
        # 2. Calcul des métriques énergétiques
        energy_metrics = self._calculate_energy_metrics(processed_result)
        
        # 3. Mémorisation
        self._store_in_memory(query, processed_result, energy_metrics)
        
        return {
            "content": processed_result,
            "energy_metrics": energy_metrics,
            "active_modules": list(self.module_registry.keys()),
            "humean_version": "0.1",
            "status": "success"
        }
    
    def _cognitive_processing(self, query):
        """Traitement cognitif simplifié"""
        return {
            "original_query": query,
            "processed_by": "HUMEAN Cognitive Layer",
            "analysis": f"Cognitive analysis of: '{query}'",
            "modules_activated": len(self.module_registry)
        }
    
    def _calculate_energy_metrics(self, result):
        """Calcul des métriques énergétiques HUMEAN"""
        complexity = len(str(result)) / 1000
        modules_used = len(self.module_registry)
        
        return {
            "free_energy": round(complexity * modules_used, 4),
            "cognitive_load": round(complexity, 4),
            "efficiency_score": round(1.0 / (complexity + 0.1), 4),
            "modules_active": modules_used
        }
    
    def _store_in_memory(self, query, result, metrics):
        """Stockage dans la mémoire HUMEAN"""
        from datetime import datetime
        memory_entry = {
            "timestamp": datetime.now().isoformat() + "Z",
            "query": query,
            "result": result,
            "energy_used": metrics["free_energy"],
            "modules_involved": list(self.module_registry.keys())
        }
        self.memory_buffer.append(memory_entry)
        print(f"💾 Memory stored: {len(self.memory_buffer)} entries")
    
    def get_system_status(self):
        """Statut du système HUMEAN"""
        return {
            "modules_registered": len(self.module_registry),
            "memory_entries": len(self.memory_buffer),
            "total_energy_used": sum(entry["energy_used"] for entry in self.memory_buffer),
            "gateway_version": "HUMEAN v0.1"
        }

# TEST DU GATEWAY HUMEAN
if __name__ == "__main__":
    print("🚀 INITIALISATION HUMEAN GATEWAY...")
    
    # Initialiser le gateway
    gw = HumeanGateway()
    
    # Enregistrer les modules cognitifs
    gw.register_cognitive_module("language_processor", ["text_analysis", "semantic_processing"])
    gw.register_cognitive_module("memory_controller", ["short_term", "associative_recall"])
    gw.register_cognitive_module("ethics_validator", ["value_alignment", "harm_prevention"])
    gw.register_cognitive_module("energy_regulator", ["free_energy_minimization"])
    
    print("\n🔧 TESTING COGNITIVE PROCESSING...")
    
    # Tester le traitement cognitif
    test_queries = [
        "Hello HUMEAN - testing cognitive integration",
        "What is the meaning of consciousness?",
        "Calculate energy metrics for this interaction"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        result = gw.process_with_cognitive_layer(query)
        print(f"   ⚡ Energy: {result['energy_metrics']['free_energy']}")
        print(f"   🧠 Modules: {result['active_modules']}")
    
    print(f"\n📊 SYSTÈME HUMEAN - STATUT FINAL:")
    status = gw.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ HUMEAN GATEWAY OPÉRATIONNEL! 🎯")