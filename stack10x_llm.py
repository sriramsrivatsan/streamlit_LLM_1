import streamlit as st
from typing import Generator
from groq import Groq

# Page configuration with professional branding
st.set_page_config(
    page_title="Stack10x AI Chat | Groq-Powered Conversations",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #f8fafc;
        --accent-color: #10b981;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
        --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Global font styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Header styling */
    .main-header {
        background: var(--gradient-bg);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        border-radius: 0 0 20px 20px;
        box-shadow: var(--card-shadow);
    }

    .company-logo {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .company-tagline {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1rem;
        color: #fff;
    }

    /* Control panel styling */
    .control-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--card-shadow);
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }

    .control-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Chat container styling */
    .chat-container {
        background: white;
        border-radius: 12px;
        box-shadow: var(--card-shadow);
        padding: 1rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        max-height: 600px;
        overflow-y: auto;
    }

    /* Model info card */
    .model-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }

    .model-name {
        font-weight: 600;
        font-size: 1.1rem;
    }

    .model-details {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }

    .stat-card {
        flex: 1;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--border-color);
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
        margin-top: 2rem;
        background: white;
        border-radius: 12px;
    }

    /* Custom button styling */
    .stButton > button {
        background: var(--gradient-bg);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            margin: -1rem -1rem 1rem -1rem;
            padding: 1.5rem 0;
        }

        .company-logo {
            font-size: 2rem;
        }

        .app-title {
            font-size: 1.4rem;
        }

        .stats-container {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

# Professional header with branding
st.markdown("""
<div class="main-header">
    <div class="company-logo">🚀 Stack10x</div>
    <div class="company-tagline">Accelerating Innovation Through AI</div>
    <div class="app-title">⚡ Groq-Powered AI Chat</div>
</div>
""", unsafe_allow_html=True)

# Initialize Groq client
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "total_tokens_used" not in st.session_state:
    st.session_state.total_tokens_used = 0

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Enhanced model details with more information
models = {
    "gemma2-9b-it": {
        "name": "Gemma2-9B-IT",
        "tokens": 8192,
        "developer": "Google",
        "description": "Google's efficient instruction-tuned model",
        "speed": "⚡ Ultra Fast"
    },
    "llama-3.3-70b-versatile": {
        "name": "LLaMA3.3-70B-Versatile",
        "tokens": 128000,
        "developer": "Meta",
        "description": "Meta's most versatile large language model",
        "speed": "🔥 High Performance"
    },
    "llama-3.1-8b-instant": {
        "name": "LLaMA3.1-8B-Instant",
        "tokens": 128000,
        "developer": "Meta",
        "description": "Lightning-fast responses with great quality",
        "speed": "⚡ Instant"
    },
    "llama3-70b-8192": {
        "name": "LLaMA3-70B-8192",
        "tokens": 8192,
        "developer": "Meta",
        "description": "Powerful model for complex reasoning",
        "speed": "🚀 Fast"
    },
    "llama3-8b-8192": {
        "name": "LLaMA3-8B-8192",
        "tokens": 8192,
        "developer": "Meta",
        "description": "Balanced performance and efficiency",
        "speed": "⚡ Quick"
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7B-Instruct",
        "tokens": 32768,
        "developer": "Mistral",
        "description": "Expert mixture model for diverse tasks",
        "speed": "🔥 Optimized"
    },
}

# Control panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown('<div class="control-title">🎛️ Model Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    model_option = st.selectbox(
        "Choose your AI model:",
        options=list(models.keys()),
        format_func=lambda x: f"{models[x]['name']} ({models[x]['speed']})",
        index=1,  # Default to LLaMA3.3-70B
        help="Select the AI model that best fits your needs"
    )

# Display model information
selected_model_info = models[model_option]
st.markdown(f"""
<div class="model-info">
    <div class="model-name">{selected_model_info['name']}</div>
    <div class="model-details">
        {selected_model_info['description']} |
        Developer: {selected_model_info['developer']} |
        Max Tokens: {selected_model_info['tokens']:,}
    </div>
</div>
""", unsafe_allow_html=True)

# Detect model change and clear chat history
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option
    st.session_state.conversation_count = 0

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Response Length:",
        min_value=512,
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Control response length (max: {max_tokens_range:,} tokens)"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Statistics dashboard
st.markdown(f"""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.messages)//2}</div>
        <div class="stat-label">Messages Sent</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{st.session_state.total_tokens_used:,}</div>
        <div class="stat-label">Tokens Used</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{selected_model_info['developer']}</div>
        <div class="stat-label">Model Provider</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    if message["role"] == "assistant":
        avatar = '🤖'
        name = "Stack10x AI"
    else:
        avatar = '👤'
        name = "You"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Chat input with enhanced UX
if prompt := st.chat_input("💬 Ask me anything... (powered by Stack10x AI)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_count += 1

    with st.chat_message("user", avatar='👤'):
        st.markdown(prompt)

    # Fetch response from Groq API with error handling
    try:
        with st.spinner("🧠 Stack10x AI is thinking..."):
            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],
                max_tokens=max_tokens,
                stream=True
            )

            # Generate response with streaming
            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)

        # Update token usage (approximation)
        st.session_state.total_tokens_used += len(prompt.split()) + len(str(full_response).split())

    except Exception as e:
        st.error(f"⚠️ Error connecting to Stack10x AI: {str(e)}", icon="🚨")
        st.info("💡 Please check your API key and try again.", icon="💡")

    # Append response to chat history
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": combined_response}
        )

# Sidebar with additional features
with st.sidebar:
    st.markdown("### 🛠️ Stack10x Tools")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.total_tokens_used = 0
        st.session_state.conversation_count = 0
        st.rerun()

    st.markdown("### 📊 Session Stats")
    st.write(f"**Active Model:** {selected_model_info['name']}")
    st.write(f"**Messages:** {len(st.session_state.messages)}")
    st.write(f"**Est. Tokens:** {st.session_state.total_tokens_used:,}")

    st.markdown("### 🌟 About Stack10x")
    st.write("Stack10x accelerates innovation through cutting-edge AI solutions.")
    st.write("Visit [stack10x.com](https://stack10x.com) to learn more about our services.")

# Professional footer
st.markdown("""
<div class="footer">
    <p><strong>Powered by Stack10x AI Platform</strong></p>
    <p>🚀 Accelerating Innovation • 🤖 AI-First Solutions • 💡 Next-Gen Technology</p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        © 2024 Stack10x. Built with ❤️ using Streamlit & Groq
    </p>
</div>
""", unsafe_allow_html=True)
