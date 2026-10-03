
import streamlit as st
import datetime
import requests
import uuid

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Rajat AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(59,130,246,0.10), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(139,92,246,0.10), transparent 25%),
            #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Hide Streamlit elements ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ---------- Hero Section ---------- */

    .hero {
        padding: 35px 35px 30px 35px;
        border-radius: 25px;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 45%,
            #7c3aed 100%
        );
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 15px 40px rgba(30, 64, 175, 0.20);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.88;
        line-height: 1.6;
        max-width: 750px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.20);
        padding: 7px 14px;
        border-radius: 50px;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* ---------- Feature Cards ---------- */

    .feature-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        min-height: 145px;
        box-shadow: 0 5px 18px rgba(15,23,42,0.05);
        transition: 0.2s;
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 5px;
    }

    .feature-text {
        font-size: 13px;
        color: #64748b;
        line-height: 1.5;
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #0f172a;
        margin-top: 28px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #64748b;
        margin-bottom: 20px;
    }

    /* ---------- Travel Plan ---------- */

    .plan-container {
        background: white;
        border-radius: 22px;
        padding: 30px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 30px rgba(15,23,42,0.06);
        margin-top: 25px;
    }

    .plan-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .plan-title {
        font-size: 27px;
        font-weight: 800;
        color: #0f172a;
    }

    .generated-time {
        font-size: 12px;
        color: #64748b;
        background: #f1f5f9;
        padding: 7px 12px;
        border-radius: 20px;
    }

    /* ---------- Chat messages ---------- */

    .user-message {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0 10px auto;
        max-width: 75%;
        box-shadow: 0 5px 15px rgba(37,99,235,0.15);
    }

    .assistant-message {
        background: white;
        color: #334155;
        padding: 18px 20px;
        border-radius: 18px 18px 18px 5px;
        border: 1px solid #e2e8f0;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(15,23,42,0.04);
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #172554);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .sidebar-brand {
        text-align: center;
        padding: 15px 5px 25px 5px;
    }

    .sidebar-logo {
        font-size: 48px;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 800;
    }

    .sidebar-text {
        font-size: 13px;
        opacity: 0.75;
        line-height: 1.5;
    }

    .sidebar-feature {
        padding: 12px 5px;
        font-size: 14px;
    }

    /* ---------- Input ---------- */

    div[data-testid="stTextInput"] input {
        border-radius: 14px;
        border: 1px solid #cbd5e1;
        padding: 14px;
        font-size: 15px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.15);
    }

    /* ---------- Button ---------- */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 13px;
        border: none;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        font-weight: 700;
        padding: 10px 25px;
        transition: 0.2s;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(79,70,229,0.25);
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())    

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🌍</div>
            <div class="sidebar-title">Rajat AI</div>
            <div class="sidebar-text">
                Your intelligent travel planning assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### ✨ What I can help with")

    st.markdown(
        """
        <div class="sidebar-feature">📍 Find attractions</div>
        <div class="sidebar-feature">🍽️ Discover restaurants</div>
        <div class="sidebar-feature">🎯 Plan activities</div>
        <div class="sidebar-feature">🚗 Explore transportation</div>
        <div class="sidebar-feature">💰 Calculate travel expenses</div>
        <div class="sidebar-feature">☀️ Check weather</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    st.caption("• Plan a 5-day trip to Goa")
    st.caption("• Best places to visit in Jaipur")
    st.caption("• Plan a budget trip to Manali")
    st.caption("• 3-day trip to Kerala")

    st.divider()

    st.caption("🤖 Powered by AI")
    st.caption("Built by Rajat")

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-Powered Travel Planner
        </div>

        <div class="hero-title">
            Plan your next adventure 🌏
        </div>

        <div class="hero-subtitle">
            Tell me where you want to go, and I'll help you discover
            attractions, restaurants, activities, transportation and
            estimated expenses — all in one place.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FEATURES
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📍</div>
            <div class="feature-title">Explore</div>
            <div class="feature-text">
                Discover interesting places and attractions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🍜</div>
            <div class="feature-title">Eat</div>
            <div class="feature-text">
                Find restaurants and local food experiences.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🗺️</div>
            <div class="feature-title">Plan</div>
            <div class="feature-text">
                Build a personalized travel itinerary.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Budget</div>
            <div class="feature-text">
                Estimate your trip and daily expenses.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CHAT HISTORY
# ============================================================

if st.session_state.messages:

    st.markdown(
        '<div class="section-title">💬 Your conversation</div>',
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="user-message">
                    <strong>👤 You</strong><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
                <div class="assistant-message">
                    <strong>🤖 Rajat AI Travel Agent</strong><br><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================
# INPUT
# ============================================================

st.markdown(
    """
    <div class="section-title">
        ✈️ Where are you going?
    </div>

    <div class="section-subtitle">
        Describe your dream trip and let AI create a plan for you.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form(key="query-form", clear_on_submit=True):

    user_input = st.text_input(
        "Travel request",
        placeholder="e.g. Plan a 5-day trip to Goa under ₹25,000...",
        label_visibility="collapsed",
    )

    submit_button = st.form_submit_button(
        "✨ Create My Travel Plan",
        use_container_width=True,
    )

# ============================================================
# API REQUEST
# ============================================================

if submit_button and user_input.strip():

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    try:

        with st.spinner("🌍 Exploring destinations and creating your itinerary..."):

            payload = {
                "session_id": st.session_state.session_id,
                "question": user_input
            }

            response = requests.post(
                f"{BASE_URL}/query",
                json=payload,
                timeout=120,
            )

        if response.status_code == 200:

            answer = response.json().get(
                "answer",
                "No travel plan was generated."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()

        else:

            st.error(
                f"❌ Bot failed to respond: {response.text}"
            )

    except requests.exceptions.Timeout:

        st.error(
            "⏳ The travel agent took too long to respond. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "🔌 Could not connect to the backend. "
            "Make sure FastAPI is running on port 8000."
        )

    except Exception as e:

        st.error(
            f"❌ Something went wrong: {str(e)}"
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🌍 <strong>Rajat AI Travel Planner</strong>
        <br><br>

        Your AI-powered companion for smarter travel planning.

        <br><br>

        ⚠️ AI-generated travel information should be verified
        before making bookings or important travel decisions.

    </div>
    """,
    unsafe_allow_html=True,
)
