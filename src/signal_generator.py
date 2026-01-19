"""
SmartCoach - Générateur de Signaux Réalistes
VERSION FINALE - Noms harmonisés avec config.py et ml_predictor.py
"""

import numpy as np
from scipy import signal
import pandas as pd


class SignalGenerator:
    """Génère des signaux réalistes pour simuler des capteurs de mouvement"""
    
    def __init__(self, sampling_rate=50):
        self.sampling_rate = sampling_rate
        
        # ✅ NOMS HARMONISÉS (compatibles avec config.py)
        self.exercise_patterns = {
            'squat': {
                'frequency': 0.5,
                'amplitude_y': 3.0,
                'amplitude_x': 0.5,
                'amplitude_z': 0.3,
                'noise_level': 0.2
            },
            'pushup': {
                'frequency': 0.7,
                'amplitude_y': 1.5,
                'amplitude_x': 0.8,
                'amplitude_z': 2.5,
                'noise_level': 0.15
            },
            'bicep_curl': {  # ✅ Changé de 'curl' à 'bicep_curl'
                'frequency': 0.6,
                'amplitude_y': 2.0,
                'amplitude_x': 0.4,
                'amplitude_z': 1.2,
                'noise_level': 0.18
            },
            'bench_press': {  # ✅ Changé de 'bench' à 'bench_press'
                'frequency': 0.5,
                'amplitude_y': 0.8,
                'amplitude_x': 1.0,
                'amplitude_z': 3.0,
                'noise_level': 0.2
            },
            'deadlift': {
                'frequency': 0.4,
                'amplitude_y': 3.5,
                'amplitude_x': 0.4,
                'amplitude_z': 1.0,
                'noise_level': 0.22
            },
            # ✅ Exercices additionnels (optionnels)
            'jumping_jack': {
                'frequency': 1.2,
                'amplitude_y': 2.5,
                'amplitude_x': 3.0,
                'amplitude_z': 0.8,
                'noise_level': 0.25
            },
            'plank': {
                'frequency': 0.1,
                'amplitude_y': 0.2,
                'amplitude_x': 0.15,
                'amplitude_z': 0.1,
                'noise_level': 0.3
            }
        }
        
        # ✅ Mapping pour rétro-compatibilité
        self.legacy_names = {
            'curl': 'bicep_curl',
            'bench': 'bench_press',
            'ohp': 'shoulder_press',
            'row': 'bent_over_row',
            'lunge': 'forward_lunge'
        }
    
    def generate_signal(self, exercise, duration, intensity='medium', reps=None):
        """
        Génère un signal complet pour un exercice
        
        Args:
            exercise: Type d'exercice (accepte aussi anciens noms via mapping)
            duration: Durée en secondes
            intensity: 'light', 'medium', 'heavy'
            reps: Nombre de répétitions (calculé auto si None)
            
        Returns:
            DataFrame avec colonnes: time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z
        """
        
        # ✅ Mapper les anciens noms si nécessaire
        exercise = self.legacy_names.get(exercise, exercise)
        
        # Vérification
        if exercise not in self.exercise_patterns:
            available = list(self.exercise_patterns.keys())
            raise ValueError(
                f"❌ Exercice '{exercise}' non reconnu.\n"
                f"Exercices disponibles: {', '.join(available)}\n"
                f"Anciens noms acceptés: {', '.join(self.legacy_names.keys())}"
            )
        
        pattern = self.exercise_patterns[exercise]
        
        # Ajuster selon l'intensité
        intensity_multiplier = {
            'light': 0.7,
            'medium': 1.0,
            'heavy': 1.3
        }
        mult = intensity_multiplier.get(intensity, 1.0)
        
        # Calculer le nombre de points
        n_samples = int(duration * self.sampling_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Fréquence
        freq = pattern['frequency'] / mult
        
        # Générer accélération
        acc_y = (pattern['amplitude_y'] * mult * 
                 np.sin(2 * np.pi * freq * t))
        acc_x = (pattern['amplitude_x'] * mult * 
                 np.sin(2 * np.pi * freq * t + np.pi/4))
        acc_z = (pattern['amplitude_z'] * mult * 
                 np.sin(2 * np.pi * freq * t + np.pi/2))
        
        # Ajouter bruit
        noise_level = pattern['noise_level']
        acc_x += np.random.normal(0, noise_level, n_samples)
        acc_y += np.random.normal(0, noise_level, n_samples)
        acc_z += np.random.normal(0, noise_level, n_samples)
        
        # Générer gyroscope
        gyr_x = np.gradient(acc_x) * 10
        gyr_y = np.gradient(acc_y) * 10
        gyr_z = np.gradient(acc_z) * 10
        
        # Appliquer filtre passe-bas
        acc_x = self._apply_lowpass_filter(acc_x)
        acc_y = self._apply_lowpass_filter(acc_y)
        acc_z = self._apply_lowpass_filter(acc_z)
        gyr_x = self._apply_lowpass_filter(gyr_x)
        gyr_y = self._apply_lowpass_filter(gyr_y)
        gyr_z = self._apply_lowpass_filter(gyr_z)
        
        # Créer DataFrame
        df = pd.DataFrame({
            'time': t,
            'acc_x': acc_x,
            'acc_y': acc_y,
            'acc_z': acc_z,
            'gyr_x': gyr_x,
            'gyr_y': gyr_y,
            'gyr_z': gyr_z
        })
        
        return df
    
    def _apply_lowpass_filter(self, data, cutoff_freq=5):
        """Applique un filtre passe-bas"""
        nyquist = self.sampling_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(4, normal_cutoff, btype='low', analog=False)
        filtered_data = signal.filtfilt(b, a, data)
        return filtered_data
    
    def get_available_exercises(self):
        """Retourne la liste des exercices disponibles"""
        return list(self.exercise_patterns.keys())


# Test
if __name__ == "__main__":
    print("🧪 Test Signal Generator (Harmonisé)")
    print("=" * 70)
    
    gen = SignalGenerator()
    
    print("\n📋 Exercices disponibles:")
    for ex in gen.get_available_exercises():
        print(f"  ✅ {ex}")
    
    print("\n🔬 Test de génération:")
    
    # Test avec nouveaux noms
    for ex in ['squat', 'bicep_curl', 'bench_press']:
        signal = gen.generate_signal(ex, duration=5)
        print(f"  ✅ {ex}: {signal.shape}")
    
    # Test rétro-compatibilité
    print("\n🔄 Test rétro-compatibilité:")
    signal = gen.generate_signal('curl', duration=5)  # Ancien nom
    print(f"  ✅ 'curl' → bicep_curl: {signal.shape}")
    
    signal = gen.generate_signal('bench', duration=5)  # Ancien nom
    print(f"  ✅ 'bench' → bench_press: {signal.shape}")
    
    print("\n✅ Tous les tests passent!")