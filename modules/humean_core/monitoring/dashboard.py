"""
Tableau de bord de monitoring simplifié
"""

import logging
from typing import Dict, Any

class MonitoringDashboard:
    """Tableau de bord de monitoring basique"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.interaction_count = 0
        self.error_count = 0
        self.performance_data = []
    
    def log_interaction(self, interaction_data: Dict[str, Any]):
        """Log une interaction"""
        self.interaction_count += 1
        self.logger.info(f"📊 Interaction #{self.interaction_count} logged")
    
    def log_error(self, error_data: Dict[str, Any]):
        """Log une erreur"""
        self.error_count += 1
        self.logger.error(f"❌ Error #{self.error_count}: {error_data.get('message', 'Unknown')}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques"""
        return {
            "interaction_count": self.interaction_count,
            "error_count": self.error_count,
            "performance": "basic_monitoring"
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport"""
        return {
            "summary": {
                "total_interactions": self.interaction_count,
                "total_errors": self.error_count,
                "success_rate": 1.0 - (self.error_count / max(self.interaction_count, 1))
            },
            "status": "operational"
        }
