"""
Script d'initialisation de la base de données SmartCoach Pro
Lance ce script UNE FOIS avant d'utiliser l'application
"""
import sys
from pathlib import Path

# Ajouter le dossier racine au path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🚀 INITIALISATION DE LA BASE DE DONNÉES SMARTCOACH PRO")
print("=" * 70)

# 1. Importer la fonction d'initialisation
try:
    from backend.database import init_db
    print("\n✅ Modules backend chargés")
except ImportError as e:
    print(f"\n❌ Erreur d'import : {e}")
    print("\n💡 Assure-toi que tous les fichiers backend/ existent")
    sys.exit(1)

# 2. Créer toutes les tables
try:
    print("\n🔧 Création des tables...")
    init_db()
    print("✅ Tables créées avec succès !")
except Exception as e:
    print(f"\n❌ Erreur lors de la création des tables : {e}")
    sys.exit(1)

# 3. Ajouter les données de base (achievements et programmes)
try:
    from backend.database import get_db
    from backend.models import Achievement, TrainingProgram
    
    db = get_db()
    
    # Vérifier si les achievements existent déjà
    ach_count = db.query(Achievement).count()
    
    if ach_count == 0:
        print("\n📊 Ajout des achievements...")
        
        # Importer les achievements depuis gamification.py (si existe)
        try:
            from src.gamification import ACHIEVEMENTS_DATA
            
            for ach in ACHIEVEMENTS_DATA:
                achievement = Achievement(
                    name=ach['name'],
                    description=ach['description'],
                    xp_reward=ach['xp_reward'],
                    icon=ach['icon']
                )
                db.add(achievement)
            
            db.commit()
            print(f"✅ {len(ACHIEVEMENTS_DATA)} achievements ajoutés")
        except ImportError:
            print("⚠️  Fichier gamification.py non trouvé, skip achievements")
    else:
        print(f"\n⚠️  {ach_count} achievements déjà présents, skip...")
    
    # Vérifier si les programmes existent déjà
    prog_count = db.query(TrainingProgram).count()
    
    if prog_count == 0:
        print("\n📚 Ajout des programmes d'entraînement...")
        
        # Importer les programmes depuis workout_programs.py (si existe)
        try:
            from src.workout_programs import TRAINING_PROGRAMS
            
            for prog in TRAINING_PROGRAMS:
                program = TrainingProgram(
                    name=prog['name'],
                    description=prog['description'],
                    difficulty=prog['difficulty'],
                    duration_weeks=prog['duration_weeks']
                )
                db.add(program)
            
            db.commit()
            print(f"✅ {len(TRAINING_PROGRAMS)} programmes ajoutés")
        except ImportError:
            print("⚠️  Fichier workout_programs.py non trouvé, skip programmes")
    else:
        print(f"\n⚠️  {prog_count} programmes déjà présents, skip...")
    
    db.close()
    
except Exception as e:
    print(f"\n⚠️  Impossible d'ajouter les données de base : {e}")
    print("Les tables sont créées, tu pourras ajouter les données plus tard")

print("\n" + "=" * 70)
print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS !")
print("=" * 70)
print("\n💡 Tu peux maintenant lancer l'application :")
print("   streamlit run app.py")
print("\n📝 Note : Si tu as des erreurs, vérifie que tous les fichiers")
print("         backend/ et src/ sont bien présents dans ton projet")
print()