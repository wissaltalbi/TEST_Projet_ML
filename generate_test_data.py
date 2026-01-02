"""
Script pour générer des données de test dans l'historique
Utilise ce script si tu veux avoir des données d'exemple
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Paramètres
NUM_SESSIONS = 30  # Nombre de sessions à générer
EXERCISES = ['squat', 'pushup', 'curl', 'jumping_jack', 'plank']

# Générer des données
data = []

for i in range(NUM_SESSIONS):
    # Date aléatoire dans les 30 derniers jours
    days_ago = random.randint(0, 30)
    timestamp = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
    
    # Exercice aléatoire
    exercise = random.choice(EXERCISES)
    
    # Paramètres selon l'exercice
    if exercise == 'squat':
        reps = random.randint(8, 15)
        duration = random.uniform(8, 12)
    elif exercise == 'pushup':
        reps = random.randint(10, 20)
        duration = random.uniform(10, 15)
    elif exercise == 'curl':
        reps = random.randint(10, 15)
        duration = random.uniform(8, 12)
    elif exercise == 'jumping_jack':
        reps = random.randint(15, 25)
        duration = random.uniform(10, 15)
    else:  # plank
        reps = 1
        duration = random.uniform(30, 60)
    
    # Score avec une progression réaliste
    base_score = 60 + (i * 0.5)  # Progression au fil du temps
    score = min(100, base_score + random.uniform(-10, 10))
    
    # Régularité corrélée au score
    regularity = score + random.uniform(-10, 5)
    regularity = max(50, min(100, regularity))
    
    # Vitesse
    speed = (reps / duration) * 60
    
    # Feedback selon le score
    if score >= 90:
        feedback = "Performance exceptionnelle !"
    elif score >= 75:
        feedback = "Très bonne séance !"
    elif score >= 60:
        feedback = "Bonne performance"
    else:
        feedback = "Performance moyenne"
    
    data.append({
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'exercise': exercise,
        'repetitions': int(reps),
        'duration': round(duration, 1),
        'score': round(score, 1),
        'regularity': round(regularity, 1),
        'speed': round(speed, 1),
        'feedback': feedback
    })

# Créer le DataFrame
df = pd.DataFrame(data)

# Trier par date
df = df.sort_values('timestamp')

# Sauvegarder
df.to_csv('data/history.csv', index=False)

print(f"✅ {NUM_SESSIONS} sessions de test générées !")
print(f"\nAperçu des données :")
print(df.head())
print(f"\nStatistiques :")
print(f"- Score moyen : {df['score'].mean():.1f}%")
print(f"- Nombre total de répétitions : {df['repetitions'].sum()}")
print(f"- Exercices : {df['exercise'].value_counts().to_dict()}")