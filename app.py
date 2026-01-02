"""
SmartCoach Pro - Application de coaching sportif intelligent
Phase 2 : Animation temps réel + Historique complet
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import numpy as np

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
# CSS PERSONNALISÉ AMÉLIORÉ
# ============================================================================
st.markdown("""
<style>
    /* Titre principal */
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF4B4B, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Cartes statistiques */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Boutons */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
    }
    
    .badge-excellent {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .badge-good {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .badge-normal {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    /* Animation de chargement */
    .loading {
        text-align: center;
        font-size: 24px;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
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
if 'history_loaded' not in st.session_state:
    st.session_state.history_loaded = False


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================
def load_history():
    """Charge l'historique depuis le CSV"""
    try:
        df = pd.read_csv('data/history.csv')
        if df.empty or len(df) == 0:
            return pd.DataFrame()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()


def get_performance_badge(score):
    """Retourne un badge HTML selon le score"""
    if score >= 90:
        return '<span class="badge badge-excellent">🔥 Excellent</span>'
    elif score >= 75:
        return '<span class="badge badge-good">💪 Très Bien</span>'
    else:
        return '<span class="badge badge-normal">👍 Bien</span>'


def animate_graph(time_data, acc_x, acc_y, acc_z, exercise_name, placeholder):
    """Anime le graphique en temps réel"""
    steps = 50  # Nombre d'étapes d'animation
    chunk_size = len(time_data) // steps
    
    for i in range(1, steps + 1):
        end_idx = min(i * chunk_size, len(time_data))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_data[:end_idx],
            y=acc_x[:end_idx],
            mode='lines',
            name='Acc X',
            line=dict(color='#FF4B4B', width=2.5)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_data[:end_idx],
            y=acc_y[:end_idx],
            mode='lines',
            name='Acc Y',
            line=dict(color='#4BFF4B', width=2.5)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_data[:end_idx],
            y=acc_z[:end_idx],
            mode='lines',
            name='Acc Z',
            line=dict(color='#4B4BFF', width=2.5)
        ))
        
        fig.update_layout(
            title=f"⚡ Simulation en direct - {exercise_name}",
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
        
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)


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
        help="Plus élevé = plus précis"
    )
    
    animate_enabled = st.checkbox(
        "🎬 Animation en temps réel",
        value=True,
        help="Active/désactive l'animation du graphique"
    )
    
    st.markdown("---")
    
    # Statistiques rapides
    history_df = load_history()
    if not history_df.empty:
        st.markdown("### 📊 Statistiques rapides")
        total_sessions = len(history_df)
        avg_score = history_df['score'].mean()
        
        st.metric("Sessions totales", total_sessions)
        st.metric("Score moyen", f"{avg_score:.1f}%")
    
    st.markdown("---")
    st.markdown("### 📚 À propos")
    st.info("""
    **SmartCoach Pro** v2.0
    
    ✅ Reconnaissance automatique
    ✅ Comptage précis
    ✅ Analyse de qualité
    ✅ Feedback intelligent
    ✅ Suivi des progrès
    """)


# ============================================================================
# ONGLETS PRINCIPAUX
# ============================================================================
tab1, tab2, tab3 = st.tabs(["🏋️ Simulation", "📊 Résultats", "📅 Historique"])


# ============================================================================
# ONGLET 1 : SIMULATION
# ============================================================================
with tab1:
    st.markdown("## 🎯 Simulation d'Exercice")
    
    # Dictionnaire des exercices
    EXERCISES = {
        "squat": "🏋️ Squat",
        "pushup": "💪 Push-up",
        "curl": "🦾 Curl",
        "jumping_jack": "🤸 Jumping Jack",
        "plank": "🧘 Plank"
    }
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_exercise = st.selectbox(
            "🎯 Choisis ton exercice :",
            list(EXERCISES.keys()),
            format_func=lambda x: EXERCISES[x],
            key="exercise_selector"
        )
        
        # Description
        descriptions = {
            "squat": "💡 Renforce les jambes, fessiers et bas du dos",
            "pushup": "💡 Développe les pectoraux, triceps et épaules",
            "curl": "💡 Cible les biceps et avant-bras",
            "jumping_jack": "💡 Exercice cardio complet pour l'endurance",
            "plank": "💡 Gainage pour renforcer les abdominaux"
        }
        st.caption(descriptions[selected_exercise])
    
    with col2:
        start_button = st.button(
            "▶️ START SIMULATION",
            type="primary",
            use_container_width=True,
            key="start_sim"
        )
    
    # ========================================================================
    # ZONE DE SIMULATION
    # ========================================================================
    if start_button:
        st.balloons()
        
        with st.spinner("🔄 Préparation de la simulation..."):
            # Génération
            gen = SignalGenerator(duration=duration, sampling_rate=sampling_rate)
            time_data, acc_x, acc_y, acc_z = gen.get_exercise_signal(selected_exercise)
        
        st.markdown("---")
        st.markdown("### 📈 Signaux capteurs")
        
        # Animation ou affichage direct
        graph_placeholder = st.empty()
        
        if animate_enabled:
            st.info("⚡ Animation en cours... (peut prendre quelques secondes)")
            animate_graph(time_data, acc_x, acc_y, acc_z, EXERCISES[selected_exercise], graph_placeholder)
        else:
            # Affichage direct sans animation
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=time_data, y=acc_x, mode='lines', 
                                    name='Acc X', line=dict(color='#FF4B4B', width=2.5)))
            fig.add_trace(go.Scatter(x=time_data, y=acc_y, mode='lines', 
                                    name='Acc Y', line=dict(color='#4BFF4B', width=2.5)))
            fig.add_trace(go.Scatter(x=time_data, y=acc_z, mode='lines', 
                                    name='Acc Z', line=dict(color='#4B4BFF', width=2.5)))
            
            fig.update_layout(
                title=f"Signaux - {EXERCISES[selected_exercise]}",
                xaxis_title="Temps (secondes)",
                yaxis_title="Accélération (m/s²)",
                height=450,
                hovermode='x unified',
                template='plotly_white'
            )
            
            graph_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Analyse
        with st.spinner("🔍 Analyse en cours..."):
            analyzer = MovementAnalyzer(time_data, acc_x, acc_y, acc_z)
            analysis = analyzer.get_full_analysis(selected_exercise)
            
            feedback_engine = FeedbackEngine()
            feedback = feedback_engine.generate_feedback(analysis)
        
        st.success("✅ Analyse terminée !")
        
        # Métriques
        st.markdown("---")
        st.markdown("### 📊 Résultats")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔄 Répétitions", analysis['repetitions'])
        with col2:
            st.metric("⏱️ Durée", f"{analysis['duration']}s")
        with col3:
            delta_text = "Excellent!" if analysis['score'] >= 80 else "Bien"
            st.metric("📊 Score", f"{analysis['score']}%", delta=delta_text)
        with col4:
            st.metric("🎯 Régularité", f"{analysis['regularity']}%")
        
        # Feedback
        st.markdown("---")
        st.markdown("### 💬 Feedback du Coach")
        
        st.info(f"{feedback['emoji']} **{feedback['overall']}**")
        
        for msg in feedback['messages']:
            st.write(f"• {msg}")
        
        # Badge de performance
        st.markdown(get_performance_badge(analysis['score']), unsafe_allow_html=True)
        
        # Sauvegarde
        st.session_state.simulation_done = True
        st.session_state.last_analysis = analysis
        st.session_state.last_feedback = feedback
        
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
        
        try:
            existing = pd.read_csv('data/history.csv')
            updated = pd.concat([existing, session_data], ignore_index=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            updated = session_data
        
        updated.to_csv('data/history.csv', index=False)
        st.success("💾 Session sauvegardée !")


# ============================================================================
# ONGLET 2 : RÉSULTATS DÉTAILLÉS
# ============================================================================
with tab2:
    st.markdown("## 📊 Analyse Détaillée")
    
    if st.session_state.simulation_done:
        analysis = st.session_state.last_analysis
        feedback = st.session_state.last_feedback
        
        # Section performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Performance Globale")
            
            # Jauge de score
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=analysis['score'],
                title={'text': "Score de Performance"},
                delta={'reference': 75},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Statistiques")
            
            stats_data = {
                'Métrique': ['Répétitions', 'Durée', 'Vitesse', 'Régularité', 'Amplitude'],
                'Valeur': [
                    f"{analysis['repetitions']} reps",
                    f"{analysis['duration']} s",
                    f"{analysis['speed']} rep/min",
                    f"{analysis['regularity']}%",
                    f"{analysis['amplitude']:.2f}"
                ]
            }
            
            df_stats = pd.DataFrame(stats_data)
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
            
            st.markdown("### 💬 Feedback")
            st.success(f"{feedback['emoji']} {feedback['overall']}")
            
            for msg in feedback['messages']:
                st.write(f"• {msg}")
    else:
        st.info("👋 Lance une simulation pour voir les résultats détaillés !")
        st.image("https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif", width=300)


# ============================================================================
# ONGLET 3 : HISTORIQUE COMPLET
# ============================================================================
with tab3:
    st.markdown("## 📅 Historique des Entraînements")
    
    history_df = load_history()
    
    if not history_df.empty:
        # Statistiques globales en cartes
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-label">🏆 SESSIONS</div>
                <div class="stats-number">{len(history_df)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_score = history_df['score'].mean()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-label">⭐ SCORE MOYEN</div>
                <div class="stats-number">{avg_score:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            best_score = history_df['score'].max()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-label">🔥 MEILLEUR</div>
                <div class="stats-number">{best_score:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_reps = history_df['repetitions'].sum()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-label">💪 TOTAL REPS</div>
                <div class="stats-number">{total_reps}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Graphique d'évolution
        st.markdown("### 📈 Évolution du Score")
        
        fig = px.line(
            history_df,
            x=history_df.index,
            y='score',
            color='exercise',
            markers=True,
            title="Progression dans le temps"
        )
        
        fig.update_layout(
            xaxis_title="Session #",
            yaxis_title="Score (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Graphique par exercice
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Répartition par Exercice")
            
            exercise_counts = history_df['exercise'].value_counts()
            fig = px.pie(
                values=exercise_counts.values,
                names=exercise_counts.index,
                title="Distribution des exercices"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Scores par Exercice")
            
            fig = px.box(
                history_df,
                x='exercise',
                y='score',
                color='exercise',
                title="Distribution des scores"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé
        st.markdown("---")
        st.markdown("### 📋 Détails des Sessions")
        
        # Filtre
        exercises_filter = st.multiselect(
            "Filtrer par exercice :",
            options=history_df['exercise'].unique(),
            default=history_df['exercise'].unique()
        )
        
        filtered_df = history_df[history_df['exercise'].isin(exercises_filter)]
        
        # Formatage
        display_df = filtered_df[['timestamp', 'exercise', 'repetitions', 
                                   'score', 'regularity', 'feedback']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            display_df.sort_values('timestamp', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Boutons d'export
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            csv = history_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Export CSV",
                csv,
                "smartcoach_history.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            if st.button("🗑️ Effacer historique", use_container_width=True):
                if st.session_state.get('confirm_delete', False):
                    # Réinitialiser le CSV
                    pd.DataFrame(columns=['timestamp', 'exercise', 'repetitions', 
                                         'duration', 'score', 'regularity', 
                                         'speed', 'feedback']).to_csv('data/history.csv', index=False)
                    st.success("✅ Historique effacé !")
                    st.session_state.confirm_delete = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.confirm_delete = True
                    st.warning("⚠️ Clique à nouveau pour confirmer")
    
    else:
        st.info("📭 Aucune session enregistrée pour le moment.")
        st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <p style='font-size: 64px;'>🏋️</p>
            <p style='font-size: 20px; color: gray;'>
                Lance ta première simulation pour commencer !
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p style='font-size: 18px; margin-bottom: 10px;'>
        🏋️ <strong>SmartCoach Pro</strong> - Version 2.0
    </p>
    <p style='font-size: 14px;'>
        Développé avec ❤️ | Phase 2 - Animation & Historique
    </p>
</div>
""", unsafe_allow_html=True)