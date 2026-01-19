"""
GÉNÉRATEUR DE SIGNAUX RÉALISTES - VERSION 7 EXERCICES
Compatible avec tout le pipeline ML
"""

import numpy as np
from scipy import signal
import pandas as pd
from dataclasses import dataclass


@dataclass
class UserProfile:
    """Profil utilisateur pour variabilité"""
    height: float  # cm
    weight: float  # kg
    fitness_level: str  # 'beginner', 'intermediate', 'advanced'
    age: int
    gender: str  # 'M', 'F'
    
    def get_strength_factor(self) -> float:
        base = 1.0
        if self.fitness_level == 'beginner':
            base *= 0.7
        elif self.fitness_level == 'advanced':
            base *= 1.3
        if self.gender == 'M':
            base *= 1.15
        return base
    
    def get_speed_factor(self) -> float:
        base = 1.0
        if self.fitness_level == 'beginner':
            base *= 0.8
        elif self.fitness_level == 'advanced':
            base *= 1.2
        if self.age > 50:
            base *= 0.9
        elif self.age < 25:
            base *= 1.1
        return base


class ImprovedSignalGenerator:
    """Générateur avec 7 exercices biomécaniquement réalistes"""
    
    # ✅ EXERCICES COMPLETS (7)
    # ✅ NOMS compatibles avec config.py
    EXERCISE_PARAMS = {
        'squat': {
            'frequency_range': (0.5, 1.2),
            'amplitude_acc_y': (-15, -5),
            'amplitude_acc_x': (-2, 2),
            'amplitude_acc_z': (-3, 3),
            'duration_range': (2.0, 4.0),
        },
        'pushup': {
            'frequency_range': (0.4, 1.0),
            'amplitude_acc_y': (-8, -2),
            'amplitude_acc_x': (-1, 1),
            'amplitude_acc_z': (-10, -3),
            'duration_range': (2.5, 4.5),
        },
        'curl': {
            'frequency_range': (0.6, 1.5),
            'amplitude_acc_y': (-6, 6),
            'amplitude_acc_x': (-3, 3),
            'amplitude_acc_z': (-8, 8),
            'duration_range': (1.5, 3.0),
        },
        'bench': {
            'frequency_range': (0.4, 1.0),
            'amplitude_acc_y': (-12, -4),
            'amplitude_acc_x': (-2, 2),
            'amplitude_acc_z': (-5, 5),
            'duration_range': (2.0, 4.0),
        },
        'deadlift': {
            'frequency_range': (0.3, 0.8),
            'amplitude_acc_y': (-18, -6),
            'amplitude_acc_x': (-3, 3),
            'amplitude_acc_z': (-4, 4),
            'duration_range': (3.0, 5.0),
        },
        'jumping_jack': {
            'frequency_range': (1.0, 2.0),
            'amplitude_acc_y': (-8, 8),
            'amplitude_acc_x': (-10, 10),
            'amplitude_acc_z': (-4, 4),
            'duration_range': (0.8, 1.5),
        },
        'plank': {
            'frequency_range': (0.1, 0.3),
            'amplitude_acc_y': (-1, 1),
            'amplitude_acc_x': (-0.5, 0.5),
            'amplitude_acc_z': (-0.5, 0.5),
            'duration_range': (5.0, 10.0),
        },
    }
    
    def __init__(self, sampling_rate: int = 50):
        self.fs = sampling_rate
        
    def generate_exercise_signal(
        self,
        exercise: str,
        duration: float,
        user_profile: UserProfile,
        reps: int = None,
        fatigue_factor: float = 0.0,
        form_quality: float = 1.0
    ) -> pd.DataFrame:
        """Génère signal réaliste"""
        
        if exercise not in self.EXERCISE_PARAMS:
            raise ValueError(f"Exercise {exercise} not supported. Available: {list(self.EXERCISE_PARAMS.keys())}")
        
        params = self.EXERCISE_PARAMS[exercise]
        n_samples = int(duration * self.fs)
        t = np.linspace(0, duration, n_samples)
        
        # Pour plank: 1 seule "rep" (statique)
        if exercise == 'plank':
            reps = 1
        elif reps is None:
            rep_duration = np.mean(params['duration_range'])
            reps = max(1, int(duration / rep_duration))
        
        # Initialiser signaux
        acc_x = np.zeros(n_samples)
        acc_y = np.zeros(n_samples)
        acc_z = np.zeros(n_samples)
        gyr_x = np.zeros(n_samples)
        gyr_y = np.zeros(n_samples)
        gyr_z = np.zeros(n_samples)
        
        # Facteurs utilisateur
        strength = user_profile.get_strength_factor()
        speed = user_profile.get_speed_factor()
        
        # Générer chaque répétition
        rep_duration = duration / reps
        samples_per_rep = int(rep_duration * self.fs)
        
        for rep in range(reps):
            start_idx = rep * samples_per_rep
            end_idx = min(start_idx + samples_per_rep, n_samples)
            rep_samples = end_idx - start_idx
            
            if rep_samples <= 0:
                break
            
            # Fatigue progressive (sauf pour plank)
            if exercise != 'plank':
                current_fatigue = fatigue_factor * (rep / max(reps - 1, 1))
                current_form = form_quality * (1 - 0.3 * current_fatigue)
            else:
                current_fatigue = 0
                current_form = form_quality
            
            # Pattern de répétition
            rep_signal = self._generate_single_rep(
                exercise, params, rep_samples,
                strength, speed, current_form
            )
            
            # Ajouter au signal
            acc_x[start_idx:end_idx] += rep_signal['acc_x']
            acc_y[start_idx:end_idx] += rep_signal['acc_y']
            acc_z[start_idx:end_idx] += rep_signal['acc_z']
            gyr_x[start_idx:end_idx] += rep_signal['gyr_x']
            gyr_y[start_idx:end_idx] += rep_signal['gyr_y']
            gyr_z[start_idx:end_idx] += rep_signal['gyr_z']
        
        # Ajouter gravité sur Y
        acc_y += -9.81
        
        # Bruit (très faible pour plank)
        noise_level = 0.1 if exercise == 'plank' else 0.5
        acc_x = self._add_noise(acc_x, noise_level)
        acc_y = self._add_noise(acc_y, noise_level)
        acc_z = self._add_noise(acc_z, noise_level)
        gyr_x = self._add_noise(gyr_x, noise_level * 0.2)
        gyr_y = self._add_noise(gyr_y, noise_level * 0.2)
        gyr_z = self._add_noise(gyr_z, noise_level * 0.2)
        
        # Filtrer
        acc_x = self._lowpass_filter(acc_x, 20)
        acc_y = self._lowpass_filter(acc_y, 20)
        acc_z = self._lowpass_filter(acc_z, 20)
        gyr_x = self._lowpass_filter(gyr_x, 20)
        gyr_y = self._lowpass_filter(gyr_y, 20)
        gyr_z = self._lowpass_filter(gyr_z, 20)
        
        # DataFrame
        df = pd.DataFrame({
            'acc_x': acc_x,
            'acc_y': acc_y,
            'acc_z': acc_z,
            'gyr_x': gyr_x,
            'gyr_y': gyr_y,
            'gyr_z': gyr_z,
            'timestamp': t
        })
        
        return df
    
    def _generate_single_rep(self, exercise, params, n_samples, 
                            strength, speed, form_quality):
        """Génère une répétition"""
        t = np.linspace(0, 1, n_samples)
        freq = np.random.uniform(*params['frequency_range']) * speed
        
        # Accélération Y
        amp_y_min, amp_y_max = params['amplitude_acc_y']
        amp_y = np.random.uniform(amp_y_min, amp_y_max) * strength
        acc_y = amp_y * np.sin(2 * np.pi * freq * t)
        
        # Mauvaise forme = mouvement saccadé
        if form_quality < 0.8 and exercise != 'plank':
            acc_y += amp_y * 0.2 * np.random.randn(n_samples) * (1 - form_quality)
        
        # Accélération X
        amp_x_min, amp_x_max = params['amplitude_acc_x']
        amp_x = np.random.uniform(amp_x_min, amp_x_max) * strength * 0.3
        
        # Jumping jack: mouvement latéral dominant
        if exercise == 'jumping_jack':
            acc_x = amp_x * 3.0 * np.sin(2 * np.pi * freq * t)
        else:
            acc_x = amp_x * np.sin(2 * np.pi * freq * t * 0.5 + np.pi/4)
        
        # Accélération Z
        amp_z_min, amp_z_max = params['amplitude_acc_z']
        amp_z = np.random.uniform(amp_z_min, amp_z_max) * strength * 0.4
        acc_z = amp_z * np.cos(2 * np.pi * freq * t)
        
        # Gyroscope
        gyr_amp = 0.05 if exercise == 'plank' else 0.3
        gyr_x = gyr_amp * np.sin(2 * np.pi * freq * t * 0.7)
        gyr_y = gyr_amp * 0.5 * np.cos(2 * np.pi * freq * t * 0.5)
        gyr_z = gyr_amp * 0.3 * np.sin(2 * np.pi * freq * t * 0.3)
        
        return {
            'acc_x': acc_x, 'acc_y': acc_y, 'acc_z': acc_z,
            'gyr_x': gyr_x, 'gyr_y': gyr_y, 'gyr_z': gyr_z
        }
    
    def _add_noise(self, signal_data: np.ndarray, noise_level: float):
        """Ajoute bruit gaussien"""
        gaussian = np.random.normal(0, noise_level, len(signal_data))
        quantization = np.random.uniform(-0.05, 0.05, len(signal_data))
        return signal_data + gaussian + quantization
    
    def _lowpass_filter(self, data: np.ndarray, cutoff: float):
        """Filtre passe-bas"""
        nyquist = self.fs / 2
        normalized_cutoff = cutoff / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, data)


