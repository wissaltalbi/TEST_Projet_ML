# SmartCoach Pro - Professional Fitness Application
# Refactored with modular architecture and external CSS
# Updated: Login Page Redesign with Logo Card

import streamlit as st
import base64
from pathlib import Path
import logging

# Import pages
from pages import dashboard_page, workout_page, programs_page, achievements_page, history_page

# Import authentication
from backend.auth import login_user, register_user
from backend.session_manager import get_session_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="SmartCoach Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="auto",  # Auto-collapse on mobile
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "SmartCoach Pro - AI Fitness Tracking with ML"
    }
)

# PWA Meta Tags for Mobile Installation
st.markdown("""
<link rel="manifest" href="/app/static/manifest.json">
<meta name="theme-color" content="#6366f1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="SmartCoach">
<meta name="mobile-web-app-capable" content="yes">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes">
<meta name="description" content="Application de fitness intelligente avec détection automatique d'exercices par IA">
""", unsafe_allow_html=True)



@st.cache_data
def get_img_b64(path: str) -> str:
    """Load and encode image as base64 - Cached for performance"""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        logger.warning(f"Image file not found: {path}")
        return ""
    except Exception as e:
        logger.error(f"Error loading image {path}: {str(e)}")
        return ""


# Load background images
LOGIN_BG = get_img_b64('assets/login_bg_premium.png')
DASH_BG = get_img_b64('assets/dashboard_background_pro_1767472546043.png')
WORKOUT_BG = get_img_b64('assets/workout_background_pro_1767472562531.png')
ACH_BG = get_img_b64('assets/achievements_background_pro_1767472580234.png')
LOGO = get_img_b64('assets/logo.png')


def load_css_content():
    """Load external CSS file content - Fresh load every time for now"""
    css_file = Path("styles.css")
    if css_file.exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css = f.read()
            # CSS now has !important declarations to override Streamlit
            return css
        except Exception as e:
            logger.error(f"Error loading CSS file: {str(e)}")
            return get_fallback_css()
    else:
        logger.warning("CSS file not found, using fallback")
        return get_fallback_css()


