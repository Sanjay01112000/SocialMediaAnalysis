import streamlit as st
from dotenv import load_dotenv
import requests
import os

# Custom CSS
st.markdown("""
<style>
    .navbar {
        padding: 1rem;
        background-color: #1a5d1a;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .main-content {
        margin-bottom: 100px;
    }
    .sidebar .stButton>button {
        background-color: #1a5d1a;
        color: white;
        width: 100%;
    }
    .stTextInput>div>div>input {
        border-color: #1a5d1a;
    }
</style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <h2>Websitians</h2>
    <div>Social Media Analytics</div>
</div>
""", unsafe_allow_html=True)

# Rest of your code
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = "SocialMedia"

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    
    st.markdown("""
    ### Ask questions about your social media engagement data:
    - Performance metrics 📈
    - Trend analysis 📊
    - Content recommendations 💡
    """)

    initialize_session_state()

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your question..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing... 🤔"):
                try:
                    response = run_flow(prompt)
                    answer = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Sidebar
    with st.sidebar:
        st.markdown("### 📝 Sample Questions")
        if st.button("Best performing post type?"):
            st.text("Which post type has the highest engagement rate?")
        if st.button("Content strategy"):
            st.text("What content strategy would you recommend?")
        if st.button("Engagement trends"):
            st.text("Show me engagement trends over time")

        st.markdown("### ⚙️ Options")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []


if __name__ == "__main__":
    main()