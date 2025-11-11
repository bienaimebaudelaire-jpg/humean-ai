"""
GESTIONNAIRE INTELLIGENT DES GATEWAYS - Version finale
"""

import logging
from typing import Dict, List, Optional, Any

class GatewayManager:
    """Gère les différents gateways avec les bonnes classes"""
    
    def __init__(self, config_manager=None):
        self.logger = logging.getLogger(__name__)
        self.config = config_manager
        self.available_gateways = {}
        self.active_gateway = None
        self.gateway_priority = []
        
        self._discover_gateways()
        self._select_best_gateway()
    
    def _discover_gateways(self):
        """Découvre les gateways avec leurs vraies classes"""
        self.logger.info("🔍 Découverte des gateways...")
        
        gateway_candidates = [
            # (nom, module, classe, priorité, args d'init)
            ("test", "gateway.test_gateway", "TestGateway", 0, True),  # Priorité haute pour les tests
            ("classic", "gateway.humean_gateway", "HumeanGateway", 1, False),
            ("gemini", "gateway.humean_gateway_gemini", "humean_gateway_gemini", 2, True),
            ("ollama", "gateway.humean_gateway_ollama", "humean_gateway_ollama", 3, True),
            ("v2", "gateway.humean_gateway_v2", "humean_gateway_v2", 4, True)
        ]
        
        for name, module_path, class_name, priority, takes_config in gateway_candidates:
            try:
                module = __import__(module_path, fromlist=[class_name])
                gateway_class = getattr(module, class_name)
                
                # Initialisation avec ou sans config selon la classe
                if takes_config:
                    gateway_instance = gateway_class(self.config)
                else:
                    gateway_instance = gateway_class()
                
                self.available_gateways[name] = {
                    'instance': gateway_instance,
                    'class': gateway_class,
                    'priority': priority,
                    'status': 'available',
                    'takes_config': takes_config
                }
                
                self.gateway_priority.append((name, priority))
                self.logger.info(f"✅ Gateway {name} ({class_name}) initialisé")
                
            except Exception as e:
                self.logger.warning(f"⚠️ Gateway {name} ({class_name}) non disponible: {e}")
        
        self.gateway_priority.sort(key=lambda x: x[1])
        self.logger.info(f"📊 Gateways disponibles: {list(self.available_gateways.keys())}")
    
    def _select_best_gateway(self):
        """Sélectionne le meilleur gateway disponible"""
        for gateway_name, _ in self.gateway_priority:
            if gateway_name in self.available_gateways:
                self.active_gateway = gateway_name
                self.logger.info(f"🎯 Gateway actif: {gateway_name}")
                return
        
        self.logger.error("❌ Aucun gateway disponible")
        self.active_gateway = None
    
    def analyze_query(self, user_input: str) -> Dict[str, Any]:
        """Analyse une requête via le gateway actif"""
        if not self.active_gateway:
            return self._fallback_analysis(user_input)
        
        try:
            gateway = self.available_gateways[self.active_gateway]['instance']
            
            if hasattr(gateway, 'analyze_query'):
                result = gateway.analyze_query(user_input)
                self.logger.info(f"📊 Analyse réussie avec {self.active_gateway}")
                return result
            else:
                self.logger.warning(f"⚠️ Méthode analyze_query non disponible pour {self.active_gateway}")
                return self._fallback_analysis(user_input)
                
        except Exception as e:
            self.logger.error(f"❌ Erreur analyse avec {self.active_gateway}: {e}")
            return self._fallback_analysis(user_input)
    
    def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Génère une réponse via le gateway actif"""
        if not self.active_gateway:
            return self._fallback_response(context)
        
        try:
            gateway = self.available_gateways[self.active_gateway]['instance']
            
            if hasattr(gateway, 'generate_response'):
                result = gateway.generate_response(context)
                self.logger.info(f"💬 Génération réussie avec {self.active_gateway}")
                return result
            else:
                self.logger.warning(f"⚠️ Méthode generate_response non disponible pour {self.active_gateway}")
                return self._fallback_response(context)
                
        except Exception as e:
            self.logger.error(f"❌ Erreur génération avec {self.active_gateway}: {e}")
            return self._fallback_response(context)
    
    def _fallback_analysis(self, user_input: str) -> Dict[str, Any]:
        """Analyse de fallback"""
        return {
            "intent": "unknown",
            "sentiment": "neutral", 
            "topics": ["fallback"],
            "confidence": 0.1,
            "language": "fr"
        }
    
    def _fallback_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Réponse de fallback"""
        user_input = context.get('user_input', 'Unknown')
        return {
            "response": f"🔧 [Mode Fallback] J'ai reçu: '{user_input}'. Gateways en cours de configuration.",
            "confidence": 0.1,
            "model_used": "fallback",
            "success": False
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut des gateways"""
        status = {
            "active_gateway": self.active_gateway,
            "available_gateways": list(self.available_gateways.keys()),
            "gateway_details": {}
        }
        
        for name, info in self.available_gateways.items():
            status["gateway_details"][name] = {
                "priority": info['priority'],
                "status": info['status'],
                "takes_config": info['takes_config']
            }
        
        return status
    
    def switch_gateway(self, gateway_name: str) -> bool:
        """Change le gateway actif"""
        if gateway_name in self.available_gateways:
            self.active_gateway = gateway_name
            self.logger.info(f"🔄 Gateway changé vers: {gateway_name}")
            return True
        else:
            self.logger.error(f"❌ Gateway {gateway_name} non disponible")
            return False
