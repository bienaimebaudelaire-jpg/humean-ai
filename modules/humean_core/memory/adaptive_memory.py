# modules/humean_core/memory/adaptive_memory.py
import json
from datetime import datetime, timedelta

class AdaptiveMemory:
    """Mémoire adaptive HUMEAN avec pondération énergétique"""
    
    def __init__(self, max_entries=1000):
        self.memories = []
        self.max_entries = max_entries
        self.energy_threshold = 0.1
    
    def store(self, event, emotional_weight=0.5, cognitive_importance=0.5):
        """Stocker un événement avec pondérations"""
        memory_entry = {
            "timestamp": datetime.now().isoformat() + "Z",
            "event": event,
            "emotional_weight": emotional_weight,
            "cognitive_importance": cognitive_importance,
            "energy_value": emotional_weight * cognitive_importance,
            "access_count": 0
        }
        
        self.memories.append(memory_entry)
        
        # Limiter la taille de la mémoire
        if len(self.memories) > self.max_entries:
            self._compress_memories()
        
        print(f"💾 Memory stored (energy: {memory_entry['energy_value']})")
        return memory_entry
    
    def recall(self, query, max_results=5):
        """Rappeler les mémoires les plus pertinentes"""
        scored_memories = []
        
        for memory in self.memories[-100:]:  # Dernières 100 entrées
            score = self._compute_relevance_score(memory, query)
            scored_memories.append((score, memory))
        
        # Trier par score de pertinence
        scored_memories.sort(reverse=True)
        
        # Retourner les plus pertinents
        results = [memory for score, memory in scored_memories[:max_results]]
        
        # Mettre à jour le compteur d'accès
        for memory in results:
            memory["access_count"] += 1
        
        print(f"🔍 Memory recall: {len(results)} relevant memories found")
        return results
    
    def _compute_relevance_score(self, memory, query):
        """Calculer le score de pertinence"""
        # Score basé sur similarité sémantique simple
        text_similarity = self._simple_text_similarity(str(memory["event"]), query)
        
        # Facteurs temporels (récence)
        memory_time = datetime.fromisoformat(memory["timestamp"].replace('Z', ''))
        time_diff = (datetime.now() - memory_time).total_seconds() / 3600  # heures
        recency_factor = 1.0 / (1.0 + time_diff/24)  # Décroissance sur 24h
        
        # Combiner les scores
        relevance = (text_similarity * 0.6 + 
                    memory["energy_value"] * 0.2 + 
                    recency_factor * 0.2)
        
        return relevance
    
    def _simple_text_similarity(self, text1, text2):
        """Similarité textuelle simplifiée"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _compress_memories(self):
        """Compresser les mémoires peu utilisées"""
        if len(self.memories) <= self.max_entries:
            return
        
        # Supprimer les mémoires avec faible énergie et peu d'accès
        self.memories = [
            mem for mem in self.memories 
            if mem["energy_value"] > self.energy_threshold or mem["access_count"] > 0
        ]
        
        print(f"🧹 Memory compressed: {len(self.memories)} entries remaining")
    
    def get_stats(self):
        """Obtenir les statistiques de la mémoire"""
        if not self.memories:
            return {"total_memories": 0}
        
        return {
            "total_memories": len(self.memories),
            "avg_energy": sum(m["energy_value"] for m in self.memories) / len(self.memories),
            "high_energy_memories": len([m for m in self.memories if m["energy_value"] > 0.7]),
            "most_accessed": max(self.memories, key=lambda x: x["access_count"])["access_count"]
        }

# TEST
if __name__ == "__main__":
    print("🧠 TESTING ADAPTIVE MEMORY...")
    
    memory = AdaptiveMemory(max_entries=50)
    
    # Stocker quelques mémoires
    memory.store("Apprentissage du concept d'énergie libre", 0.8, 0.9)
    memory.store("Intégration avec le gateway HUMEAN", 0.6, 0.8)
    memory.store("Test du système cognitif", 0.3, 0.5)
    
    # Rappeler des mémoires
    results = memory.recall("énergie libre", max_results=2)
    print(f"📝 Recall results: {len(results)} memories")
    
    # Afficher les stats
    stats = memory.get_stats()
    print("📊 Memory Stats:", stats)
    
    print("✅ ADAPTIVE MEMORY OPERATIONNELLE!")