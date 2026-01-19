"""Pages package - Modular page components for SmartCoach Pro"""

from .dashboard import dashboard_page
from .workout import workout_page
from .programs import programs_page
from .achievements import achievements_page
from .history import history_page

__all__ = [
    'dashboard_page',
    'workout_page',
    'programs_page',
    'achievements_page',
    'history_page',
    'simulation_page',
]
