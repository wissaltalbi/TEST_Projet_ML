"""
SmartCoach - Application de coaching sportif intelligent
Phase 1 : Interface de base avec simulation
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Importer les modules
from src.signal_generator import SignalGenerator
from src.movement_analyzer import MovementAnalyzer
from src.feedback_engine import FeedbackEngine


# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================
st.set_page_config(
    page_title="SmartCoach Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CSS PERSONNALISÉ
# ============================================================================
st.markdown("""
<style>
    /* Titre principal */
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF4B4B, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Boutons personnalisés */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Cartes de métriques */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Animation de pulsation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# INITIALISATION SESSION STATE
# ============================================================================
if 'simulation_done' not in st.session_state:
    st.session_state.simulation_done = False
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None
if 'last_feedback' not in st.session_state:
    st.session_state.last_feedback = None


# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-title">🏋️ SmartCoach Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ton coach sportif virtuel intelligent 🤖</p>', unsafe_allow_html=True)


# ============================================================================
# SIDEBAR - PARAMÈTRES
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Paramètres de simulation")
    
    duration = st.slider(
        "⏱️ Durée de l'exercice (secondes)",
        min_value=5,
        max_value=20,
        value=10,
        help="Durée totale de la simulation"
    )
    
    sampling_rate = st.slider(
        "📊 Fréquence d'échantillonnage (Hz)",
        min_value=30,
        max_value=100,
        value=50,
        help="Plus élevé = plus précis mais plus lourd"
    )
    
    st.markdown("---")
    st.markdown("### 📚 À propos")
    st.info("""
    **SmartCoach Pro** utilise des algorithmes avancés pour :
    - ✅ Détecter automatiquement les exercices
    - ✅ Compter les répétitions
    - ✅ Analyser la qualité du mouvement
    - ✅ Fournir un feedback en temps réel
    """)


# ============================================================================
# ONGLET 1 : SIMULATION
# ============================================================================
st.markdown("## 🏋️ Simulation d'Exercice")

# Dictionnaire des exercices avec emojis
EXERCISES = {
    "squat": "🏋️ Squat",
    "pushup": "💪 Push-up",
    "curl": "🦾 Curl",
    "jumping_jack": "🤸 Jumping Jack",
    "plank": "🧘 Plank"
}

# Layout en colonnes
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Choisis ton exercice")
    selected_exercise = st.selectbox(
        "Type d'exercice :",
        list(EXERCISES.keys()),
        format_func=lambda x: EXERCISES[x],
        key="exercise_selector"
    )
    
    # Description de l'exercice
    exercise_descriptions = {
        "squat": "💡 Exercice pour les jambes et les fessiers",
        "pushup": "💡 Exercice pour les pectoraux et les triceps",
        "curl": "💡 Exercice pour les biceps",
        "jumping_jack": "💡 Exercice cardio complet",
        "plank": "💡 Exercice de gainage pour les abdominaux"
    }
    st.caption(exercise_descriptions[selected_exercise])

with col2:
    st.markdown("### 🎬 Action")
    start_button = st.button(
        "▶️ START SIMULATION",
        type="primary",
        use_container_width=True
    )


