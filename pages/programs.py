"""
Programs Page - Professional & Organized
Modern design with filtering and better UX
"""

import streamlit as st
from src.workout_programs import get_all_programs, enroll_user_in_program, get_user_active_program
from src.design_system import COLORS


def get_difficulty_color(difficulty: str) -> str:
    """Get color based on difficulty level"""
    difficulty_colors = {
        'beginner': COLORS['success'],
        'intermediate': COLORS['warning'],
        'advanced': COLORS['danger'],
        'expert': COLORS['accent']
    }
    return difficulty_colors.get(difficulty.lower(), COLORS['info'])


def programs_page(background_b64=None):
    """Render the professional training programs page"""
    # Background is now set by main_app(), no need to set it here
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Training Programs
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            Structured programs to help you reach your fitness goals
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    programs = get_all_programs()
    active_program = get_user_active_program(st.session_state.user_id)
    
    # ==========================================
    # ACTIVE PROGRAM DISPLAY
    # ==========================================
    if active_program:
        st.markdown("### Currently Enrolled")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{active_program['program_name']}**")
        
        with col2:
            st.metric("Day", f"{active_program['current_day']}/{active_program['total_days']}")
        
        with col3:
            progress = (active_program['current_day'] / active_program['total_days']) * 100
            st.metric("Progress", f"{progress:.0f}%")
        
        st.progress(progress / 100)
        st.divider()
    else:
        st.info("Not currently enrolled in any program. Choose one below to get started!")
        st.divider()
    
    # ==========================================
    # FILTERS & SORTING
    # ==========================================
    st.markdown("### Available Programs")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        difficulty_filter = st.multiselect(
            "Filter by Difficulty",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            default=[],
            help="Select difficulty levels to filter programs"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Name", "Difficulty", "Duration"],
            help="Sort programs by selected criteria"
        )
    
    st.markdown("")
    
    # ==========================================
    # FILTER & SORT PROGRAMS
    # ==========================================
    if not programs:
        st.info("No programs available at this time.")
        return
    
    # Apply difficulty filter
    filtered_programs = programs
    if difficulty_filter:
        filtered_programs = [
            p for p in programs 
            if p['difficulty'].title() in difficulty_filter
        ]
    
    # Apply sorting
    if sort_by == "Name":
        filtered_programs = sorted(filtered_programs, key=lambda x: x['name'])
    elif sort_by == "Difficulty":
        difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        filtered_programs = sorted(
            filtered_programs,
            key=lambda x: difficulty_order.get(x['difficulty'].lower(), 5)
        )
    elif sort_by == "Duration":
        filtered_programs = sorted(filtered_programs, key=lambda x: x['duration_weeks'])
    
    # Show count
    st.caption(f"Showing {len(filtered_programs)} program(s)")
    st.markdown("")
    
    # ==========================================
    # PROGRAMS GRID
    # ==========================================
    if not filtered_programs:
        st.warning("No programs match your selected filters.")
        return
    
    for i in range(0, len(filtered_programs), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(filtered_programs):
                break
            
            program = filtered_programs[idx]
            
            with col:
                # Program Card Container
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    border-radius: 1rem;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                '>
                """, unsafe_allow_html=True)
                
                # Program header
                col_title, col_badge = st.columns([3, 1])
                
                with col_title:
                    st.markdown(f"### {program['name']}")
                
                with col_badge:
                    difficulty_color = get_difficulty_color(program['difficulty'])
                    st.markdown(f"""
                    <div style='text-align: right; margin-top: 0.5rem;'>
                        <span style='
                            display: inline-block;
                            background: {difficulty_color}30;
                            color: {difficulty_color};
                            padding: 0.4rem 1rem;
                            border-radius: 999px;
                            font-size: 0.75rem;
                            font-weight: 700;
                            text-transform: uppercase;
                            border: 1px solid {difficulty_color}50;
                        '>{program['difficulty']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Description
                st.markdown(f"<p style='color: rgba(255,255,255,0.7); margin: 1rem 0;'>{program['description']}</p>", unsafe_allow_html=True)
                
                # Details
                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.markdown(f"<p style='color: rgba(255,255,255,0.6);'>⏱️ <strong>{program['duration_weeks']} weeks</strong></p>", unsafe_allow_html=True)
                with detail_col2:
                    st.markdown(f"<p style='color: rgba(255,255,255,0.6);'>📊 <strong>{program['difficulty'].title()}</strong></p>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Enrollment button
                is_active = active_program and active_program['program_id'] == program['id']
                
                if is_active:
                    st.success(" Currently Enrolled")
                else:
                    if st.button(
                        "Enroll in Program",
                        key=f"enroll_{program['id']}",
                        use_container_width=True,
                        type="primary"
                    ):
                        enroll_user_in_program(st.session_state.user_id, program['id'])
                        st.success(f"Successfully enrolled in {program['name']}!")
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # INFORMATION SECTION
    # ==========================================
    st.markdown("###  About Training Programs")
    
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
        border-left: 4px solid #6366f1;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-top: 1rem;
    '>
        <p style='color: rgba(255,255,255,0.85); line-height: 1.8; margin: 0;'>
            Training programs provide structured workout plans to help you achieve specific fitness goals:
        </p>
        <br>
        <ul style='color: rgba(255,255,255,0.85); line-height: 2;'>
            <li><strong style='color: #10b981;'>Beginner</strong>: Perfect for those just starting their fitness journey</li>
            <li><strong style='color: #f59e0b;'>Intermediate</strong>: For those with some experience looking to level up</li>
            <li><strong style='color: #ef4444;'>Advanced</strong>: Challenging programs for experienced athletes</li>
            <li><strong style='color: #ec4899;'>Expert</strong>: Elite-level training for maximum performance</li>
        </ul>
        <br>
        <p style='color: rgba(255,255,255,0.7); margin: 0; font-style: italic;'>
            Each program guides you day-by-day with recommended exercises, target reps, and progressive difficulty.
        </p>
    </div>
    """, unsafe_allow_html=True)