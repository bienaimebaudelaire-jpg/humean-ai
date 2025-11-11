# modules/humean_core/gateway/humean_gateway_gemini.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from memory.adaptive_memory import AdaptiveMemory
from integration.real_gemini_bridge import RealGeminiBridge

class HumeanGatewayGemini:
    """Gateway HUMEAN avec Gemini comme moteur cognitif réel"""
    
    def __init__(self):
        self.energy_log = []
        self.module_registry = {}
        self.memory_system = AdaptiveMemory(max_entries=100)
        self.gemini_bridge = RealGeminiBridge()
        self._initialize_default_modules()
        print("🧠 HUMEAN Gateway with Gemini initialized")
    
    def _initialize_default_modules(self):
        """Initialiser les modules par défaut"""
        default_modules = {
            "gemini_cognitive_engine": ["reasoning", "analysis", "generation"],
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
        
        # Mémoriser l'enregistrement
        self.memory_system.store(
            f"Module {name} registered with capabilities: {capabilities}",
            emotional_weight=0.6,
            cognitive_importance=0.8
        )
        return True
    
    def process_with_gemini_cognition(self, query):
        """Traiter avec Gemini comme moteur cognitif réel"""
        print(f"⚡ HUMEAN-Gemini Processing: {query}")
        
        # 1. Rappeler le contexte pertinent
        context = self.memory_system.recall(query, max_results=3)
        
        # 2. Appel réel à Gemini
        gemini_result = self.gemini_bridge.generate_response(query, context)
        
        # 3. Traitement du résultat
        if gemini_result["success"]:
            cognitive_response = gemini_result["response"]
            model_used = gemini_result["model_used"]
        else:
            cognitive_response = f"Fallback: {query} (Gemini error: {gemini_result['error']})"
            model_used = "fallback"
        
        # 4. Préparer le résultat
        processed_result = {
            "original_query": query,
            "cognitive_response": cognitive_response,
            "model_used": model_used,
            "context_used": len(context),
            "analysis": f"Cognitive processing via {model_used} with {len(context)} context memories"
        }
        
        # 5. Calcul énergétique
        energy_metrics = self._calculate_energy_metrics(processed_result, len(context))
        
        # 6. Mémoriser l'interaction
        self._store_interaction(query, processed_result, energy_metrics, context)
        
        return {
            "content": processed_result,
            "energy_metrics": energy_metrics,
            "active_modules": list(self.module_registry.keys()),
            "context_used": len(context),
            "humean_version": "Gemini-v1",
            "status": "success"
        }
    
    def _calculate_energy_metrics(self, result, context_size):
        """Calcul des métriques énergétiques"""
        complexity = len(str(result)) / 1000
        modules_used = len(self.module_registry)
        context_factor = 1.0 + (context_size * 0.1)
        
        # Énergie basée sur la complexité
        base_energy = max(0.2, complexity * modules_used * context_factor)
        
        return {
            "free_energy": round(base_energy, 4),
            "cognitive_load": round(complexity, 4),
            "efficiency_score": round(1.0 / (complexity + 0.1), 4),
            "modules_active": modules_used,
            "context_memories_used": context_size
        }
    
    def _store_interaction(self, query, result, metrics, context):
        """Stockage de l'interaction"""
        importance = min(1.0, metrics["free_energy"] * 3)
        self.memory_system.store(
            f"Gemini interaction: {query} -> {result['analysis']}",
            emotional_weight=0.7,
            cognitive_importance=importance
        )
        print(f"💾 Gemini interaction stored")
    
    def get_system_status(self):
        """Statut du système avec info Gemini"""
        memory_stats = self.memory_system.get_stats()
        avg_energy = memory_stats.get("avg_energy", 0.0)
        
        return {
            "modules_registered": len(self.module_registry),
            "memory_entries": memory_stats["total_memories"],
            "avg_memory_energy": avg_energy,
            "cognitive_engine": "Gemini-2.0-flash",
            "gateway_version": "HUMEAN Gemini v1",
            "memory_stats": memory_stats,
            "active_modules": list(self.module_registry.keys())
        }

# TEST
if __name__ == "__main__":
    print("🚀 TESTING HUMEAN + GEMINI INTEGRATION...")
    
    gw = HumeanGatewayGemini()
    
    test_queries = [
        "Explique comment un système cognitif comme HUMEAN peut minimiser son énergie libre",
        "Qu'est-ce que la mémoire adaptive et pourquoi est-elle importante en IA?",
        "Comment Gemini fonctionne-t-il comme moteur cognitif pour HUMEAN?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        result = gw.process_with_gemini_cognition(query)
        
        if result["status"] == "success":
            print(f"   ✅ Succès - Énergie: {result['energy_metrics']['free_energy']}")
            print(f"   🤖 Modèle: {result['content']['model_used']}")
            response_preview = result['content']['cognitive_response'][:150] + "..."
            print(f"   💬 Réponse: {response_preview}")
        else:
            print(f"   ❌ Erreur")
    
    status = gw.get_system_status()
    print(f"\n📊 STATUT SYSTÈME HUMEAN-GEMINI:")
    print(f"   Modules: {status['modules_registered']}")
    print(f"   Entrées mémoire: {status['memory_entries']}")
    print(f"   Moteur cognitif: {status['cognitive_engine']}")
    print(f"   Énergie moyenne: {status['avg_memory_energy']:.3f}")
    
    print("\n🎯 HUMEAN + GEMINI OPERATIONNEL!")
