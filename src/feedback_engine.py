"""
Module de génération de feedback intelligent
"""


class FeedbackEngine:
    """Génère des feedbacks intelligents"""
    
    def generate_feedback(self, analysis):
        """
        Génère un feedback basé sur l'analyse
        
        Args:
            analysis: dict contenant les résultats de l'analyse
        
        Returns:
            dict avec 'emoji', 'overall', 'messages'
        """
        score = analysis['score']
        regularity = analysis['regularity']
        speed = analysis['speed']
        
        feedback = {
            'emoji': '',
            'overall': '',
            'messages': []
        }
        
        # Feedback global basé sur le score
        if score >= 90:
            feedback['emoji'] = '🔥'
            feedback['overall'] = "Performance exceptionnelle !"
        elif score >= 75:
            feedback['emoji'] = '💪'
            feedback['overall'] = "Très bonne séance !"
        elif score >= 60:
            feedback['emoji'] = '👍'
            feedback['overall'] = "Bonne performance"
        else:
            feedback['emoji'] = '⚠️'
            feedback['overall'] = "Performance moyenne"
        
        # Feedback sur la régularité
        if regularity < 50:
            feedback['messages'].append("⚠️ Rythme irrégulier. Essaie de garder un tempo constant.")
        elif regularity < 70:
            feedback['messages'].append("💡 Régularité acceptable, mais peut être améliorée.")
        else:
            feedback['messages'].append("✅ Excellent rythme ! Continue comme ça.")
        
        # Feedback sur la vitesse
        if speed > 40:
            feedback['messages'].append("🐇 Trop rapide ! Ralentis pour une meilleure forme.")
        elif speed < 15:
            feedback['messages'].append("🐢 Un peu lent. Tu peux accélérer légèrement.")
        else:
            feedback['messages'].append("✅ Vitesse parfaite !")
        
        return feedback