def generate_complete_dataset(
    n_samples_per_exercise: int = 200,
    exercises: list = None,
    save_path: str = "data/realistic_dataset.pkl"
) -> pd.DataFrame:
    """Génère dataset complet avec 7 exercices"""
    
    if exercises is None:
        # ✅ NOMS compatibles avec config.py
        exercises = ['squat', 'pushup', 'curl', 'bench', 'deadlift', 'jumping_jack', 'plank']
    
    generator = ImprovedSignalGenerator(sampling_rate=50)
    
    # Profils utilisateurs variés
    user_profiles = [
        UserProfile(175, 70, 'beginner', 25, 'M'),
        UserProfile(165, 55, 'intermediate', 30, 'F'),
        UserProfile(180, 85, 'advanced', 28, 'M'),
        UserProfile(170, 65, 'intermediate', 35, 'F'),
        UserProfile(178, 78, 'beginner', 22, 'M'),
    ]
    
    all_data = []
    set_counter = 1
    
    print("🏋️ Génération du dataset réaliste (7 exercices)...")
    
    for exercise in exercises:
        print(f"  📊 {exercise.upper()}: ", end="")
        
        for i in range(n_samples_per_exercise):
            user = np.random.choice(user_profiles)
            duration = np.random.uniform(10, 20)
            reps = np.random.randint(5, 15) if exercise != 'plank' else 1
            fatigue = np.random.uniform(0, 0.5)
            form_quality = np.random.uniform(0.7, 1.0)
            
            df = generator.generate_exercise_signal(
                exercise=exercise,
                duration=duration,
                user_profile=user,
                reps=reps,
                fatigue_factor=fatigue,
                form_quality=form_quality
            )
            
            df['label'] = exercise
            df['set'] = set_counter
            df['participant'] = f"user_{user_profiles.index(user) + 1}"
            df['category'] = 'heavy' if form_quality > 0.85 else 'medium'
            
            all_data.append(df)
            set_counter += 1
            
            if (i + 1) % 50 == 0:
                print(f"{i + 1}...", end="", flush=True)
        
        print(" ✅")
    
    final_df = pd.concat(all_data, ignore_index=True)
    
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    final_df.to_pickle(save_path)
    
    print(f"\n✅ Dataset généré: {len(final_df)} échantillons")
    print(f"   Exercices: {exercises}")
    print(f"📁 Sauvegardé dans: {save_path}")
    
    return final_df


# TEST
if __name__ == "__main__":
    print("🧪 Test du générateur (7 exercices)...")
    
    # Test simple
    user = UserProfile(175, 70, 'intermediate', 25, 'M')
    gen = ImprovedSignalGenerator()
    
    for ex in ['squat', 'jumping_jack', 'plank']:
        df = gen.generate_exercise_signal(ex, 10, user)
        print(f"✅ {ex}: {df.shape}")
    
    # Générer dataset complet
    print("\n🔥 Génération dataset complet...")
    df_full = generate_complete_dataset(n_samples_per_exercise=200)