"""
Farmer Advisory Agent — Streamlit Chat UI
Multilingual AI assistant for Indian farmers.
"""
import streamlit as st
import os
from agent.core import FarmerAgent
from utils.language import detect_language, SUPPORTED_LANGUAGES

# Page config
st.set_page_config(
    page_title="🌾 Krishi Mitra — Farmer Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage { padding: 0.5rem 1rem; }
    .stChatMessage[data-testid="stChatMessage-User"] { background-color: #e8f5e9; }
    .stChatMessage[data-testid="stChatMessage-Assistant"] { background-color: #fff8e1; }
    .main-header {
        background: linear-gradient(90deg, #2e7d32, #66bb6a);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .feature-card {
        background: #f1f8e9;
        border-left: 4px solid #4caf50;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .lang-badge {
        background: #e3f2fd;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state."""
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "language" not in st.session_state:
        st.session_state.language = "en"


def sidebar():
    """Sidebar with settings and info."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/wheat.png", width=64)
        st.title("🌾 Krishi Mitra")
        st.caption("Your AI farming companion")

        st.divider()

        # API Key input
        st.subheader("🔑 API Key")
        api_key = st.text_input(
            "OpenAI or Groq API Key",
            type="password",
            placeholder="sk-... or gsk_...",
            help="Get free Groq API key at console.groq.com",
        )

        provider = st.selectbox(
            "Provider",
            ["groq", "openai"],
            help="Groq is free and fast. OpenAI has better multilingual support.",
        )

        if api_key and st.session_state.agent is None:
            st.session_state.agent = FarmerAgent(api_key=api_key, provider=provider)
            st.success("✅ Agent ready!")
        elif api_key and st.session_state.agent:
            if st.button("🔄 Reset Agent"):
                st.session_state.agent = FarmerAgent(api_key=api_key, provider=provider)
                st.session_state.messages = []
                st.rerun()

        st.divider()

        # Language info
        st.subheader("🌐 Supported Languages")
        for code, name in SUPPORTED_LANGUAGES.items():
            st.markdown(f'<span class="lang-badge">{name}</span>', unsafe_allow_html=True)

        st.divider()

        # Quick actions
        st.subheader("⚡ Quick Questions")
        quick_qs = [
            "गेहूं की फसल में पीले धब्बे आ रहे हैं, क्या करूं?",
            "What is the best time to sow rice in Punjab?",
            "Tomato mein fal todne wala keeda lag gaya hai",
            "Kisan Credit Card kaise banwayen?",
            "What are the current onion prices?",
        ]
        for q in quick_qs:
            if st.button(q, use_container_width=True, key=f"q_{q[:20]}"):
                st.session_state.pending_message = q
                st.rerun()

        st.divider()
        st.caption("Built for GSSoC 2026 — Agents for India Track")
        st.caption("By [Nawang Dorjay](https://github.com/nawangdorjay)")


def main():
    init_session_state()
    sidebar()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌾 Krishi Mitra</h1>
        <p style="font-size:1.1rem; margin:0;">AI-Powered Farmer Advisory — Ask in any Indian language</p>
        <p style="font-size:0.9rem; margin:0.5rem 0 0 0; opacity:0.9;">
            Crop info • Weather advice • Pest management • Government schemes • Market prices
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards (shown when no messages)
    if not st.session_state.messages:
        cols = st.columns(3)
        features = [
            ("🌿 Crop Advisory", "Sowing times, varieties, fertilizer doses, irrigation schedules for rice, wheat, cotton, and more."),
            ("🐛 Pest & Disease", "Identify problems by symptoms. Get treatment recommendations with dosage and timing."),
            ("🏛️ Govt Schemes", "PM-KISAN, Fasal Bima, KCC, subsidies — eligibility, how to apply, benefits."),
            ("💰 Market Prices", "Current mandi prices across states. Know when and where to sell."),
            ("📅 Crop Calendar", "Region-specific sowing/harvest calendars for kharif and rabi seasons."),
            ("🌐 Multilingual", "Ask in Hindi, Tamil, Telugu, Bengali, Marathi, or any Indian language."),
        ]
        for i, (title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <b>{title}</b><br>
                    <span style="font-size:0.9rem; color:#555;">{desc}</span>
                </div>
                """, unsafe_allow_html=True)

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle pending message from sidebar quick questions
    prompt = None
    if "pending_message" in st.session_state:
        prompt = st.session_state.pending_message
        del st.session_state.pending_message

    # Chat input
    if not prompt:
        prompt = st.chat_input("फसल के बारे में पूछें... Ask about farming...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Check for API key
        if not st.session_state.agent:
            error_msg = "⚠️ Please enter your API key in the sidebar to start chatting."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.warning(error_msg)
            return

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("🌾 सोच रहा हूँ... Thinking..."):
                response = st.session_state.agent.process_query(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer
    st.divider()
    st.caption(
        "💡 **Tip:** Ask in your own language — Hindi, Tamil, Telugu, Bengali, Marathi, etc. "
        "The AI will respond in the same language."
    )


if __name__ == "__main__":
    main()
