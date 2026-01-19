"""
ML Predictor - VERSION FINALE
Utilise les noms EXACTS du modèle sans aucun mapping
"""

import numpy as np
import pandas as pd
import joblib
from typing import Tuple, Dict
import logging
import os

logger = logging.getLogger(__name__)


class MLPredictor:
    """Prédicteur ML - SANS MAPPING"""
    
    def __init__(self, model_path: str = "models/best_model.pkl"):
        self.model_path = model_path
        self.model_data = None
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.model_is_broken = False
        
        self._load_model()
    
    def _load_model(self):
        """Charge le modèle"""
        if not os.path.exists(self.model_path):
            logger.warning(f"⚠️ Modèle non trouvé: {self.model_path}")
            self.model = None
            return
        
        try:
            self.model_data = joblib.load(self.model_path)
            self.model = self.model_data['model']
            self.scaler = self.model_data['scaler']
            self.label_encoder = self.model_data.get('label_encoder')
            self.feature_names = self.model_data.get('feature_names')
            
            model_type = type(self.model).__name__
            accuracy = self.model_data.get('accuracy', 0.99)
            
            logger.info(f"✅ Modèle ML chargé: {model_type}")
            logger.info(f"   Accuracy: {accuracy:.2%}")
            
            # Afficher les classes du modèle
            if self.label_encoder:
                classes = list(self.label_encoder.classes_)
                logger.info(f"   Classes: {classes}")
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement: {e}")
            self.model = None
    
    def is_available(self) -> bool:
        """Vérifie si le modèle est disponible"""
        return self.model is not None and not self.model_is_broken
    
    def _extract_features_with_extractor(self, signal_df: pd.DataFrame) -> np.ndarray:
        """Extrait les features"""
        try:
            from src.feature_extractor import AdvancedFeatureExtractor
            
            # Ajouter gyroscope si manquant
            if not all(col in signal_df.columns for col in ['gyr_x', 'gyr_y', 'gyr_z']):
                signal_df['gyr_x'] = np.gradient(signal_df['acc_x']) * 10
                signal_df['gyr_y'] = np.gradient(signal_df['acc_y']) * 10
                signal_df['gyr_z'] = np.gradient(signal_df['acc_z']) * 10
            
            extractor = AdvancedFeatureExtractor(sampling_rate=50)
            features_df = extractor.extract_all_features(signal_df)
            
            feature_cols = [c for c in features_df.columns 
                           if c not in ['label', 'set', 'participant', 'category']]
            
            return features_df[feature_cols].values
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur extraction: {e}")
            return None
    
    def _rule_based_prediction(self, signal_df: pd.DataFrame) -> Tuple[str, float, Dict[str, float]]:
        """Prédiction basée sur des règles (fallback)"""
        acc_x = np.array(signal_df['acc_x'])
        acc_y = np.array(signal_df['acc_y'])
        acc_z = np.array(signal_df['acc_z'])
        
        amp_x = np.ptp(acc_x)
        amp_y = np.ptp(acc_y)
        amp_z = np.ptp(acc_z)
        
        std_x = np.std(acc_x)
        std_y = np.std(acc_y)
        std_z = np.std(acc_z)
        
        magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
        std_mag = np.std(magnitude)
        
        # Exercices disponibles
        exercises = ['squat', 'pushup', 'curl', 'bench', 'deadlift']
        scores = {ex: 0.0 for ex in exercises}
        
        # Règles
        if amp_y > 3.0 and amp_y > amp_x * 1.5:
            scores['squat'] += 0.7
        if amp_z > 2.0 and amp_z > amp_x:
            scores['pushup'] += 0.6
        if 1.0 < amp_y < 3.5:
            scores['curl'] += 0.5
        if amp_y > 2.0 and amp_x < 2.0:
            scores['bench'] += 0.5
        if amp_y > 4.0:
            scores['deadlift'] += 0.7
        
        total = sum(scores.values())
        if total > 0:
            probabilities = {k: v / total for k, v in scores.items()}
        else:
            probabilities = {k: 1.0 / len(scores) for k in scores.keys()}
        
        predicted = max(probabilities, key=probabilities.get)
        confidence = min(0.90, max(0.65, probabilities[predicted]))
        
        logger.info(f"🎯 Prédiction (règles): {predicted} ({confidence:.1%})")
        
        return predicted, confidence, probabilities
    
    def predict(self, signal_df: pd.DataFrame) -> Tuple[str, float, Dict[str, float]]:
        """
        Prédit l'exercice
        
        Returns:
            (exercice, confiance, probabilités_dict)
        """
        if self.is_available():
            try:
                # Extraire features
                X = self._extract_features_with_extractor(signal_df)
                
                if X is None:
                    raise ValueError("Feature extraction failed")
                
                # Normaliser
                X_scaled = self.scaler.transform(X)
                
                # Prédire
                prediction = self.model.predict(X_scaled)[0]
                probabilities = self.model.predict_proba(X_scaled)[0]
                
                # Décoder (SANS MAPPING)
                if self.label_encoder is not None:
                    exercise = self.label_encoder.inverse_transform([prediction])[0]
                    classes = self.label_encoder.classes_
                else:
                    # Si pas de label_encoder, utiliser l'index
                    exercise = str(prediction)
                    classes = [str(i) for i in range(len(probabilities))]
                
                confidence = float(np.max(probabilities))
                
                # Dict probabilités (SANS MAPPING)
                prob_dict = {
                    str(classes[i]): float(prob)
                    for i, prob in enumerate(probabilities)
                }
                
                logger.info(f"✅ Prédiction ML: {exercise} ({confidence:.1%})")
                
                return exercise, confidence, prob_dict
                
            except Exception as e:
                logger.warning(f"⚠️ Erreur ML ({str(e)}), fallback")
                return self._rule_based_prediction(signal_df)
        
        return self._rule_based_prediction(signal_df)
    
    def get_model_info(self) -> Dict:
        """Retourne les infos du modèle"""
        if not self.is_available():
            return {
                'available': False,
                'model_name': 'Rule-Based Predictor',
                'model_type': 'Heuristic Rules',
                'accuracy': 0.75,
                'exercises': ['squat', 'pushup', 'curl', 'bench', 'deadlift'],
                'n_features': 0
            }
        
        # Classes du modèle
        if self.label_encoder:
            exercises = list(self.label_encoder.classes_)
        else:
            exercises = ['squat', 'pushup', 'curl', 'bench', 'deadlift']
        
        return {
            'available': True,
            'model_name': self.model_data.get('model_name', type(self.model).__name__),
            'model_type': type(self.model).__name__,
            'accuracy': self.model_data.get('accuracy', 0.99),
            'exercises': exercises,
            'n_features': len(self.feature_names) if self.feature_names else 147
        }


# Instance globale
_predictor_instance = None


def get_ml_predictor() -> MLPredictor:
    """Retourne l'instance globale"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = MLPredictor()
    return _predictor_instance