# ============================================================================
# ZONE DE SIMULATION
# ============================================================================
if start_button:
    # Animation de démarrage
    st.balloons()
    
    with st.spinner("🔄 Simulation en cours..."):
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Étape 1 : Génération du signal
        status_text.text("⚙️ Génération des signaux capteurs...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        gen = SignalGenerator(duration=duration, sampling_rate=sampling_rate)
        time_data, acc_x, acc_y, acc_z = gen.get_exercise_signal(selected_exercise)
        
        # Étape 2 : Analyse
        status_text.text("🔍 Analyse du mouvement...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        analyzer = MovementAnalyzer(time_data, acc_x, acc_y, acc_z)
        analysis = analyzer.get_full_analysis(selected_exercise)
        
        # Étape 3 : Génération du feedback
        status_text.text("💬 Génération du feedback...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        feedback_engine = FeedbackEngine()
        feedback = feedback_engine.generate_feedback(analysis)
        
        # Étape 4 : Finalisation
        status_text.text("✅ Finalisation...")
        progress_bar.progress(100)
        time.sleep(0.3)
        
        # Nettoyer
        progress_bar.empty()
        status_text.empty()
    
    st.success("✅ Simulation terminée avec succès !")
    
    # Sauvegarder dans session state
    st.session_state.simulation_done = True
    st.session_state.last_analysis = analysis
    st.session_state.last_feedback = feedback
    
    # ========================================================================
    # AFFICHAGE DES SIGNAUX
    # ========================================================================
    st.markdown("---")
    st.markdown("### 📈 Signaux capteurs en temps réel")
    
    # Créer le graphique
    fig = go.Figure()
    
    # Ajouter les traces
    fig.add_trace(go.Scatter(
        x=time_data,
        y=acc_x,
        mode='lines',
        name='Acc X',
        line=dict(color='#FF4B4B', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_data,
        y=acc_y,
        mode='lines',
        name='Acc Y',
        line=dict(color='#4BFF4B', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_data,
        y=acc_z,
        mode='lines',
        name='Acc Z',
        line=dict(color='#4B4BFF', width=2)
    ))
    
    # Configuration du layout
    fig.update_layout(
        title=f"Signaux - {EXERCISES[selected_exercise]}",
        xaxis_title="Temps (secondes)",
        yaxis_title="Accélération (m/s²)",
        height=450,
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # RÉSULTATS IMMÉDIATS
    # ========================================================================
    st.markdown("---")
    st.markdown("### 📊 Résultats de l'analyse")
    
    # Métriques en colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔄 Répétitions",
            value=analysis['repetitions'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="⏱️ Durée",
            value=f"{analysis['duration']}s",
            delta=None
        )
    
    with col3:
        st.metric(
            label="📊 Score",
            value=f"{analysis['score']}%",
            delta="Excellent" if analysis['score'] >= 80 else "Bien"
        )
    
    with col4:
        st.metric(
            label="🎯 Régularité",
            value=f"{analysis['regularity']}%",
            delta="Bon rythme" if analysis['regularity'] >= 70 else None
        )
    
    # ========================================================================
    # FEEDBACK
    # ========================================================================
    st.markdown("---")
    st.markdown("### 💬 Feedback du coach")
    
    # Message principal avec emoji
    st.info(f"{feedback['emoji']} **{feedback['overall']}**")
    
    # Messages détaillés
    for msg in feedback['messages']:
        st.write(f"• {msg}")
    
    # ========================================================================
    # SAUVEGARDE DANS CSV
    # ========================================================================
    # Créer le DataFrame pour cette session
    session_data = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'exercise': selected_exercise,
        'repetitions': analysis['repetitions'],
        'duration': analysis['duration'],
        'score': analysis['score'],
        'regularity': analysis['regularity'],
        'speed': analysis['speed'],
        'feedback': feedback['overall']
    }])
    
    # Charger l'historique existant et ajouter la nouvelle ligne
    try:
        existing_data = pd.read_csv('data/history.csv')
        updated_data = pd.concat([existing_data, session_data], ignore_index=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        updated_data = session_data
    
    # Sauvegarder
    updated_data.to_csv('data/history.csv', index=False)
    
    st.success("💾 Session sauvegardée dans l'historique !")


# ============================================================================
# AFFICHAGE DES DERNIERS RÉSULTATS (si disponibles)
# ============================================================================
if st.session_state.simulation_done and not start_button:
    st.markdown("---")
    st.markdown("### 📌 Dernière simulation")
    
    analysis = st.session_state.last_analysis
    feedback = st.session_state.last_feedback
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Répétitions", analysis['repetitions'])
    with col2:
        st.metric("Score", f"{analysis['score']}%")
    with col3:
        st.metric("Régularité", f"{analysis['regularity']}%")
    
    st.info(f"{feedback['emoji']} {feedback['overall']}")


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p style='font-size: 16px;'>
        🏋️ <strong>SmartCoach Pro</strong> - Ton coach virtuel intelligent
    </p>
    <p style='font-size: 14px;'>
        Développé avec ❤️ | Version 1.0 - Phase 1
    </p>
</div>
""", unsafe_allow_html=True)