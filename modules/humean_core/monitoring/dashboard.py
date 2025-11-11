# modules/humean_core/monitoring/dashboard.py
import json
from datetime import datetime
import sys
from pathlib import Path

# Corriger l'import
sys.path.append(str(Path(__file__).parent.parent))
from gateway.humean_gateway_v2 import HumeanGatewayV2

class HumeanDashboard:
    """Dashboard de monitoring HUMEAN en temps réel"""
    
    def __init__(self, gateway):
        self.gateway = gateway
        self.operation_log = []
    
    def log_operation(self, operation, details):
        """Journaliser les opérations"""
        entry = {
            "timestamp": datetime.now().isoformat() + "Z",
            "operation": operation,
            "details": details
        }
        self.operation_log.append(entry)
        print(f"📊 Dashboard: {operation}")
    
    def generate_system_report(self):
        """Générer un rapport système complet"""
        status = self.gateway.get_system_status()
        
        # Corriger la clé manquante
        active_modules = status.get("modules_registered", 0)
        
        report = {
            "generated_at": datetime.now().isoformat() + "Z",
            "system_status": status,
            "recent_operations": self.operation_log[-10:],  # 10 dernières
            "performance_metrics": {
                "energy_efficiency": status["memory_stats"]["avg_energy"],
                "cognitive_density": status["memory_entries"] / max(1, active_modules),
                "system_health": "OPTIMAL" if status["memory_stats"]["avg_energy"] > 0.3 else "LEARNING"
            }
        }
        
        return report

# Utilisation
if __name__ == "__main__":
    gw = HumeanGatewayV2()
    dashboard = HumeanDashboard(gw)
    
    # Simuler des opérations
    dashboard.log_operation("system_start", {"version": "HUMEAN v0.2"})
    dashboard.log_operation("module_registration", {"module": "test_module"})
    
    # Générer le rapport
    report = dashboard.generate_system_report()
    print("📈 HUMEAN DASHBOARD REPORT:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
