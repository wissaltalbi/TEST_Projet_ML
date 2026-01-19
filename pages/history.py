"""
History Page - Professional & Organized
Clean design with comprehensive workout statistics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from backend.services.workout_service import get_user_workouts, get_workout_stats
from src.design_system import COLORS


def set_background(img_b64):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


def clean_exercise_name(exercise_name):
    """Clean exercise name - standardize naming"""
    if not exercise_name:
        return "Unknown"
    
    # Convert to lowercase for comparison
    name_lower = exercise_name.lower().replace('_', ' ').strip()
    
    # Map variations to standard names
    exercise_map = {
        'bicep curl': 'Curl',
        'bicep_curl': 'Curl',
        'curl': 'Curl',
        'bench press': 'Bench Press',
        'bench_press': 'Bench Press',
        'bench': 'Bench Press',
        'jumping jack': 'Jumping Jack',
        'jumping_jack': 'Jumping Jack',
        'squat': 'Squat',
        'pushup': 'Pushup',
        'push up': 'Pushup',
        'plank': 'Plank',
        'deadlift': 'Deadlift',
        'dead lift': 'Deadlift'
    }
    
    return exercise_map.get(name_lower, exercise_name.replace('_', ' ').title())


def history_page(background_b64=None):
    """Render the professional workout history page"""
    set_background(background_b64)
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Workout History
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            View your progress and track your performance over time
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user workouts
    workouts = get_user_workouts(st.session_state.user_id, limit=50)
    
    if not workouts:
        st.info("No workout history yet. Start training to build your history!")
        if st.button("Start Workout", use_container_width=True, type="primary"):
            st.session_state.page = 'workout'
            st.rerun()
        return
    
    # Convert to DataFrame with cleaned exercise names
    df = pd.DataFrame([{
        'Date': workout.timestamp.strftime('%Y-%m-%d %H:%M'),
        'Exercise': clean_exercise_name(workout.exercise),
        'Reps': workout.repetitions,
        'Score': workout.score,
        'Duration': workout.duration,
        'Timestamp': workout.timestamp
    } for workout in workouts])
    
    # Get statistics  
    stats = get_workout_stats(st.session_state.user_id, days=30)
    
    # ==========================================
    # STATISTICS SUMMARY
    # ==========================================
    st.markdown("### 30-Day Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Workouts", stats['total_workouts'])
    col2.metric("Average Score", f"{stats['average_score']:.1f}%")
    col3.metric("Best Score", f"{stats['best_score']:.0f}%" if stats['best_score'] else "N/A")
    
    favorite = clean_exercise_name(stats['favorite_exercise']) if stats['favorite_exercise'] else "N/A"
    col4.metric("Favorite Exercise", favorite)
    
    st.divider()
    
    # ==========================================
    # PERFORMANCE EVOLUTION
    # ==========================================
    st.markdown("### Performance Evolution")
    
    fig = go.Figure()
    
    # Add score line
    fig.add_trace(go.Scatter(
        x=df['Timestamp'],
        y=df['Score'],
        mode='lines+markers',
        name='Score',
        line=dict(color=COLORS['primary'], width=4),
        marker=dict(size=10, color=COLORS['accent'], line=dict(width=2, color='white'))
    ))
    
    # Add trend line
    if len(df) >= 5:
        df['MA5'] = df['Score'].rolling(window=5).mean()
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['MA5'],
            mode='lines',
            name='Trend (5-workout MA)',
            line=dict(color=COLORS['success'], width=2, dash='dash'),
            opacity=0.7
        ))
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        xaxis_title="Date",
        yaxis_title="Score (%)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ==========================================
    # DISTRIBUTIONS
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Exercise Distribution")
        exercise_counts = df['Exercise'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=exercise_counts.index,
            values=exercise_counts.values,
            hole=0.4,
            marker=dict(colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
                       COLORS['success'], COLORS['info']])
        )])
        
        fig_pie.update_layout(template='plotly_dark', height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### Score Distribution")
        
        fig_hist = go.Figure(data=[go.Histogram(
            x=df['Score'],
            nbinsx=10,
            marker=dict(color=COLORS['primary'], line=dict(color='white', width=1))
        )])
        
        fig_hist.update_layout(
            template='plotly_dark',
            height=300,
            xaxis_title="Score (%)",
            yaxis_title="Count",
            showlegend=False
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.divider()
    
    # ==========================================
    # DETAILED TABLE
    # ==========================================
    st.markdown("### Workout Details")
    
    # Prepare display dataframe
    display_df = df[['Date', 'Exercise', 'Reps', 'Score', 'Duration']].copy()
    display_df['Score'] = display_df['Score'].apply(lambda x: f"{x:.1f}%")
    display_df['Duration'] = display_df['Duration'].apply(lambda x: f"{x}s")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
    
    # ==========================================
    # EXPORT BUTTONS
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=" Export to CSV",
            data=csv_data,
            file_name=f"smartcoach_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Generate PDF report with charts - imports at module level for faster load
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER
        from io import BytesIO
        import plotly.io as pio
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=rl_colors.HexColor('#6366f1'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Title
        title = Paragraph("SmartCoach - Workout History Report", title_style)
        elements.append(title)
        
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=rl_colors.grey,
            alignment=TA_CENTER
        )
        date_text = Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", date_style)
        elements.append(date_text)
        elements.append(Spacer(1, 30))
        
        # Statistics as simple table (original style)
        stats_header = Paragraph("<b>30-Day Statistics</b>", styles['Heading2'])
        elements.append(stats_header)
        elements.append(Spacer(1, 12))
        
        stats_data = [
            ['Metric', 'Value'],
            ['Total Workouts', str(stats['total_workouts'])],
            ['Average Score', f"{stats['average_score']:.1f}%"],
            ['Best Score', f"{stats['best_score']:.0f}%" if stats['best_score'] else "N/A"],
            ['Favorite Exercise', favorite]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), rl_colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, rl_colors.HexColor('#d1d5db')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 30))
        
        # Performance chart - COLORFUL
        try:
            perf_fig = go.Figure()
            
            # Main score line with gradient colors
            perf_fig.add_trace(go.Scatter(
                x=df['Timestamp'],
                y=df['Score'],
                mode='lines+markers',
                name='Score',
                line=dict(color='#6366f1', width=3),
                marker=dict(
                    size=10,
                    color=df['Score'],
                    colorscale='Viridis',
                    showscale=False,
                    line=dict(width=2, color='white')
                )
            ))
            
            # Add trend line if enough data
            if len(df) >= 5:
                df_trend = df.copy()
                df_trend['MA5'] = df_trend['Score'].rolling(window=5).mean()
                perf_fig.add_trace(go.Scatter(
                    x=df_trend['Timestamp'],
                    y=df_trend['MA5'],
                    mode='lines',
                    name='Trend',
                    line=dict(color='#10b981', width=2, dash='dash')
                ))
            
            perf_fig.update_layout(
                title=dict(text='Performance Evolution', font=dict(size=16, color='#1f2937')),
                xaxis=dict(title="Date", showgrid=True, gridcolor='#e5e7eb'),
                yaxis=dict(title="Score (%)", showgrid=True, gridcolor='#e5e7eb'),
                height=350,
                margin=dict(l=60, r=40, t=60, b=60),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#1f2937', size=11),
                showlegend=True,
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
            )
            
            # Save to image with higher quality
            img_bytes = pio.to_image(perf_fig, format='png', width=800, height=400, scale=2)
            img_buffer = BytesIO(img_bytes)
            elements.append(Image(img_buffer, width=6.5*inch, height=3.25*inch))
            elements.append(Spacer(1, 20))
        except Exception as e:
            error_para = Paragraph(f"<i>Performance chart unavailable</i>", styles['Normal'])
            elements.append(error_para)
            elements.append(Spacer(1, 20))
        
        # Exercise distribution chart - COLORFUL PIE CHART
        try:
            exercise_counts = df['Exercise'].value_counts()
            
            # Define vibrant colors for each exercise
            colors_list = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#14b8a6']
            
            pie_fig = go.Figure(data=[go.Pie(
                labels=exercise_counts.index,
                values=exercise_counts.values,
                hole=0.3,
                marker=dict(
                    colors=colors_list[:len(exercise_counts)],
                    line=dict(color='white', width=2)
                ),
                textposition='auto',
                textinfo='label+percent',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
            )])
            
            pie_fig.update_layout(
                title=dict(text='Exercise Distribution', font=dict(size=16, color='#1f2937')),
                height=350,
                margin=dict(l=40, r=40, t=60, b=40),
                paper_bgcolor='white',
                font=dict(color='#1f2937', size=11),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    bgcolor='rgba(255,255,255,0.8)'
                )
            )
            
            img_bytes = pio.to_image(pie_fig, format='png', width=800, height=400, scale=2)
            img_buffer = BytesIO(img_bytes)
            elements.append(Image(img_buffer, width=6.5*inch, height=3.25*inch))
            elements.append(Spacer(1, 30))
        except Exception as e:
            error_para = Paragraph(f"<i>Exercise distribution chart unavailable</i>", styles['Normal'])
            elements.append(error_para)
            elements.append(Spacer(1, 30))
        
        # Page break before table
        elements.append(PageBreak())
        
        # Section title for workout details
        details_title = Paragraph("<b>Workout Details</b>", styles['Heading2'])
        elements.append(details_title)
        elements.append(Spacer(1, 12))
        
        # Workout table with cleaned exercise names
        table_data = [['Date', 'Exercise', 'Reps', 'Score', 'Duration']]
        for _, row in display_df.iterrows():
            table_data.append([
                row['Date'],
                row['Exercise'],  # Already cleaned
                str(row['Reps']),
                row['Score'],
                row['Duration']
            ])
        
        # Adjust column widths to prevent truncation
        table = Table(table_data, colWidths=[1.8*inch, 1.5*inch, 0.8*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), rl_colors.HexColor('#f9fafb')),
            ('GRID', (0, 0), (-1, -1), 0.5, rl_colors.HexColor('#d1d5db')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [rl_colors.white, rl_colors.HexColor('#f9fafb')])
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Direct download button - PDF downloads when clicked
        st.download_button(
            label=" Export to PDF",
            data=pdf_data,
            file_name=f"smartcoach_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )