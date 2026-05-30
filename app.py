import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

# --- 1. PAGE SETUP & THEME DECORATION ---
st.set_page_config(
    page_title="DocuMind AI Pro | Smart Developer Agent",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextArea textarea { background-color: #1e293b !important; color: #38bdf8 !important; font-family: 'Fira Code', monospace !important; }
    .stSelectbox div { background-color: #1e293b !important; }
    .metric-box { background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. UI SIDEBAR CONTROLS (Input for User Credentials) ---
with st.sidebar:
    st.title("📝 DocuMind AI Pro")
    st.caption("Next-Gen Technical Documentation Engine")
    st.markdown("---")
    
    # NEW: Secure Input for User Credentials
    st.subheader("🔑 Authentication")
    project_id = st.text_input("Google Cloud Project ID", type="password")
    location = st.text_input("Location (e.g., us-central1)", value="us-central1")
    
    st.markdown("---")
    lang_type = st.selectbox("Source Language:", ["Python", "Java", "C / C++", "JavaScript / TypeScript", "Go / Rust", "SQL"])
    doc_style = st.selectbox("Output Blueprint:", ["Standard README.md", "Detailed API Reference", "Architectural Overview", "Code Logic & Flow Explainer"])

# --- 3. MAIN USER WORKSPACE ---
st.title("🚀 Smart Technical Documentation Generator")
st.write("Convert raw source files into clear, comprehensive, developer-ready reference ecosystems.")

col1, col2 = st.columns([3, 2])

with col1:
    raw_code = st.text_area("Input Source Code:", height=380, placeholder="Paste your code here...")

with col2:
    st.markdown("### 📊 Live Code Metrics Panel")
    st.markdown("""
    <div class="metric-box">
        <span style='color: #94a3b8; font-size: 12px;'>STATUS</span>
        <h3 style='margin: 5px 0; color: #38bdf8;'>Ready for Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

# --- 4. EXECUTION ---
if st.button("✨ Analyze Code & Generate Assets"):
    if not project_id:
        st.error("Please enter your Google Cloud Project ID in the sidebar.")
    elif not raw_code.strip():
        st.warning("Please paste some valid code blocks first.")
    else:
        with st.spinner("Decoding abstract structures..."):
            try:
                # Initialize Vertex AI with user-provided credentials
                vertexai.init(project=project_id, location=location)
                ai_model = GenerativeModel("gemini-1.5-flash") # Updated to supported model name
                
                system_prompt = f"""
                Analyze this {lang_type} code and compile a {doc_style} in Markdown.
                Include: 1. Architecture, 2. Interface Matrix (Table), 3. Complexity, 4. Examples, 5. Warnings.
                Code: {raw_code}
                """
                
                response = ai_model.generate_content(system_prompt)
                st.success("Documentation Generated!")
                st.markdown(response.text)
                
                st.download_button("📥 Download Markdown", response.text, "README.md", "text/markdown")
                st.balloons()
            except Exception as e:
                st.error(f"Authentication or Execution Error: {e}")
                
