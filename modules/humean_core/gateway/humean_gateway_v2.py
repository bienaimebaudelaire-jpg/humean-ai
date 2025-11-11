# modules/humean_core/gateway/humean_gateway_v2.py
import json
import sys
from pathlib import Path

# Importer la mémoire adaptive
sys.path.append(str(Path(__file__).parent.parent))
from memory.adaptive_memory import AdaptiveMemory

class HumeanGatewayV2:
    """Gateway HUMEAN v2 avec mémoire intégrée"""
    
    def __init__(self):
        self.energy_log = []
        self.module_registry = {}
        self.memory_system = AdaptiveMemory(max_entries=100)
        self._initialize_default_modules()
        print("🧠 HUMEAN Gateway v2 initialized with Adaptive Memory")
    
    def _initialize_default_modules(self):
        """Initialiser les modules par défaut"""
        default_modules = {
            "language_processor": ["text_analysis", "semantic_processing"],
            "memory_controller": ["short_term", "associative_recall"], 
            "ethics_validator": ["value_alignment", "harm_prevention"],
            "energy_regulator": ["free_energy_minimization"]
        }
        
        for name, capabilities in default_modules.items():
            self.register_cognitive_module(name, capabilities)
    
    def register_cognitive_module(self, name, capabilities):
        """Enregistrer un module cognitif HUMEAN"""
        self.module_registry[name] = {
            "capabilities": capabilities,
            "energy_cost": 0.0,
            "activation_count": 0
        }
        print(f"✅ HUMEAN Module registered: {name}")
        
        # Mémoriser l'enregistrement avec plus d'énergie
        self.memory_system.store(
            f"Module {name} registered with capabilities: {capabilities}",
            emotional_weight=0.6,  # Augmenté
            cognitive_importance=0.8  # Augmenté
        )
        return True
    
    def process_with_cognitive_layer(self, query):
        """Traiter avec mémoire contextuelle"""
        print(f"⚡ HUMEAN Processing: {query}")
        
        # 1. Rappeler le contexte pertinent
        context = self.memory_system.recall(query, max_results=3)
        
        # 2. Traitement cognitif avec contexte
        processed_result = self._cognitive_processing(query, context)
        
        # 3. Calcul des métriques énergétiques
        energy_metrics = self._calculate_energy_metrics(processed_result, len(context))
        
        # 4. Mémoriser l'interaction
        self._store_interaction(query, processed_result, energy_metrics, context)
        
        return {
            "content": processed_result,
            "energy_metrics": energy_metrics,
            "active_modules": list(self.module_registry.keys()),  # Corrigé
            "context_used": len(context),
            "humean_version": "0.2",
            "status": "success"
        }
    
    def _cognitive_processing(self, query, context):
        """Traitement cognitif avec contexte"""
        context_summary = [mem["event"] for mem in context] if context else ["No relevant context"]
        
        return {
            "original_query": query,
            "processed_by": "HUMEAN Cognitive Layer v2",
            "context_used": context_summary,
            "analysis": f"Cognitive analysis with {len(context)} context memories",
            "modules_activated": len(self.module_registry)
        }
    
    def _calculate_energy_metrics(self, result, context_size):
        """Calcul des métriques énergétiques avec contexte"""
        complexity = len(str(result)) / 1000
        modules_used = len(self.module_registry)
        context_factor = 1.0 + (context_size * 0.1)
        
        # Énergie de base pour assurer > 0
        base_energy = max(0.1, complexity * modules_used * context_factor)
        
        return {
            "free_energy": round(base_energy, 4),
            "cognitive_load": round(complexity, 4),
            "efficiency_score": round(1.0 / (complexity + 0.1), 4),
            "modules_active": modules_used,
            "context_memories_used": context_size
        }
    
    def _store_interaction(self, query, result, metrics, context):
        """Stockage de l'interaction complète"""
        interaction_entry = {
            "query": query,
            "result": result,
            "energy_used": metrics["free_energy"],
            "context_size": len(context),
            "modules_involved": list(self.module_registry.keys())
        }
        
        # Stocker avec pondération énergétique basée sur l'énergie réelle
        importance = min(1.0, metrics["free_energy"] * 3)  # Augmenté le multiplicateur
        self.memory_system.store(
            f"Interaction: {query} -> {result['analysis']}",
            emotional_weight=0.7,  # Augmenté
            cognitive_importance=importance
        )
        
        print(f"💾 Interaction stored (importance: {importance})")
    
    def get_system_status(self):
        """Statut complet du système HUMEAN"""
        memory_stats = self.memory_system.get_stats()
        
        return {
            "modules_registered": len(self.module_registry),
            "memory_entries": memory_stats["total_memories"],
            "avg_memory_energy": memory_stats["avg_energy"],
            "total_energy_used": sum(entry["energy_used"] for entry in self.energy_log),
            "gateway_version": "HUMEAN v0.2",
            "memory_stats": memory_stats,
            "active_modules": list(self.module_registry.keys())  # Ajouté pour le dashboard
        }

# TEST DU GATEWAY V2
if __name__ == "__main__":
    print("🚀 INITIALISATION HUMEAN GATEWAY v2...")
    
    gw = HumeanGatewayV2()
    
    print("\n🔧 TESTING COGNITIVE PROCESSING WITH MEMORY...")
    
    test_queries = [
        "Hello HUMEAN - testing improved energy system",
        "How does your adaptive memory work?",
        "What modules are currently active?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        result = gw.process_with_cognitive_layer(query)
        print(f"   ⚡ Energy: {result['energy_metrics']['free_energy']}")
        print(f"   🧠 Modules: {result['active_modules']}")
        print(f"   📚 Context used: {result['context_used']} memories")
    
    status = gw.get_system_status()
    print(f"\n📊 SYSTEM STATUS:")
    print(f"   Memory entries: {status['memory_entries']}")
    print(f"   Avg memory energy: {status['avg_memory_energy']:.3f}")
    
    print("\n✅ HUMEAN GATEWAY v2 IMPROVED OPERATIONNEL! 🎯")
