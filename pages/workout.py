"""
Workout Page - VERSION FINALE SIMPLIFIÉE
Design épuré : affiche seulement l'exercice détecté
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import re

# ✅ Modules existants
from src.movement_analyzer import MovementAnalyzer
from src.config import EXERCISES

# ✅ GÉNÉRATEURS
from src.signal_generator import SignalGenerator
from src.improved_signal_generator import ImprovedSignalGenerator, UserProfile

# ✅ Module ML
from src.ml_predictor import get_ml_predictor

# ✅ Backend
from backend.services.workout_service import create_workout
from backend.services.ai_coach_service import AICoach
from src.gamification import check_and_unlock_achievements


def get_exercise_name(exercise_key: str) -> str:
    """Retourne le nom d'affichage d'un exercice"""
    if exercise_key in EXERCISES:
        return EXERCISES[exercise_key]['name']
    else:
        return exercise_key.replace('_', ' ').title()


def workout_page(bg_image):
    """Page Workout avec design simplifié"""
    
    # ✅ RESET automatique
    if 'last_workout_page_visit' not in st.session_state:
        st.session_state.last_workout_page_visit = datetime.now()
        st.session_state.workout_started = False
        st.session_state.workout_completed = False
    else:
        if st.session_state.get('current_page_tracker') != 'workout':
            st.session_state.workout_started = False
            st.session_state.workout_completed = False
            st.session_state.workout_data = None
    
    st.session_state.current_page_tracker = 'workout'
    
    # Background
    if bg_image:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{bg_image})'></div>""",
            unsafe_allow_html=True
        )
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Start Workout
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            Track your exercise performance with AI-powered analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charger le prédicteur ML et coach
    predictor = get_ml_predictor()
    coach = AICoach()
    
    # ==========================================
    # EXERCISE SELECTION
    # ==========================================
    st.markdown("###  Exercise Selection")
    
    # Auto-detect checkbox
    auto_detect = st.checkbox(
        " Enable AI Auto-Detection",
        help="Automatically detect exercise type using machine learning"
    )
    
    # Dropdown et bouton alignés
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if not auto_detect:
            exercise_type = st.selectbox(
                "Choose Exercise",
                list(EXERCISES.keys()),
                format_func=lambda x: get_exercise_name(x),
                help="Select the exercise you want to perform"
            )
        else:
            st.info(" AI will automatically detect your exercise type")
    
    with col2:
        if st.button(" START", type="primary", key="start_workout_btn", use_container_width=True):
            st.session_state.workout_started = True
            st.rerun()
    
    st.divider()
    
    # ==========================================
    # WORKOUT SETTINGS
    # ==========================================
    with st.expander(" Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.slider(
                "Duration (seconds)",
                min_value=5,
                max_value=20,
                value=10,
                help="Workout duration for signal generation"
            )
        
        with col2:
            sampling_rate = st.slider(
                "Sampling Rate (Hz)",
                min_value=30,
                max_value=100,
                value=50,
                help="Signal sampling frequency (default: 50Hz)"
            )
    
    # ==========================================
    # WORKOUT EXECUTION
    # ==========================================
    if st.session_state.get('workout_started', False):
        with st.spinner(" Analyzing your workout..."):
            
            # ✅ CHOIX DU GÉNÉRATEUR
            if auto_detect:
                # Mode ML: Signal réaliste
                import random
                
                available_exercises = list(EXERCISES.keys())
                random_exercise = random.choice(available_exercises)
                
                # Générer signal réaliste
                generator = ImprovedSignalGenerator(sampling_rate=50)
                user = UserProfile(175, 70, 'intermediate', 25, 'M')
                
                signal_data_raw = generator.generate_exercise_signal(
                    exercise=random_exercise,
                    duration=duration,
                    user_profile=user,
                    reps=np.random.randint(5, 12),
                    fatigue_factor=np.random.uniform(0, 0.3),
                    form_quality=np.random.uniform(0.8, 1.0)
                )
                
                # Convertir en format attendu
                signal_data = pd.DataFrame({
                    'time': signal_data_raw['timestamp'],
                    'acc_x': signal_data_raw['acc_x'],
                    'acc_y': signal_data_raw['acc_y'],
                    'acc_z': signal_data_raw['acc_z'],
                    'gyr_x': signal_data_raw['gyr_x'],
                    'gyr_y': signal_data_raw['gyr_y'],
                    'gyr_z': signal_data_raw['gyr_z']
                })
                
                st.session_state.true_exercise = random_exercise
                
            else:
                # Mode Manuel: Signal simple
                generator = SignalGenerator(sampling_rate=sampling_rate)
                
                signal_data = generator.generate_signal(
                    exercise=exercise_type,
                    duration=duration,
                    intensity='medium'
                )
                
                st.session_state.true_exercise = exercise_type
            
            # ==========================================
            # PRÉDICTION ML (si mode auto)
            # ==========================================
            confidence = None
            if auto_detect and predictor.is_available():
                predicted_exercise, confidence, probabilities = predictor.predict(signal_data)
                predicted_name = get_exercise_name(predicted_exercise)
            else:
                predicted_exercise = exercise_type if not auto_detect else st.session_state.true_exercise
                predicted_name = get_exercise_name(predicted_exercise)
            
            # ✅ AFFICHAGE UNIQUE : Carte bleue simple
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(79, 70, 229, 0.1));
                padding: 2rem;
                border-radius: 0.75rem;
                border-left: 4px solid #6366f1;
                margin: 1rem 0;
                text-align: center;
            '>
                <div style='font-size: 2.5rem; font-weight: 700; color: #6366f1;'>
                    {predicted_name}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ==========================================
            # ANALYSE DU MOUVEMENT
            # ==========================================
            analyzer = MovementAnalyzer(
                time=signal_data['time'].values,
                acc_x=signal_data['acc_x'].values,
                acc_y=signal_data['acc_y'].values,
                acc_z=signal_data['acc_z'].values
            )
            
            analysis = analyzer.get_full_analysis(predicted_exercise)
            
            # ==========================================
            # FEEDBACK IA
            # ==========================================
            feedback = coach.generate_workout_feedback(
                predicted_exercise,
                analysis['score'],
                analysis['regularity'],
                analysis['speed'],
                analysis['repetitions']
            )
        
        st.divider()
        
        # ==========================================
        # RESULTS DISPLAY
        # ==========================================
        st.markdown("###  Workout Results")
        
        # Performance Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Repetitions", analysis['repetitions'])
        col2.metric("Duration", f"{analysis['duration']}s")
        col3.metric("Score", f"{analysis['score']:.1f}%")
        col4.metric("Regularity", f"{analysis['regularity']:.1f}%")
        
        st.divider()
        
        # ==========================================
        # SIGNAL VISUALIZATION
        # ==========================================
        st.markdown("###  Signal Data - 3 Axes")
        
        # Create interactive plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=signal_data['time'],
            y=signal_data['acc_x'],
            mode='lines',
            name='X Axis',
            line=dict(color='#6366f1', width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=signal_data['time'],
            y=signal_data['acc_y'],
            mode='lines',
            name='Y Axis',
            line=dict(color='#8b5cf6', width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=signal_data['time'],
            y=signal_data['acc_z'],
            mode='lines',
            name='Z Axis',
            line=dict(color='#ec4899', width=2.5)
        ))
        
        fig.update_layout(
            height=450,
            template='plotly_dark',
            hovermode='x unified',
            xaxis_title="Time (s)",
            yaxis_title="Acceleration (m/s²)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # ==========================================
        # AI FEEDBACK
        # ==========================================
        st.success(" Workout Completed Successfully!")
        
        # Nettoyer le feedback
        feedback_clean = feedback.replace('⚡', '•').replace('💡', '•').replace('📝', '•')
        feedback_clean = re.sub(r'[^\w\s\-.,!?:•%/()]+', '', feedback_clean)
        feedback_clean = feedback_clean.replace('•', '<br><br>•').lstrip('<br><br>')
        
        st.markdown("###  Coach Feedback")
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.1));
            padding: 1.5rem;
            border-radius: 0.75rem;
            border-left: 4px solid #8b5cf6;
        '>
            <div style='color: rgba(255,255,255,0.9); line-height: 1.8; font-size: 0.95rem;'>
                {feedback_clean}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ==========================================
        # SAVE WORKOUT
        # ==========================================
        if st.session_state.get('user_id'):
            try:
                workout = create_workout(
                    st.session_state.user_id,
                    predicted_exercise,
                    analysis['repetitions'],
                    analysis['duration'],
                    analysis['score'],
                    analysis['regularity'],
                    analysis['speed'],
                    feedback,
                    auto_detect,
                    confidence
                )
                
                # Vérifier achievements
                if workout:
                    newly_unlocked = check_and_unlock_achievements(st.session_state.user_id)
                    
                    if newly_unlocked:
                        st.balloons()
                        st.markdown("###  New Achievements Unlocked!")
                        for achievement in newly_unlocked:
                            st.success(f"**{achievement['name']}** - +{achievement['xp_reward']} XP")
                            st.caption(achievement['description'])
            except Exception as e:
                st.error(f"Error saving workout: {e}")
        
        st.divider()
        
        # Reset button
        if st.button(" Start Another Workout", type="primary", key="reset_workout", use_container_width=True):
            st.session_state.workout_started = False
            st.rerun()