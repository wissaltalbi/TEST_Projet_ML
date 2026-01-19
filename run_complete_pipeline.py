"""
SCRIPT PRINCIPAL - Lance TOUT automatiquement
"""

from datetime import datetime
import os

# Imports directs depuis src
from src.improved_signal_generator import generate_complete_dataset
from src.feature_extractor import prepare_ml_dataset
from src.model_trainer import train_and_evaluate
from src.create_visualizations import create_all_visualizations


def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}".center(80))
    print("="*80 + "\n")


def run_full_pipeline(n_samples=200):
    """LANCE LE PIPELINE COMPLET"""
    
    start_time = datetime.now()
    
    print_header("🚀 PIPELINE ML COMPLET - SMARTCOACH PRO")
    print(f"⏰ Démarrage: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Créer dossiers
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("reports/figures", exist_ok=True)
    
    try:
        # ÉTAPE 1: GÉNÉRER DATASET
        print_header("ÉTAPE 1/4: GÉNÉRATION DU DATASET")
        
        df_raw = generate_complete_dataset(
            n_samples_per_exercise=n_samples,
            exercises=['squat', 'pushup', 'curl', 'bench', 'deadlift'],
            save_path="data/realistic_dataset.pkl"
        )
        
        print(f"\n✅ Dataset généré: {df_raw.shape[0]} échantillons")
        
        # ÉTAPE 2: EXTRAIRE FEATURES
        print_header("ÉTAPE 2/4: EXTRACTION DES FEATURES")
        
        df_features = prepare_ml_dataset(
            raw_data_path="data/realistic_dataset.pkl",
            output_path="data/features_dataset.pkl"
        )
        
        print(f"\n✅ Features extraites: {df_features.shape[1]} colonnes")
        
        # ÉTAPE 3: ENTRAÎNER MODÈLES
        print_header("ÉTAPE 3/4: ENTRAÎNEMENT DES MODÈLES")
        
        trainer, report = train_and_evaluate(
            features_path="data/features_dataset.pkl",
            save_path="models/best_model.pkl"
        )
        
        print(f"\n✅ {len(trainer.models)} modèles entraînés")
        
        # ÉTAPE 4: VISUALISATIONS
        print_header("ÉTAPE 4/4: GÉNÉRATION DES VISUALISATIONS")
        
        create_all_visualizations(
            trainer=trainer,
            output_dir="reports/figures"
        )
        
        # RÉSUMÉ FINAL
        end_time = datetime.now()
        duration = end_time - start_time
        
        print_header("✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
        
        print(f"⏱️  Durée totale: {duration}")
        print(f"📊 Dataset: {df_raw.shape[0]} échantillons")
        print(f"🔢 Features: {df_features.shape[1]} colonnes")
        print(f"🏆 Meilleur: {trainer.best_model_name}")
        print(f"🎯 Accuracy: {trainer.results[trainer.best_model_name]['accuracy']:.4f}")
        
        print("\n📁 Fichiers générés:")
        print("  • data/realistic_dataset.pkl")
        print("  • data/features_dataset.pkl")
        print("  • models/best_model.pkl")
        print("  • reports/figures/confusion_matrix.png")
        print("  • reports/figures/model_comparison.png")
        print("  • reports/figures/feature_importance.png")
        print("  • reports/figures/classification_report.csv")
        
        print("\n" + "="*80)
        print("🎉 VOTRE PROJET ML EST MAINTENANT COMPLET!")
        print("="*80 + "\n")
        
        return {
            'trainer': trainer,
            'report': report,
            'duration': duration
        }
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n" + "🔥"*40)
    print("  LANCEMENT DU PIPELINE COMPLET".center(80))
    print("🔥"*40)
    
    # LANCER!
    results = run_full_pipeline(n_samples=200)
    
    if results:
        print("\n✅ SUCCÈS!")
        print("🎓 VOUS ÊTES PRÊT POUR VOTRE SOUTENANCE!")
    else:
        print("\n❌ Échec. Vérifiez les erreurs ci-dessus.")