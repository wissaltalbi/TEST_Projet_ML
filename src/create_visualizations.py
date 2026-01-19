"""
ÉTAPE 4: Création des Visualisations
Créer ce fichier: create_visualizations.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
import os


def create_all_visualizations(trainer, output_dir='reports/figures'):
    """Génère toutes les visualisations pour le rapport"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n📊 Génération des visualisations...")
    print("="*70)
    
    # Style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    results = trainer.results
    best_name = trainer.best_model_name
    best_results = results[best_name]
    exercise_names = trainer.label_encoder.classes_
    
    # 1. MATRICE DE CONFUSION
    print("\n1️⃣ Matrice de confusion...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cm = best_results['confusion_matrix']
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=exercise_names,
        yticklabels=exercise_names,
        cbar_kws={'label': 'Nombre'},
        ax=ax
    )
    
    ax.set_xlabel('Prédictions', fontsize=12, fontweight='bold')
    ax.set_ylabel('Vraies Valeurs', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Matrice de Confusion - {best_name}\n' +
        f'Accuracy: {best_results["accuracy"]:.2%}',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print(f"  💾 confusion_matrix.png")
    plt.close()
    
    # 2. COMPARAISON DES MODÈLES
    print("\n2️⃣ Comparaison des modèles...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    models = list(results.keys())
    accuracies = [results[m]['accuracy'] for m in models]
    cv_means = [results[m]['cv_mean'] for m in models]
    
    # Graphique 1: Test vs CV
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, accuracies, width, label='Test', alpha=0.8)
    bars2 = ax1.bar(x + width/2, cv_means, width, label='CV', alpha=0.8)
    
    ax1.set_xlabel('Modèles', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax1.set_title('Comparaison Test vs CV', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Valeurs sur barres
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=8
            )
    
    # Graphique 2: Métriques du meilleur
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    metrics_values = [
        best_results['accuracy'],
        best_results['precision'],
        best_results['recall'],
        best_results['f1_score']
    ]
    
    bars = ax2.barh(metrics_names, metrics_values, color='skyblue', alpha=0.8)
    ax2.set_xlabel('Score', fontsize=12, fontweight='bold')
    ax2.set_title(f'Métriques - {best_name}', fontsize=14, fontweight='bold')
    ax2.set_xlim([0, 1])
    ax2.grid(axis='x', alpha=0.3)
    
    for i, (bar, val) in enumerate(zip(bars, metrics_values)):
        ax2.text(
            val + 0.01, i, f'{val:.4f}',
            va='center', fontsize=10, fontweight='bold'
        )
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_comparison.png', dpi=300, bbox_inches='tight')
    print(f"  💾 model_comparison.png")
    plt.close()
    
    # 3. FEATURE IMPORTANCE (si Random Forest)
    if hasattr(best_results['model'], 'feature_importances_'):
        print("\n3️⃣ Feature importance...")
        
        importances = best_results['model'].feature_importances_
        feature_names = trainer.feature_names
        
        # Top 20
        indices = np.argsort(importances)[::-1][:20]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        y_pos = np.arange(len(indices))
        ax.barh(y_pos, importances[indices], align='center', alpha=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([feature_names[i] for i in indices])
        ax.invert_yaxis()
        ax.set_xlabel('Importance', fontsize=12, fontweight='bold')
        ax.set_title(
            f'Top 20 Features - {best_name}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/feature_importance.png', dpi=300, bbox_inches='tight')
        print(f"  💾 feature_importance.png")
        plt.close()
    
    # 4. RAPPORT CLASSIFICATION
    print("\n4️⃣ Rapport de classification...")
    
    report = classification_report(
        trainer.y_test,
        best_results['y_pred'],
        target_names=exercise_names,
        output_dict=True
    )
    
    df_report = pd.DataFrame(report).transpose()
    df_report.to_csv(f'{output_dir}/classification_report.csv')
    print(f"  💾 classification_report.csv")
    
    print("\n" + "="*70)
    print(f"✅ Visualisations créées dans: {output_dir}")
    print("="*70)


# Pour utiliser:
if __name__ == "__main__":
    print("Pour utiliser:")
    print("from model_trainer import train_and_evaluate")
    print("trainer, _ = train_and_evaluate()")
    print("create_all_visualizations(trainer)")