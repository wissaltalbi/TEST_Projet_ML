# -*- coding: utf-8 -*-
"""
SmartCoach Pro - Configuration et constantes
"""

# === ICÔNES RÉELLES (Unicode) ===
ICONS = {
    # Navigation
    'home': '🏠',
    'chart': '📊',
    'history': '📅',
    'settings': '⚙️',
    'profile': '👤',
    
    # Exercices  
    'squat': '🏋️',
    'pushup': '💪',
    'curl': '🦾',
    'jumping_jack': '🤸',
    'plank': '🧘',
    'workout': '🏃',
    
    # Actions
    'play': '▶️',
    'pause': '⏸️',
    'stop': '⏹️',
    'refresh': '🔄',
    'download': '📥',
    'upload': '📤',
    'save': '💾',
    'delete': '🗑️',
    'edit': '✏️',
    'check': '✅',
    'cross': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    
    # Stats & Performance
    'trophy': '🏆',
    'medal': '🥇',
    'star': '⭐',
    'fire': '🔥',
    'target': '🎯',
    'rocket': '🚀',
    'flash': '⚡',
    'diamond': '💎',
    
    # AI & Tech
    'robot': '🤖',
    'brain': '🧠',
    'magic': '✨',
    'crystal_ball': '🔮',
    'chart_up': '📈',
    'chart_down': '📉',
    
    # Time & Calendar
    'clock': '⏱️',
    'calendar': '📆',
    'timer': '⏲️',
    'hourglass': '⌛',
    
    # Emotions & Feedback
    'thumbs_up': '👍',
    'thumbs_down': '👎',
    'clap': '👏',
    'muscle': '💪',
    'heart': '❤️',
    'party': '🎉',
    'confetti': '🎊',
    'chat': '💬',
    'smile': '😊',
    'speech': '💭',
    
    # Nature & Elements  
    'sun': '☀️',
    'moon': '🌙',
    'lightning': '⚡',
    'water': '💧',
    
    # Misc
    'bell': '🔔',
    'lock': '🔒',
    'unlock': '🔓',
    'key': '🔑',
    'gift': '🎁',
    'flag': '🚩',
}

# === EXERCICES CONFIGURATION ===
EXERCISES = {
    'squat': {
        'name': 'Squat',
        'icon': ICONS['squat'],
        'description': 'Renforce les jambes, fessiers et bas du dos',
        'muscle_groups': ['Quadriceps', 'Fessiers', 'Ischio-jambiers'],
        'difficulty': 'Intermédiaire',
        'calories_per_rep': 0.4,
        'target_reps': (8, 15),
        'color': '#6366f1'
    },
    'pushup': {
        'name': 'Push-up',
        'icon': ICONS['pushup'],
        'description': 'Développe les pectoraux, triceps et épaules',
        'muscle_groups': ['Pectoraux', 'Triceps', 'Épaules'],
        'difficulty': 'Débutant',
        'calories_per_rep': 0.6,
        'target_reps': (10, 20),
        'color': '#8b5cf6'
    },
    'curl': {
        'name': 'Curl',
        'icon': ICONS['curl'],
        'description': 'Cible les biceps et avant-bras',
        'muscle_groups': ['Biceps', 'Avant-bras'],
        'difficulty': 'Débutant',
        'calories_per_rep': 0.3,
        'target_reps': (10, 15),
        'color': '#ec4899'
    },
    'jumping_jack': {
        'name': 'Jumping Jack',
        'icon': ICONS['jumping_jack'],
        'description': 'Exercice cardio complet pour l\'endurance',
        'muscle_groups': ['Full Body', 'Cardio'],
        'difficulty': 'Débutant',
        'calories_per_rep': 0.5,
        'target_reps': (15, 25),
        'color': '#10b981'
    },
    'plank': {
        'name': 'Plank',
        'icon': ICONS['plank'],
        'description': 'Gainage pour renforcer les abdominaux',
        'muscle_groups': ['Abdominaux', 'Core', 'Dos'],
        'difficulty': 'Intermédiaire',
        'calories_per_second': 0.1,
        'target_duration': (30, 60),
        'color': '#f59e0b'
    },
    'bench': {
        'name': 'Bench Press',
        'icon': '🏋️',
        'description': 'Développe les pectoraux, triceps et épaules',
        'muscle_groups': ['Pectoraux', 'Triceps', 'Épaules'],
        'difficulty': 'Intermédiaire',
        'calories_per_rep': 0.7,
        'target_reps': (8, 12),
        'color': '#f59e0b'
    },
    'deadlift': {
        'name': 'Deadlift',
        'icon': '💪',
        'description': 'Exercice complet pour le dos et les jambes',
        'muscle_groups': ['Dos', 'Ischio-jambiers', 'Fessiers'],
        'difficulty': 'Avancé',
        'calories_per_rep': 0.8,
        'target_reps': (5, 10),
        'color': '#ef4444'
    }
}

