"""
ÉTAPE 2: Extraction de Features Avancées
Créer ce fichier: feature_extractor.py
"""

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq


class AdvancedFeatureExtractor:
    """Extraction de 150+ features"""
    
    def __init__(self, sampling_rate: int = 50):
        self.fs = sampling_rate
        
    def extract_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrait toutes les features d'un DataFrame"""
        
        sensor_cols = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']
        
        # Vérifier colonnes
        for col in sensor_cols:
            if col not in df.columns:
                raise ValueError(f"Colonne {col} manquante")
        
        # Extraire features pour ce set
        features = self._extract_window_features(
            df[sensor_cols].values, 
            sensor_cols
        )
        
        # Ajouter métadonnées
        for meta_col in ['label', 'set', 'participant', 'category']:
            if meta_col in df.columns:
                features[meta_col] = df[meta_col].iloc[0]
        
        return pd.DataFrame([features])
    
    def _extract_window_features(self, window_data: np.ndarray, 
                                  col_names: list) -> dict:
        """Extrait features d'une fenêtre"""
        features = {}
        
        for i, col in enumerate(col_names):
            col_data = window_data[:, i]
            
            # 1. Temporelles
            temp = self._extract_temporal_features(col_data)
            for key, val in temp.items():
                features[f"{col}_{key}"] = val
            
            # 2. Fréquentielles
            freq = self._extract_frequency_features(col_data)
            for key, val in freq.items():
                features[f"{col}_{key}"] = val
            
            # 3. Statistiques
            stat = self._extract_statistical_features(col_data)
            for key, val in stat.items():
                features[f"{col}_{key}"] = val
        
        # 4. Inter-axes
        inter = self._extract_inter_axis_features(window_data)
        features.update(inter)
        
        return features
    
    def _extract_temporal_features(self, signal_data: np.ndarray) -> dict:
        """Features temporelles (10 features)"""
        return {
            'mean': np.mean(signal_data),
            'std': np.std(signal_data),
            'min': np.min(signal_data),
            'max': np.max(signal_data),
            'range': np.ptp(signal_data),
            'median': np.median(signal_data),
            'mad': np.mean(np.abs(signal_data - np.mean(signal_data))),
            'rms': np.sqrt(np.mean(signal_data**2)),
            'abs_energy': np.sum(signal_data**2),
            'abs_sum': np.sum(np.abs(signal_data)),
        }
    
    def _extract_frequency_features(self, signal_data: np.ndarray) -> dict:
        """Features fréquentielles (6 features)"""
        n = len(signal_data)
        fft_vals = fft(signal_data)
        fft_mag = np.abs(fft_vals[:n//2])
        freqs = fftfreq(n, 1/self.fs)[:n//2]
        
        power = fft_mag**2
        
        if len(fft_mag) > 0 and np.max(fft_mag) > 0:
            dominant_freq_idx = np.argmax(fft_mag[1:]) + 1
            dominant_freq = freqs[dominant_freq_idx] if dominant_freq_idx < len(freqs) else 0
        else:
            dominant_freq = 0
        
        spectral_energy = np.sum(power)
        
        if spectral_energy > 0:
            normalized_power = power / spectral_energy
            normalized_power = normalized_power[normalized_power > 0]
            spectral_entropy = -np.sum(normalized_power * np.log2(normalized_power))
        else:
            spectral_entropy = 0
        
        return {
            'dominant_freq': dominant_freq,
            'spectral_energy': spectral_energy,
            'spectral_entropy': spectral_entropy,
            'spectral_mean': np.mean(fft_mag),
            'spectral_std': np.std(fft_mag),
            'spectral_max': np.max(fft_mag),
        }
    
    def _extract_statistical_features(self, signal_data: np.ndarray) -> dict:
        """Features statistiques (7 features)"""
        return {
            'skewness': stats.skew(signal_data),
            'kurtosis': stats.kurtosis(signal_data),
            'q25': np.percentile(signal_data, 25),
            'q75': np.percentile(signal_data, 75),
            'iqr': np.percentile(signal_data, 75) - np.percentile(signal_data, 25),
            'zero_crossing': np.sum(np.diff(np.sign(signal_data)) != 0),
            'mean_crossing': np.sum(np.diff(np.sign(signal_data - np.mean(signal_data))) != 0),
        }
    
    def _extract_inter_axis_features(self, window_data: np.ndarray) -> dict:
        """Features inter-axes (9 features)"""
        features = {}
        
        if window_data.shape[1] >= 3:
            acc_mag = np.sqrt(
                window_data[:, 0]**2 + 
                window_data[:, 1]**2 + 
                window_data[:, 2]**2
            )
            features['acc_magnitude_mean'] = np.mean(acc_mag)
            features['acc_magnitude_std'] = np.std(acc_mag)
            features['acc_magnitude_max'] = np.max(acc_mag)
        
        if window_data.shape[1] >= 6:
            gyr_mag = np.sqrt(
                window_data[:, 3]**2 + 
                window_data[:, 4]**2 + 
                window_data[:, 5]**2
            )
            features['gyr_magnitude_mean'] = np.mean(gyr_mag)
            features['gyr_magnitude_std'] = np.std(gyr_mag)
            features['gyr_magnitude_max'] = np.max(gyr_mag)
        
        if window_data.shape[1] >= 3:
            features['corr_acc_xy'] = np.corrcoef(window_data[:, 0], window_data[:, 1])[0, 1]
            features['corr_acc_xz'] = np.corrcoef(window_data[:, 0], window_data[:, 2])[0, 1]
            features['corr_acc_yz'] = np.corrcoef(window_data[:, 1], window_data[:, 2])[0, 1]
        
        return features


def prepare_ml_dataset(
    raw_data_path: str,
    output_path: str = "data/features_dataset.pkl"
) -> pd.DataFrame:
    """Prépare dataset avec features pour ML"""
    
    print("🔧 Préparation du dataset ML...")
    
    # Charger données brutes
    print("  📂 Chargement des données brutes...")
    df_raw = pd.read_pickle(raw_data_path)
    
    # Initialiser extracteur
    extractor = AdvancedFeatureExtractor(sampling_rate=50)
    
    # Extraire features par set
    print("  🧮 Extraction des features...")
    all_features = []
    
    sets = df_raw['set'].unique()
    for i, set_id in enumerate(sets):
        if (i + 1) % 100 == 0:
            print(f"    {i + 1}/{len(sets)} sets...", flush=True)
        
        set_data = df_raw[df_raw['set'] == set_id]
        features_df = extractor.extract_all_features(set_data)
        all_features.append(features_df)
    
    # Combiner
    final_df = pd.concat(all_features, ignore_index=True)
    
    # Sauvegarder
    final_df.to_pickle(output_path)
    
    print(f"\n✅ Dataset ML préparé!")
    print(f"  📊 Shape: {final_df.shape}")
    print(f"  📁 Sauvegardé: {output_path}")
    
    # Compter features
    feature_cols = [c for c in final_df.columns 
                   if c not in ['label', 'set', 'participant', 'category']]
    print(f"  🔢 Features: {len(feature_cols)}")
    
    return final_df


# TEST
if __name__ == "__main__":
    print("🧪 Test Feature Extractor...")
    
    # Données test
    test_data = pd.DataFrame({
        'acc_x': np.random.randn(500),
        'acc_y': np.random.randn(500) - 9.81,
        'acc_z': np.random.randn(500),
        'gyr_x': np.random.randn(500) * 0.5,
        'gyr_y': np.random.randn(500) * 0.5,
        'gyr_z': np.random.randn(500) * 0.5,
        'label': 'squat',
        'set': 1
    })
    
    extractor = AdvancedFeatureExtractor()
    features = extractor.extract_all_features(test_data)
    
    print(f"✅ Features extraites: {features.shape[1]} colonnes")
    print("\nExemples:")
    feature_cols = [c for c in features.columns if c not in ['label', 'set']]
    for col in feature_cols[:10]:
        print(f"  • {col}: {features[col].values[0]:.4f}")