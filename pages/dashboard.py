"""
Dashboard Page - Professional & Clean
Modern professional design without emojis
"""

import streamlit as st
from src.dashboard_helpers import get_dashboard_data


def dashboard_page(background_b64=None):
    """Render the professional dashboard page"""
    
    # Set background if provided
    if background_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{background_b64})'></div>""",
            unsafe_allow_html=True
        )
    
    # Get user
    user = st.session_state.user
    
    # Fetch all data optimized
    data = get_dashboard_data(user)
    stats = data['stats']
    lvl = data['level']
    achievements = data['achievements']
    active_program = data['active_program']
    
    # ==========================================
    # HERO SECTION - Clean Welcome
    # ==========================================
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Welcome back, {user.username}
        </h1>
        <p style='font-size: 1.1rem; color: rgba(255,255,255,0.6); font-weight: 600; letter-spacing: 1px;'>
            LEVEL {lvl['current_level']} • {lvl['title'].upper()}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # STATS OVERVIEW - Professional Cards
    # ==========================================
    st.markdown("### Performance Overview")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Experience Points",
            value=f"{lvl['xp_total']:,}",
            delta=f"{lvl['xp_to_next_level']} to next" if not lvl['is_max_level'] else "MAX LEVEL",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Total Workouts",
            value=str(stats.total_workouts),
            delta="Active" if stats.total_workouts > 0 else None
        )
    
    with col3:
        st.metric(
            label="Current Streak",
            value=f"{stats.current_streak} days",
            delta="Ongoing" if stats.current_streak > 0 else None
        )
    
    with col4:
        st.metric(
            label="Achievements Unlocked",
            value=f"{achievements['unlocked_count']}/{achievements['total']}",
            delta=f"{achievements['total'] - achievements['unlocked_count']} remaining"
        )
    
    st.divider()
    
    # ==========================================
    # PROGRESS SECTION
    # ==========================================
    if not lvl['is_max_level']:
        st.markdown("### Level Progression")
        
        xp_in_level = lvl['xp_in_level']
        xp_needed = lvl['xp_to_next_level'] + xp_in_level
        progress = xp_in_level / xp_needed if xp_needed > 0 else 0
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.progress(progress)
        with col2:
            st.caption(f"**{progress*100:.0f}%**")
        
        st.caption(f"{lvl['xp_to_next_level']} XP needed to reach Level {lvl['current_level'] + 1}")
        
        st.divider()
    
    # ==========================================
    # ACTIVE PROGRAM SECTION
    # ==========================================
    st.markdown("### Training Program")
    
    if active_program:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{active_program['program_name']}**")
            st.caption(f"Day {active_program['current_day']} of {active_program['total_days']}")
        
        with col2:
            progress_pct = (active_program['current_day'] / active_program['total_days']) * 100
            st.metric("Progress", f"{progress_pct:.0f}%")
        
        prog_col1, prog_col2 = st.columns([4, 1])
        with prog_col1:
            st.progress(active_program['current_day'] / active_program['total_days'])
        with prog_col2:
            st.caption(f"**{progress_pct:.0f}%**")
        
        st.divider()
    else:
        st.info("No active program. Browse available training programs to begin.")
        st.divider()
    
    # ==========================================
    # ACHIEVEMENTS PREVIEW
    # ==========================================
    if achievements['unlocked']:
        st.markdown(f"### Recent Achievements")
        
        # Show top 3 only
        top_achievements = achievements['unlocked'][:3]
        cols = st.columns(len(top_achievements))
        
        for i, ach in enumerate(top_achievements):
            with cols[i]:
                st.success(f"**{ach['name']}**")
                st.caption(f"+{ach['xp_reward']} XP")
        
        if achievements['unlocked_count'] > 3:
            st.caption(f"View all {achievements['unlocked_count']} achievements in the Achievements page →")
        
        st.divider()
    
    # ==========================================
    # QUICK ACTIONS - Professional Buttons
    # ==========================================
    st.markdown("### Quick Actions")
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start Workout", use_container_width=True, type="primary", key="start_workout"):
            st.session_state.page = 'workout'
            st.rerun()
    
    with col2:
        if st.button("Browse Programs", use_container_width=True, key="browse_programs"):
            st.session_state.page = 'programs'
            st.rerun() 
    
    with col3:
        if st.button("View History", use_container_width=True, key="view_history"):
            st.session_state.page = 'history'
            st.rerun()
