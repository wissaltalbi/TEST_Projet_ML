"""
Module d'analyse des signaux d'accéléromètre
Corrigé pour gérer pandas Series et numpy arrays
"""
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import variation


class MovementAnalyzer:
    """Analyse les signaux d'accéléromètre"""
    
    def __init__(self, time, acc_x, acc_y, acc_z):
        """
        Args:
            time: array des timestamps (pandas Series ou numpy array)
            acc_x, acc_y, acc_z: arrays des accélérations
        """
        # ✅ TOUJOURS convertir en numpy arrays pour éviter les problèmes
        self.time = self._to_numpy(time)
        self.acc_x = self._to_numpy(acc_x)
        self.acc_y = self._to_numpy(acc_y)
        self.acc_z = self._to_numpy(acc_z)
        self.magnitude = np.sqrt(self.acc_x**2 + self.acc_y**2 + self.acc_z**2)
    
    @staticmethod
    def _to_numpy(data):
        """Convertit n'importe quel type de données en numpy array"""
        if isinstance(data, np.ndarray):
            return data
        try:
            # Pour pandas Series, utiliser .values
            return data.values if hasattr(data, 'values') else np.array(data)
        except:
            return np.array(data)
    
    def count_repetitions(self, exercise_type):
        """Compte le nombre de répétitions"""
        if exercise_type == 'plank':
            return 1
        
        # Détection de pics selon l'axe principal
        if exercise_type in ['squat', 'jumping_jack']:
            signal = self.acc_z
        elif exercise_type == 'pushup':
            signal = self.acc_y
        else:  # curl
            signal = self.magnitude
        
        try:
            peaks, _ = find_peaks(signal, distance=20, prominence=0.5)
            return len(peaks)
        except Exception as e:
            print(f"Erreur count_repetitions: {e}")
            return 0
    
    def calculate_regularity(self, exercise_type):
        """Calcule la régularité du mouvement (0-100%)"""
        try:
            if exercise_type == 'plank':
                std_val = float(np.std(self.magnitude))
                return max(0, min(100, 100.0 - (std_val * 10)))
            
            # Utiliser la magnitude pour analyser la régularité
            peaks, _ = find_peaks(self.magnitude, distance=20, prominence=0.5)
            
            if len(peaks) < 2:
                return 50.0
            
            # Calculer la variation des intervalles entre pics
            intervals = np.diff(peaks)
            if len(intervals) == 0:
                return 50.0
            
            cv = variation(intervals)
            
            # Convertir en score 0-100 (moins de variation = meilleur)
            regularity = max(0, 100 - (cv * 100))
            
            return round(float(regularity), 1)
        except Exception as e:
            print(f"Erreur calculate_regularity: {e}")
            return 50.0
    
    def calculate_performance_score(self, exercise_type):
        """Calcule un score de performance global (0-100%)"""
        try:
            regularity = self.calculate_regularity(exercise_type)
            
            # ✅ Utiliser min() et max() de numpy pour être sûr
            amplitude = float(np.max(self.magnitude) - np.min(self.magnitude))
            
            # Score basé sur régularité (60%) et amplitude (40%)
            score = (regularity * 0.6) + (min(amplitude / 15, 1) * 40)
            
            return round(float(score), 1)
        except Exception as e:
            print(f"Erreur calculate_performance_score: {e}")
            return 50.0
    
    def get_full_analysis(self, exercise_type):
        """Retourne une analyse complète"""
        try:
            reps = self.count_repetitions(exercise_type)
            regularity = self.calculate_regularity(exercise_type)
            score = self.calculate_performance_score(exercise_type)
            
            # ✅ Accès sécurisé au dernier élément
            duration = float(self.time[-1]) if len(self.time) > 0 else 1.0
            
            # Éviter division par zéro
            speed = (reps / duration) * 60 if duration > 0 else 0
            
            amplitude = float(np.max(self.magnitude) - np.min(self.magnitude))
            
            return {
                'exercise': exercise_type,
                'repetitions': int(reps),
                'duration': round(duration, 1),
                'regularity': round(regularity, 1),
                'score': round(score, 1),
                'speed': round(speed, 1),
                'amplitude': round(amplitude, 2)
            }
        except Exception as e:
            print(f"Erreur get_full_analysis: {e}")
            # Retourner des valeurs par défaut en cas d'erreur
            return {
                'exercise': exercise_type,
                'repetitions': 0,
                'duration': 0.0,
                'regularity': 50.0,
                'score': 50.0,
                'speed': 0.0,
                'amplitude': 0.0
            }