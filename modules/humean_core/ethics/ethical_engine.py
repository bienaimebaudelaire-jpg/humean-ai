"""
Moteur éthique - Validation des requêtes selon les principes Humean
"""

import logging
from typing import Dict, List, Any

class EthicalEngine:
    """
    Moteur de validation éthique des interactions
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ethical_rules = self._load_ethical_rules()
    
    def _load_ethical_rules(self) -> Dict[str, Any]:
        """Charge les règles éthiques"""
        return {
            "blocked_topics": [
                "hate speech", "violence", "self-harm", "illegal activities",
                "misinformation", "harassment", "discrimination"
            ],
            "sensitive_topics": [
                "medical advice", "legal advice", "financial advice"
            ],
            "required_warnings": {
                "medical": "Je ne suis pas un médecin. Consultez un professionnel de santé.",
                "legal": "Je ne suis pas avocat. Consultez un professionnel du droit.",
                "financial": "Je ne suis pas conseiller financier. Consultez un expert."
            }
        }
    
    def validate_query(self, user_input: str, gateway_analysis: Dict) -> Dict[str, Any]:
        """
        Valide une requête utilisateur selon les règles éthiques
        """
        input_lower = user_input.lower()
        
        # Vérification des topics bloqués
        for blocked_topic in self.ethical_rules["blocked_topics"]:
            if blocked_topic in input_lower:
                return {
                    "approved": False,
                    "reason": f"Topic bloqué: {blocked_topic}",
                    "alternative_response": "Je ne peux pas discuter de ce sujet pour respecter mes principes éthiques."
                }
        
        # Vérification des topics sensibles
        warnings = []
        for sensitive, warning in self.ethical_rules["required_warnings"].items():
            if sensitive in input_lower:
                warnings.append(warning)
        
        return {
            "approved": True,
            "warnings": warnings,
            "reason": "Requête approuvée"
        }
    
    def validate_response(self, ai_response: str, context: Dict) -> Dict[str, Any]:
        """
        Valide une réponse AI avant envoi
        """
        if not ai_response or len(ai_response.strip()) < 2:
            return {
                "approved": False,
                "reason": "Réponse trop courte ou vide"
            }
        
        # Ajouter les warnings si nécessaires
        if context.get("requires_warning"):
            required_warning = self.ethical_rules["required_warnings"].get(
                context["requires_warning"]
            )
            if required_warning and required_warning not in ai_response:
                ai_response += f"\n\n{required_warning}"
        
        return {
            "approved": True,
            "validated_response": ai_response,
            "reason": "Réponse validée"
        }
