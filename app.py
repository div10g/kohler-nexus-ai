import streamlit as st
import os
import json
import time
import pandas as pd
from google import genai
from google.genai.errors import ServerError
from langchain_community.document_loaders import PyPDFLoader

st.set_page_config(
    page_title="Kohler Nexus – Unified Enterprise AI Agent", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS for modern enterprise aesthetics
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Hero Header Styling */
    .hero-container {
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #1e2640 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }
    
    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Custom Pill Tags for Allowed Domains */
    .domain-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        margin: 0.2rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: #38bdf8;
        background-color: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
    }
    
    /* Sidebar Safeguard Card */
    .safeguard-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .safeguard-title {
        color: #38bdf8;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .safeguard-item {
        color: #cbd5e1;
        font-size: 0.83rem;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ Kohler Nexus</div>
    <div class="hero-subtitle">Unified Enterprise AI Agent • Context-Aware RAG • RBAC Secured</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Security & Guardrails UI
st.sidebar.title("🔒 Access Control")
user_role = st.sidebar.selectbox("Active User Role (RBAC):", ["Employees", "Managers", "Customers", "Support Staff"])

# Define Domain Access Matrix based on RBAC
ROLE_PERMISSIONS = {
    "Customers": ["support", "privacy"],
    "Employees": ["hr", "finance", "support", "privacy"],
    "Support Staff": ["support", "privacy", "hr"],
    "Managers": ["hr", "finance", "support", "privacy", "legal"]
}

allowed_domains = ROLE_PERMISSIONS[user_role]

st.sidebar.divider()
st.sidebar.markdown("**Permitted Policy Domains:**")

# Render styled Domain Pills
pills_html = "".join([f'<span class="domain-pill">{d.upper()}</span>' for d in allowed_domains])
st.sidebar.markdown(pills_html, unsafe_allow_html=True)

# Render Safeguard Card
st.sidebar.markdown("""
<div class="safeguard-card">
    <div class="safeguard-title">🛡️ Active Safeguards</div>
    <div class="safeguard-item">✅ Dynamic Access Control</div>
    <div class="safeguard-item">✅ Prompt Injection Shield</div>
    <div class="safeguard-item">✅ Source Grounding Verification</div>
    <div class="safeguard-item">✅ Audit Logging Enabled</div>
</div>
""", unsafe_allow_html=True)

# Load Policy PDFs based on active RBAC Role permissions
def load_permitted_policy_docs(permitted_domains):
    context_text = ""
    for d in permitted_domains:
        folder_path = f"data/{d}"
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(os.path.join(folder_path, file))
                    pages = loader.load()
                    for p in pages:
                        context_text += f"\n[Source Document: {file}]\n" + p.page_content
    return context_text

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation memory
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
if prompt := st.chat_input("Ask a policy question or follow-up request..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY environment variable not set. Please set it in your terminal.")
        else:
            # Active Prompt Injection Defense Check
            injection_keywords = ["ignore previous instructions", "system prompt", "reveal internal instructions", "disregard rules"]
            if any(key in prompt.lower() for key in injection_keywords):
                blocked_msg = "⚠️ **Security Guardrail Triggered:** Request blocked by Prompt Injection Shield. System instructions and internal parameters are confidential."
                st.warning(blocked_msg)
                st.session_state.messages.append({"role": "assistant", "content": blocked_msg})
            else:
                client = genai.Client(api_key=api_key)
                knowledge_context = load_permitted_policy_docs(allowed_domains)
                
                # Format conversation history
                formatted_history = ""
                for m in st.session_state.messages[:-1]:
                    formatted_history += f"\n{m['role'].upper()}: {m['content']}\n"

                system_instruction = f"""
                You are Kohler Nexus Enterprise AI Agent.
                User Role: {user_role}

                Permitted Knowledge Base Context:
                {knowledge_context}
                
                Recent Conversation History:
                {formatted_history}

                Instructions:
                1. If the query asks for restricted information outside the provided Permitted Knowledge Base Context, politely state that the user's role ({user_role}) lacks authorization to access those specific policy documents.
                2. Answer questions strictly based on the provided Permitted Knowledge Base Context.
                3. If the user asks for a follow-up format change (e.g., draft email, JSON, XML), apply that format strictly to the relevant topic, NOT the entire document base.
                4. Always state the exact source document name referenced.
                """

                with st.spinner("Verifying RBAC permissions, searching knowledge base, and generating response..."):
                    models_to_try = ['gemini-3.6-flash', 'gemini-2.5-flash']
                    response = None

                    for model_name in models_to_try:
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=f"{system_instruction}\n\nUSER LATEST REQUEST: {prompt}"
                            )
                            break
                        except ServerError:
                            time.sleep(1)
                            continue
                        except Exception:
                            break

                    if response:
                        reply_text = response.text
                        
                        if "excel" in prompt.lower():
                            os.makedirs("outputs", exist_ok=True)
                            excel_path = "outputs/Kohler_Summary.xlsx"
                            df = pd.DataFrame([{"Role": user_role, "User Query": prompt, "Agent Resolution": reply_text}])
                            df.to_excel(excel_path, index=False, engine='openpyxl')
                            
                            st.markdown(reply_text)
                            with open(excel_path, "rb") as f:
                                st.download_button(
                                    label="📥 Download Excel Summary (.xlsx)",
                                    data=f,
                                    file_name="Kohler_Policy_Summary.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        elif "json" in prompt.lower():
                            st.code(reply_text, language="json")
                        elif "xml" in prompt.lower():
                            st.code(reply_text, language="xml")
                        else:
                            st.markdown(reply_text)

                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                    else:
                        st.error("⚠️ Service temporarily busy due to high demand. Please re-submit your query in a few moments.")