def get_fallback_css():
    """Return fallback CSS if main file is not available"""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * {font-family: 'Inter', sans-serif;}
        #MainMenu, footer, header, .stDeployButton {display: none !important;}
        .main {background: #0a0e1a !important;}
    """


def load_css():
    """Inject CSS into page - called on every page load"""
    css_content = load_css_content()
    # Use a style tag with higher specificity
    st.markdown(f"""
    <style>
    {css_content}
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables with persistence check"""
    # Try to restore session from query params (simulating cookie)
    session_mgr = get_session_manager()
    
    # Check if we have a session token in query params
    query_params = st.query_params
    session_token = query_params.get('session', None)
    
    if session_token and 'user_id' not in st.session_state:
        # Try to restore session
        user = session_mgr.get_user_by_token(session_token)
        if user:
            st.session_state.user_id = user.id
            st.session_state.user = user
            logger.info(f"Session restored for user: {user.username}")
    
    # Initialize defaults for missing keys
    defaults = {
        'user_id': None,
        'user': None,
        'page': 'dashboard',
        'classifier': None,
        'workout_started': False,
        'session_token': session_token,
        'auth_mode': 'signin'  # 'signin' or 'signup'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_background(img_b64: str):
    """Set page background image - simple and stable approach"""
    if img_b64:
        st.markdown(
            f"""
            <style>
            /* Simple fixed background */
            .stApp {{
                background-image: url(data:image/png;base64,{img_b64}) !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            
            /* Dark overlay */
            .stApp > div:first-child {{
                background: linear-gradient(135deg, rgba(10, 14, 26, 0.85) 0%, rgba(26, 31, 53, 0.80) 100%) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


def login_page():
    """Render login page with unified card design using CSS"""
    set_background(LOGIN_BG)
    
    # Get current mode from session state
    auth_mode = st.session_state.get('auth_mode', 'signin')
    
    # Add custom CSS for unified login card
    st.markdown("""
    <style>
    /* Force main container to be visible */
    .main, .block-container {
        position: relative !important;
        z-index: 100 !important;
    }
    
    /* Unified Login Card */
    .block-container {
        padding-top: 3rem !important;
    }
    
    /* Target all columns to ensure visibility */
    div[data-testid="column"] {
        position: relative !important;
        z-index: 100 !important;
    }
    
    /* Create unified card wrapper */
    div[data-testid="column"]:nth-of-type(2) {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 1.5rem !important;
        padding: 3rem 3rem 2.5rem 3rem !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Remove form borders to blend in */
    div[data-testid="column"]:nth-of-type(2) [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Style buttons inside card */
    div[data-testid="column"]:nth-of-type(2) .stButton > button {
        margin-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and header
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2.5rem;'>
            <img src='data:image/png;base64,{LOGO}' style='
                max-width: 200px;
                height: auto;
                margin-bottom: 1.5rem;
            ' />
            <h2 style='
                font-size: 2rem;
                font-weight: 700;
                color: #ffffff;
                margin: 0 0 0.5rem 0;
            '>{'Welcome Back' if auth_mode == 'signin' else 'Create Account'}</h2>
            <p style='
                color: rgba(255,255,255,0.6);
                font-size: 1rem;
                margin: 0;
            '>{'Sign in to continue your fitness journey' if auth_mode == 'signin' else 'Join SmartCoach Pro and start training smarter'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sign In Form
        if auth_mode == 'signin':
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input(
                    "Username or Email",
                    placeholder="Enter your username or email",
                    key="login_username",
                    label_visibility="collapsed"
                )
                
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password",
                    label_visibility="collapsed"
                )
                
                st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if username and password:
                        success, message, user = login_user(username, password)
                        if success:
                            session_mgr = get_session_manager()
                            token = session_mgr.create_session(user.id)
                            
                            st.session_state.update({
                                'user_id': user.id,
                                'user': user,
                                'page': 'dashboard',
                                'session_token': token
                            })
                            
                            st.query_params['session'] = token
                            st.success("Login successful! Welcome back!")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please enter both username and password")
            
            # Switch to Sign Up
            st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='text-align: center;'>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-bottom: 1rem;'>
                    Don't have an account?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Create Account", use_container_width=True, key="switch_to_signup"):
                st.session_state.auth_mode = 'signup'
                st.rerun()
            
            # Footer
            st.markdown("""
            <div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);'>
                <p style='color: rgba(255,255,255,0.4); font-size: 0.85rem; margin: 0;'>
                    Powered by Advanced AI Technology
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sign Up Form
        else:
            with st.form("register_form", clear_on_submit=False):
                new_username = st.text_input(
                    "Username",
                    placeholder="Choose a unique username",
                    key="register_username",
                    label_visibility="collapsed"
                )
                
                new_email = st.text_input(
                    "Email",
                    placeholder="your.email@example.com",
                    key="register_email",
                    label_visibility="collapsed"
                )
                
                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password (min. 8 characters)",
                    key="register_password",
                    label_visibility="collapsed"
                )
                
                # Password strength indicator
                if new_password:
                    from backend.security import check_password_strength
                    strength_score, description = check_password_strength(new_password)
                    colors = {
                        0: "#ef4444", 1: "#f59e0b", 2: "#eab308", 
                        3: "#22c55e", 4: "#10b981"
                    }
                    color = colors.get(strength_score, "#ef4444")
                    width = (strength_score + 1) * 20
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 999px; overflow: hidden; margin-bottom: 0.5rem;">
                            <div style="width: {width}%; height: 100%; background: {color}; transition: all 0.3s ease; border-radius: 999px;"></div>
                        </div>
                        <div style="font-size: 0.75rem; color: {color}; font-weight: 600;">
                            {description}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                    key="register_confirm",
                    label_visibility="collapsed"
                )
                
                st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button(
                    "Create Account",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match!")
                        else:
                            success, message, _ = register_user(new_username, new_email, new_password)
                            if success:
                                st.success(f"{message}")
                                st.info("Please sign in with your credentials")
                                import time
                                time.sleep(2)
                                st.session_state.auth_mode = 'signin'
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.warning("Please fill in all fields")
            
            # Switch to Sign In
            st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='text-align: center;'>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-bottom: 1rem;'>
                    Already have an account?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Sign In", use_container_width=True, key="switch_to_signin"):
                st.session_state.auth_mode = 'signin'
                st.rerun()
            
            # Footer
            st.markdown("""
            <div style='text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);'>
                <p style='color: rgba(255,255,255,0.4); font-size: 0.85rem; margin: 0;'>
                    Powered by Advanced AI Technology
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_sidebar():
    """Render modern navigation sidebar"""
    with st.sidebar:
        # Modern App Header
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2rem 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
            border-radius: 1rem;
            border: 1px solid rgba(99, 102, 241, 0.2);
        '>
            <h1 style='
                font-size: 1.8rem;
                font-weight: 900;
                margin: 0;
                background: linear-gradient(135deg, #ffffff, #6366f1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            '>SmartCoach Pro</h1>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem'>
                AI-Powered Fitness
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Navigation items - clean text only
        pages = [
            ('dashboard', 'Dashboard'),
            ('workout', 'Workout'),
            ('programs', 'Programs'),
            ('achievements', 'Achievements'),
            ('history', 'History')
        ]
        
        current_page = st.session_state.get('page', 'dashboard')
        
        for page_key, page_label in pages:
            # Highlight current page
            is_active = current_page == page_key
            if is_active:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(90deg, rgba(99, 102, 241, 0.3), transparent);
                    border-left: 3px solid #6366f1;
                    padding: 0.75rem 1rem;
                    margin-bottom: 0.5rem;
                    border-radius: 0 0.5rem 0.5rem 0;
                '>
                    <span style='color: #ffffff; font-weight: 600'>{page_label}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(page_label, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()
        
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # User section
        st.markdown(f"""
        <div style='
            text-align: center;
            padding: 1.5rem 1rem;
            background: rgba(255,255,255,0.05);
            border-radius: 1rem;
            margin-top: 1rem;
        '>
            <div style='
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 50%;
                margin: 0 auto 0.75rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
            '>U</div>
            <p style='color: #f1f5f9; font-weight: 600; margin: 0'>{st.session_state.user.username}</p>
            <p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-top: 0.25rem'>Member</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        
        if st.button("Logout", key="logout_btn", use_container_width=True):
            # Revoke session token if exists
            if 'session_token' in st.session_state and st.session_state.session_token:
                session_mgr = get_session_manager()
                session_mgr.revoke_session(st.session_state.session_token)
            
            # Clear ALL session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Clear query params (removes session token from URL)
            st.query_params.clear()
            
            # Rerun will now show login page because user_id is None
            st.rerun()


def main_app():
    """Main application with navigation"""
    render_sidebar()
    
    # Route to appropriate page with backgrounds
    page = st.session_state.get('page', 'dashboard')
    
    if page == 'dashboard':
        set_background(DASH_BG)
        dashboard_page(DASH_BG)
    elif page == 'workout':
        set_background(WORKOUT_BG)
        workout_page(WORKOUT_BG)
    elif page == 'programs':
        set_background(DASH_BG)
        programs_page(DASH_BG)
    elif page == 'achievements':
        set_background(ACH_BG)
        achievements_page(ACH_BG)
    elif page == 'history':
        set_background(DASH_BG)
        history_page(DASH_BG)
    else:
        # Default to dashboard
        set_background(DASH_BG)
        dashboard_page(DASH_BG)


def main():
    """Application entry point"""
    # Load external CSS
    load_css()
    
    # Initialize session state
    init_session_state()
    
    # 🆕 CRITICAL: Initialize database on first run (for Streamlit Cloud)
    try:
        from backend.database import init_db, engine, Base
        from backend import models
        from sqlalchemy import inspect
        
        # Check if tables exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables or 'users' not in existing_tables:
            logger.info("🔄 Database tables not found, initializing...")
            init_db()
            logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"⚠️ Database initialization error: {e}")
        # Continue anyway, will show error on first use
    
    # Initialize predefined programs (only runs once if DB is empty)
    try:
        from src.workout_programs import init_predefined_programs
        logger.info("Attempting to initialize programs...")
        init_predefined_programs()
        logger.info("Program initialization completed")
    except Exception as e:
        logger.error(f"Error initializing programs: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Initialize achievements (only runs once if DB is empty)
    try:
        from src.gamification import init_achievements
        logger.info("Attempting to initialize achievements...")
        init_achievements()
        logger.info("Achievements initialization completed")
    except Exception as e:
        logger.error(f"Error initializing achievements: {e}")
    
    # Route based on authentication status
    if st.session_state.user_id is None:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()