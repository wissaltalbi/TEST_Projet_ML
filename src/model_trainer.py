"""
ÉTAPE 3: Entraînement et Comparaison de Modèles
Créer ce fichier: model_trainer.py
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix
)

# Modèles
from sklearn.ensemble import (
    RandomForestClassifier, 
    ExtraTreesClassifier, 
    GradientBoostingClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

import joblib
import warnings
warnings.filterwarnings('ignore')


class MLModelTrainer:
    """Entraîneur de modèles ML avec validation rigoureuse"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.best_model = None
        self.best_model_name = None
        
    def prepare_data(self, df: pd.DataFrame, test_size: float = 0.2):
        """Prépare les données"""
        print("📊 Préparation des données...")
        
        # Séparer features et labels
        feature_cols = [c for c in df.columns 
                       if c not in ['label', 'set', 'participant', 'category']]
        X = df[feature_cols].values
        y = df['label'].values
        
        # Encoder labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, 
            test_size=test_size, 
            random_state=self.random_state,
            stratify=y_encoded
        )
        
        # Normalisation
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"  ✅ Train: {X_train.shape}")
        print(f"  ✅ Test: {X_test.shape}")
        print(f"  ✅ Classes: {self.label_encoder.classes_}")
        
        self.X_train = X_train_scaled
        self.X_test = X_test_scaled
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = feature_cols
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def define_models(self):
        """Définit tous les modèles"""
        self.models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Extra Trees': ExtraTreesClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=self.random_state
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=15,
                random_state=self.random_state
            ),
            'KNN': KNeighborsClassifier(
                n_neighbors=5,
                n_jobs=-1
            ),
            'Naive Bayes': GaussianNB(),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=self.random_state
            ),
            'Neural Network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=self.random_state
            )
        }
        
        print(f"🤖 {len(self.models)} modèles définis")
        
    def train_all_models(self, cv_folds: int = 5):
        """Entraîne tous les modèles"""
        print("\n🏋️ Entraînement de tous les modèles...")
        print("=" * 70)
        
        for name, model in self.models.items():
            print(f"\n📍 {name}...")
            
            # Entraînement
            model.fit(self.X_train, self.y_train)
            
            # Prédictions
            y_pred = model.predict(self.X_test)
            
            # Métriques
            accuracy = accuracy_score(self.y_test, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(
                self.y_test, y_pred, average='weighted', zero_division=0
            )
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, self.X_train, self.y_train, 
                cv=cv_folds, scoring='accuracy', n_jobs=-1
            )
            
            # Stocker
            self.results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_pred': y_pred,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred)
            }
            
            print(f"  ✅ Accuracy: {accuracy:.4f}")
            print(f"  📊 CV: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
            print(f"  🎯 F1: {f1:.4f}")
        
        print("\n" + "=" * 70)
        print("✅ Tous les modèles entraînés!")
        
    def get_best_model(self):
        """Identifie le meilleur modèle"""
        best_acc = 0
        best_name = None
        
        for name, results in self.results.items():
            if results['accuracy'] > best_acc:
                best_acc = results['accuracy']
                best_name = name
        
        self.best_model_name = best_name
        self.best_model = self.results[best_name]['model']
        
        print(f"\n🏆 Meilleur: {best_name}")
        print(f"  Accuracy: {best_acc:.4f}")
        
        return self.best_model, best_name
    
    def generate_report(self) -> pd.DataFrame:
        """Génère rapport comparatif"""
        report_data = []
        
        for name, results in self.results.items():
            report_data.append({
                'Model': name,
                'Accuracy': f"{results['accuracy']:.4f}",
                'Precision': f"{results['precision']:.4f}",
                'Recall': f"{results['recall']:.4f}",
                'F1-Score': f"{results['f1_score']:.4f}",
                'CV Mean': f"{results['cv_mean']:.4f}",
                'CV Std': f"{results['cv_std']:.4f}"
            })
        
        df_report = pd.DataFrame(report_data)
        df_report = df_report.sort_values('Accuracy', ascending=False)
        
        return df_report
    
    def save_best_model(self, path: str = "models/best_model.pkl"):
        """Sauvegarde le meilleur modèle"""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'model_name': self.best_model_name,
            'accuracy': self.results[self.best_model_name]['accuracy']
        }
        
        joblib.dump(model_data, path)
        print(f"💾 Modèle sauvegardé: {path}")


def train_and_evaluate(
    features_path: str = "data/features_dataset.pkl",
    save_path: str = "models/best_model.pkl"
):
    """Pipeline complet d'entraînement"""
    print("\n" + "="*70)
    print("🚀 PIPELINE D'ENTRAÎNEMENT ML")
    print("="*70)
    
    # Charger
    print("\n1️⃣ Chargement...")
    df = pd.read_pickle(features_path)
    print(f"  Dataset: {df.shape}")
    
    # Trainer
    trainer = MLModelTrainer(random_state=42)
    
    # Préparer
    print("\n2️⃣ Préparation...")
    trainer.prepare_data(df, test_size=0.2)
    
    # Définir
    print("\n3️⃣ Définition...")
    trainer.define_models()
    
    # Entraîner
    print("\n4️⃣ Entraînement...")
    trainer.train_all_models(cv_folds=5)
    
    # Meilleur
    print("\n5️⃣ Sélection...")
    trainer.get_best_model()
    
    # Rapport
    print("\n6️⃣ Rapport...")
    report = trainer.generate_report()
    print("\n" + "="*70)
    print("📊 RAPPORT COMPARATIF")
    print("="*70)
    print(report.to_string(index=False))
    
    # Sauvegarder
    print("\n7️⃣ Sauvegarde...")
    trainer.save_best_model(save_path)
    
    print("\n" + "="*70)
    print("✅ PIPELINE TERMINÉ!")
    print("="*70)
    
    return trainer, report


# TEST
if __name__ == "__main__":
    print("Pour utiliser:")
    print("trainer, report = train_and_evaluate()")