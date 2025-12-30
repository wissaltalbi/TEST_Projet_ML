"""
Module de génération de signaux d'accéléromètre simulés
"""
import numpy as np


class SignalGenerator:
    """Génère des signaux d'accéléromètre simulés pour différents exercices"""
    
    def __init__(self, duration=10, sampling_rate=50):
        """
        Args:
            duration: Durée du signal en secondes
            sampling_rate: Fréquence d'échantillonnage (Hz)
        """
        self.duration = duration
        self.sampling_rate = sampling_rate
        self.time = np.linspace(0, duration, duration * sampling_rate)
    
    def get_exercise_signal(self, exercise_type, reps=None):
        """
        Génère un signal pour un exercice donné
        
        Args:
            exercise_type: 'squat', 'pushup', 'curl', 'jumping_jack', 'plank'
            reps: nombre de répétitions (optionnel)
        
        Returns:
            time, acc_x, acc_y, acc_z (numpy arrays)
        """
        # Répétitions par défaut pour chaque exercice
        exercise_reps = {
            'squat': 10,
            'pushup': 15,
            'curl': 12,
            'jumping_jack': 20,
            'plank': 1
        }
        
        reps = reps or exercise_reps.get(exercise_type, 10)
        freq = reps / self.duration
        
        if exercise_type == 'squat':
            # Mouvement vertical dominant
            acc_z = 9.81 + 3 * np.sin(2 * np.pi * freq * self.time)
            acc_x = 0.5 * np.sin(2 * np.pi * freq * self.time + np.pi/4)
            acc_y = 0.3 * np.cos(2 * np.pi * freq * self.time)
        
        elif exercise_type == 'pushup':
            # Mouvement avant/arrière dominant
            acc_y = 9.81 + 4 * np.sin(2 * np.pi * freq * self.time)
            acc_x = 0.6 * np.cos(2 * np.pi * freq * self.time)
            acc_z = 2 * np.sin(2 * np.pi * freq * self.time + np.pi/3)
        
        elif exercise_type == 'curl':
            # Flexion/extension
            acc_x = 2 * np.sin(2 * np.pi * freq * self.time)
            acc_y = 2.5 * np.cos(2 * np.pi * freq * self.time)
            acc_z = 9.81 + 0.5 * np.sin(2 * np.pi * freq * self.time)
        
        elif exercise_type == 'jumping_jack':
            # Saut + mouvement latéral
            acc_z = 9.81 + 5 * np.sin(2 * np.pi * freq * self.time)
            acc_x = 3 * np.sin(2 * np.pi * freq * self.time + np.pi/2)
            acc_y = np.cos(2 * np.pi * freq * self.time)
        
        elif exercise_type == 'plank':
            # Position statique avec tremblements
            acc_x = np.random.normal(0, 0.1, len(self.time))
            acc_y = np.random.normal(0, 0.1, len(self.time))
            acc_z = 9.81 + np.random.normal(0, 0.1, len(self.time))
        
        else:
            raise ValueError(f"Type d'exercice '{exercise_type}' non reconnu")
        
        # Ajouter du bruit réaliste
        noise = np.random.normal(0, 0.1, len(self.time))
        acc_x += noise
        acc_y += noise
        acc_z += noise
        
        return self.time, acc_x, acc_y, acc_z