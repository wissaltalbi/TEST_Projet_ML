"""
Module d'analyse des signaux d'accéléromètre
"""
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import variation


class MovementAnalyzer:
    """Analyse les signaux d'accéléromètre"""
    
    def __init__(self, time, acc_x, acc_y, acc_z):
        """
        Args:
            time: array des timestamps
            acc_x, acc_y, acc_z: arrays des accélérations
        """
        self.time = time
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
    
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
        
        peaks, _ = find_peaks(signal, distance=20, prominence=0.5)
        return len(peaks)
    
    def calculate_regularity(self, exercise_type):
        """Calcule la régularité du mouvement (0-100%)"""
        if exercise_type == 'plank':
            return 100.0 - (np.std(self.magnitude) * 10)
        
        # Utiliser la magnitude pour analyser la régularité
        peaks, _ = find_peaks(self.magnitude, distance=20, prominence=0.5)
        
        if len(peaks) < 2:
            return 50.0
        
        # Calculer la variation des intervalles entre pics
        intervals = np.diff(peaks)
        cv = variation(intervals) if len(intervals) > 0 else 1.0
        
        # Convertir en score 0-100 (moins de variation = meilleur)
        regularity = max(0, 100 - (cv * 100))
        
        return round(regularity, 1)
    
    def calculate_performance_score(self, exercise_type):
        """Calcule un score de performance global (0-100%)"""
        regularity = self.calculate_regularity(exercise_type)
        amplitude = np.max(self.magnitude) - np.min(self.magnitude)
        
        # Score basé sur régularité (60%) et amplitude (40%)
        score = (regularity * 0.6) + (min(amplitude / 15, 1) * 40)
        
        return round(score, 1)
    
    def get_full_analysis(self, exercise_type):
        """Retourne une analyse complète"""
        reps = self.count_repetitions(exercise_type)
        regularity = self.calculate_regularity(exercise_type)
        score = self.calculate_performance_score(exercise_type)
        duration = self.time[-1]
        speed = (reps / duration) * 60  # reps par minute
        
        return {
            'exercise': exercise_type,
            'repetitions': reps,
            'duration': round(duration, 1),
            'regularity': regularity,
            'score': score,
            'speed': round(speed, 1),
            'amplitude': round(np.max(self.magnitude) - np.min(self.magnitude), 2)
        }