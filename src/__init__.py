# -*- coding: utf-8 -*-
"""
SmartCoach Pro - Module Package
"""

# Anciens modules (votre app existante)
from .signal_generator import SignalGenerator
from .movement_analyzer import MovementAnalyzer
from .exercise_classifier import ExerciseClassifier
from .config import (
    ICONS,
    EXERCISES,
    PERFORMANCE_LEVELS,
    CHALLENGES,
    USER_GOALS,
    MOTIVATIONAL_QUOTES,
    DEFAULT_SETTINGS,
    THEME_COLORS
)

# NOUVEAUX modules ML (pour le pipeline)
try:
    from .improved_signal_generator import (
        ImprovedSignalGenerator, 
        UserProfile, 
        generate_complete_dataset
    )
    from .feature_extractor import AdvancedFeatureExtractor, prepare_ml_dataset
    from .model_trainer import MLModelTrainer, train_and_evaluate
    from .create_visualizations import create_all_visualizations
    
    __all_ml__ = [
        'ImprovedSignalGenerator',
        'UserProfile',
        'generate_complete_dataset',
        'AdvancedFeatureExtractor',
        'prepare_ml_dataset',
        'MLModelTrainer',
        'train_and_evaluate',
        'create_all_visualizations'
    ]
except ImportError:
    __all_ml__ = []

__all__ = [
    'SignalGenerator',
    'MovementAnalyzer',
    'ExerciseClassifier',
    'ICONS',
    'EXERCISES',
    'PERFORMANCE_LEVELS',
    'CHALLENGES',
    'USER_GOALS',
    'MOTIVATIONAL_QUOTES',
    'DEFAULT_SETTINGS',
    'THEME_COLORS'
] + __all_ml__

__version__ = '3.0.0'
__author__ = 'SmartCoach Pro Team'