# === NIVEAUX DE PERFORMANCE ===
PERFORMANCE_LEVELS = {
    'legendary': {
        'min_score': 95,
        'name': 'Légendaire',
        'icon': '👑',
        'color': '#fbbf24',
        'message': 'Performance EXCEPTIONNELLE! Vous êtes au sommet!'
    },
    'excellent': {
        'min_score': 90,
        'name': 'Excellent',
        'icon': ICONS['trophy'],
        'color': '#10b981',
        'message': 'EXCELLENT! Continue comme ça!'
    },
    'very_good': {
        'min_score': 75,
        'name': 'Très Bien',
        'icon': ICONS['medal'],
        'color': '#8b5cf6',
        'message': 'Très bonne séance de coaching! Encore un effort!'
    },
    'good': {
        'min_score': 60,
        'name': 'Bien',
        'icon': ICONS['thumbs_up'],
        'color': '#3b82f6',
        'message': 'Bonne performance! Tu progresses!'
    },
    'average': {
        'min_score': 0,
        'name': 'À Améliorer',
        'icon': ICONS['flash'],
        'color': '#f59e0b',
        'message': 'Bon début! Continue à t\'entraîner!'
    }
}

# === CHALLENGES ===
CHALLENGES = [
    {
        'id': 'beginner_challenge',
        'name': 'Défi Débutant',
        'description': 'Complète 10 sessions de workout',
        'icon': ICONS['target'],
        'target': 10,
        'reward_points': 100,
        'badge': '🎖️'
    },
    {
        'id': 'streak_master',
        'name': 'Maître de la Régularité',
        'description': 'Entraîne-toi 7 jours consécutifs',
        'icon': ICONS['fire'],
        'target': 7,
        'reward_points': 200,
        'badge': '🔥'
    },
    {
        'id': 'perfect_score',
        'name': 'Perfectionniste',
        'description': 'Obtiens un score de 95%+',
        'icon': ICONS['star'],
        'target': 1,
        'reward_points': 150,
        'badge': '⭐'
    },
    {
        'id': 'variety_master',
        'name': 'Touche-à-Tout',
        'description': 'Essaie tous les 5 exercices',
        'icon': ICONS['diamond'],
        'target': 5,
        'reward_points': 250,
        'badge': '💎'
    },
    {
        'id': 'century_club',
        'name': 'Club des Centenaires',
        'description': 'Accumule 100 répétitions au total',
        'icon': ICONS['muscle'],
        'target': 100,
        'reward_points': 300,
        'badge': '💪'
    }
]

# === OBJECTIFS UTILISATEUR ===
USER_GOALS = {
    'weight_loss': {
        'name': 'Perte de Poids',
        'icon': '🎯',
        'color': '#ef4444',
        'recommended_exercises': ['jumping_jack', 'squat'],
        'sessions_per_week': 4
    },
    'muscle_gain': {
        'name': 'Prise de Masse',
        'icon': ICONS['muscle'],
        'color': '#8b5cf6',
        'recommended_exercises': ['pushup', 'squat', 'curl'],
        'sessions_per_week': 5
    },
    'endurance': {
        'name': 'Endurance',
        'icon': ICONS['rocket'],
        'color': '#10b981',
        'recommended_exercises': ['jumping_jack', 'plank'],
        'sessions_per_week': 4
    },
    'general_fitness': {
        'name': 'Forme Générale',
        'icon': ICONS['heart'],
        'color': '#ec4899',
        'recommended_exercises': list(EXERCISES.keys()),
        'sessions_per_week': 3
    }
}

# === CITATIONS MOTIVANTES ===
MOTIVATIONAL_QUOTES = [
    "💪 La différence entre essayer et réussir, c'est la persévérance!",
    "🏆 Ton seul limite, c'est toi!",
    "🚀 Chaque rep compte. Chaque session compte.",
    "⭐ Le succès commence par la décision d'essayer.",
    "🔥 Ton corps peut tout faire. C'est ton esprit qu'il faut convaincre!",
    "💎 Les champions s'entraînent, les légendes ne s'arrêtent jamais!",
    "✨ Crois en toi et tout devient possible!",
    "🎯 L'excellence n'est pas une destination, c'est un voyage!",
]

# === PARAMÈTRES PAR DÉFAUT ===
DEFAULT_SETTINGS = {
    'duration_range': (5, 20),
    'default_duration': 10,
    'sampling_rate_range': (30, 100),
    'default_sampling_rate': 50,
    'animation_speed': 0.04,
    'theme': 'dark',
    'language': 'fr',
    'notifications': True,
    'sound_effects': True
}

# === COULEURS THÈME ===
THEME_COLORS = {
    'primary': '#6366f1',
    'secondary': '#8b5cf6',
    'accent': '#ec4899',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'dark_bg': '#0f172a',
    'surface': '#1e293b',
    'card': '#334155'
}
