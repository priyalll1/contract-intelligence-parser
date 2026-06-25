import streamlit as st
import fitz  # PyMuPDF
import json
import re
import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Autonomous Contract Intelligence Parser",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "extraction_results" not in st.session_state:
    st.session_state.extraction_results = {}
if "raw_texts" not in st.session_state:
    st.session_state.raw_texts = {}
if "raw_ai_outputs" not in st.session_state:
    st.session_state.raw_ai_outputs = {}
if "verification_states" not in st.session_state:
    st.session_state.verification_states = {}
if "edited_values" not in st.session_state:
    st.session_state.edited_values = {}

# --- CUSTOM CSS FOR PRESTIGE LAW FIRM AESTHETICS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Global Font and Base Overrides */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Prestige Law Firm Header */
.law-header {
    background: linear-gradient(135deg, #0b0f19 0%, #1e293b 50%, #111827 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(197, 168, 128, 0.25); /* Gold border */
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.law-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(197, 168, 128, 0.04) 0%, transparent 60%);
    pointer-events: none;
}
.law-title {
    font-size: 3rem;
    font-weight: 800;
    color: #f1e4c3; /* Elegant off-white gold */
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}
.law-subtitle {
    font-size: 1.25rem;
    color: #94a3b8;
    max-width: 800px;
    margin: 0 auto;
}

/* Placeholder card for inactive tabs */
.placeholder-card {
    background: rgba(30, 41, 59, 0.2);
    border: 1px dashed rgba(197, 168, 128, 0.2);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    color: #94a3b8;
    margin: 2rem 0;
}

/* Premium Gold Accent Metric Cards */
.law-card {
    background: rgba(30, 41, 59, 0.5);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(197, 168, 128, 0.15); /* Light gold border */
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}
.law-card:hover {
    transform: translateY(-4px);
    border-color: rgba(197, 168, 128, 0.45);
    box-shadow: 0 15px 30px rgba(197, 168, 128, 0.12);
}
.law-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.75rem;
}
.law-card-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #c5a880; /* Gold */
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.law-card-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.35;
}
.law-card-badge {
    align-self: flex-start;
    margin-top: 1rem;
    padding: 0.25rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
    border-radius: 9999px;
    background: rgba(197, 168, 128, 0.1);
    color: #f1e4c3;
    border: 1px solid rgba(197, 168, 128, 0.25);
}

/* Premium Buttons */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #c5a880 0%, #a37f55 100%) !important; /* Gold gradient */
    color: #0b0f19 !important; /* Dark text on gold */
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 15px rgba(197, 168, 128, 0.35) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #a37f55 0%, #c5a880 100%) !important;
    box-shadow: 0 6px 22px rgba(197, 168, 128, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* Chat bubble aesthetics */
.chat-bubble-user {
    background: rgba(197, 168, 128, 0.12);
    border: 1px solid rgba(197, 168, 128, 0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.chat-bubble-ai {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem;
    margin-bottom: 1rem;
}

.sidebar-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONFIGURATIONS PANEL ---
st.sidebar.markdown("""
<div style='text-align: center; padding-bottom: 1.5rem;'>
    <img src="https://img.icons8.com/color/120/contract.png" width="80">
    <h2 style='margin-top: 0.5rem; font-weight: 800; font-size: 1.6rem; background: linear-gradient(135deg, #c5a880, #f1e4c3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>LexAI Auditor</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🏛️ Legal Settings")

# Model Provider Dropdown
model_provider = st.sidebar.selectbox(
    "Select Model Provider:",
    ["Google Gemini", "Anthropic Claude"],
    index=0
)

# Model Selection Dropdown & API Keys
if model_provider == "Google Gemini":
    selected_model = st.sidebar.selectbox(
        "Select Model Name:",
        ["gemini-3-pro-preview", "gemini-3-flash-preview", "gemini-2.5-pro", "gemini-2.5-flash", "gemini-pro-latest"],
        index=0,
        help="gemini-3-pro-preview is Gemini 3 Pro. gemini-2.5-flash is verified working for free tier."
    )
    
    # Gemini API Key loading
    default_gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not default_gemini_key:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                default_gemini_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    if not default_gemini_key:
        default_gemini_key = "YOUR_API_KEY_HERE"
        
    api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        value=default_gemini_key,
        help="Loads key from secrets.toml by default."
    )
    anthropic_key = ""

else:  # Anthropic Claude
    selected_model = st.sidebar.selectbox(
        "Select Model Name:",
        ["claude-3-5-sonnet-latest", "claude-3-opus-20240229"],
        index=0,
        help="Requires an active Anthropic API key."
    )
    
    default_anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not default_anthropic_key:
        try:
            if "ANTHROPIC_API_KEY" in st.secrets:
                default_anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            pass
    if not default_anthropic_key:
        default_anthropic_key = "YOUR_ANTHROPIC_KEY_HERE"
        
    anthropic_key = st.sidebar.text_input(
        "Anthropic API Key",
        type="password",
        value=default_anthropic_key,
        help="Enter your Claude API key."
    )
    api_key = ""

st.sidebar.markdown("---")

# Dynamic Custom Clauses Configuration
st.sidebar.markdown("### 🎯 Custom Audit Clauses")
custom_clauses_input = st.sidebar.text_area(
    "Define custom terms to extract (comma separated):",
    value="Payment_Terms, Warranty_Period, Termination_Rights",
    help="Add custom terms to extract from contracts in real-time."
)
custom_clauses = [c.strip() for c in custom_clauses_input.split(",") if c.strip()]

st.sidebar.markdown("---")

# --- HEADER SECTION ---
st.markdown("""
<div class="law-header">
    <div class="law-title">🏛️ Autonomous Contract Intelligence Parser</div>
    <div class="law-subtitle">High-fidelity legal clause extraction, audit verification, comparative analysis, and compliance reminders powered by Gemini 3 Pro.</div>
</div>
""", unsafe_allow_html=True)

# --- WORKSPACE CONTROLS ---
col1, col2 = st.columns([1.8, 1])

with col2:
    st.markdown("### ⚡ Quick Testing (CUAD)")
    st.write("Analyze preloaded agreements from the industry-standard CUAD dataset:")
    
    # Scan for compiled CUAD files
    preloaded_options = ["Sample_Contract.pdf"]
    if os.path.exists("cuad_contracts"):
        cuad_files = [f"cuad_contracts/{f}" for f in os.listdir("cuad_contracts") if f.endswith(".pdf")]
        preloaded_options.extend(cuad_files)
        
    selected_preloaded = st.selectbox(
        "Select contract to audit:",
        preloaded_options,
        index=0,
        help="Select a generated sample contract or a real contract from the CUAD dataset."
    )
    
    run_sample = st.button("🚀 Analyze Selected Document", use_container_width=True)
    
    st.markdown(f"""
    <div class="sidebar-card">
        <span style="font-weight: 600; color: #c5a880;">📂 Document Context:</span><br>
        <span style="font-size: 0.85rem; color: #94a3b8;">
            Currently selected document: <strong>{selected_preloaded}</strong>.<br>
            Runs semantic audit over its full text content.
        </span>
    </div>
    """, unsafe_allow_html=True)

with col1:
    st.markdown("### 📥 Legal Document Inbox")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF contracts to begin analysis",
        type="pdf",
        accept_multiple_files=True,
        help="Upload multiple legal agreements to audit and compare side-by-side."
    )

# --- LLM INITIALIZATION AND PARSING LOGIC ---
trigger_analysis = False
files_to_process = []

if uploaded_files:
    for f in uploaded_files:
        files_to_process.append({"name": f.name, "stream": f.read()})
    trigger_analysis = st.button("🔍 Run Legal NLP Audit", type="primary")

elif run_sample:
    if os.path.exists(selected_preloaded):
        try:
            with open(selected_preloaded, "rb") as f:
                # Use base filename for display keys in results
                base_name = os.path.basename(selected_preloaded)
                files_to_process.append({"name": base_name, "stream": f.read()})
            trigger_analysis = True
        except Exception as e:
            st.error(f"Failed to read {selected_preloaded}: {e}")
    else:
        st.error(f"{selected_preloaded} was not found. Please run the generation or setup steps first.")

if trigger_analysis:
    if model_provider == "Google Gemini" and (not api_key.strip() or api_key == "YOUR_API_KEY_HERE"):
        st.error("❌ A Google Gemini API Key is required. Please configure it in the sidebar.")
        st.stop()
    elif model_provider == "Anthropic Claude" and (not anthropic_key.strip() or anthropic_key == "YOUR_ANTHROPIC_KEY_HERE"):
        st.error("❌ An Anthropic API Key is required. Please configure it in the sidebar.")
        st.stop()

    st.session_state.extraction_results = {}
    st.session_state.raw_texts = {}
    st.session_state.raw_ai_outputs = {}
    st.session_state.verification_states = {}
    st.session_state.edited_values = {}

    for file_info in files_to_process:
        file_name = file_info["name"]
        with st.spinner(f"Parsing PDF Structure: {file_name}..."):
            try:
                doc = fitz.open(stream=file_info["stream"], filetype="pdf")
                raw_text = "".join([page.get_text() for page in doc])
                if not raw_text.strip():
                    st.warning(f"⚠️ No readable text found in {file_name}. Skipping.")
                    continue
                st.session_state.raw_texts[file_name] = raw_text
            except Exception as e:
                st.error(f"Failed to read {file_name}: {e}")
                continue

        with st.spinner(f"Auditing clauses in {file_name}..."):
            try:
                # Build dynamic schema based on custom clauses input
                prompt_clauses = [
                    "- Governing_Law",
                    "- Liability_Limit",
                    "- Expiration_Date",
                    "- Notice_Days",
                    "- Confidentiality_Included"
                ]
                schema_fields = [
                    '  "Governing_Law": "string",',
                    '  "Liability_Limit": "string",',
                    '  "Expiration_Date": "string",',
                    '  "Notice_Days": "string",',
                    '  "Confidentiality_Included": "boolean",'
                ]
                for custom_c in custom_clauses:
                    clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', custom_c)
                    prompt_clauses.append(f"- {clean_key}")
                    schema_fields.append(f'  "{clean_key}": "string",')
                
                clauses_str = "\n".join(prompt_clauses)
                schema_str = "\n".join(schema_fields)

                prompt = PromptTemplate.from_template(
                    "You are an expert legal AI assistant. Your task is to analyze the contract text and extract specific clauses.\n\n"
                    "Extract the following fields:\n"
                    "{clauses}\n\n"
                    "Return ONLY a valid JSON object. Do not include any preambles, introductory text, explanations, or markdown code blocks (like ```json).\n\n"
                    "JSON schema format:\n"
                    "{{\n"
                    "{schema}\n"
                    "}}\n\n"
                    "Contract Text:\n"
                    "{text}\n\n"
                    "JSON Output:"
                )

                # Initialize LLM with Fallback support
                llm_model = selected_model
                using_fallback = False
                fallback_model = "gemini-2.5-flash"
                
                try:
                    if model_provider == "Google Gemini":
                        llm = ChatGoogleGenerativeAI(model=llm_model, google_api_key=api_key)
                    else:  # Claude
                        from langchain_anthropic import ChatAnthropic
                        llm = ChatAnthropic(model=llm_model, api_key=anthropic_key)
                    
                    chain = prompt | llm
                    response = chain.invoke({
                        "clauses": clauses_str,
                        "schema": schema_str,
                        "text": raw_text
                    })
                except Exception as api_err:
                    err_msg = str(api_err).lower()
                    # Check if Google Gemini failed due to quota/model and fallback to gemini-2.5-flash
                    if model_provider == "Google Gemini" and llm_model != fallback_model and ("quota" in err_msg or "limit" in err_msg or "resource_exhausted" in err_msg or "not found" in err_msg or "429" in err_msg or "404" in err_msg or "unavailable" in err_msg):
                        st.warning(f"⚠️ `{llm_model}` quota was exceeded or is unavailable. Automatically falling back to `{fallback_model}` to complete analysis.")
                        llm_model = fallback_model
                        using_fallback = True
                        
                        llm = ChatGoogleGenerativeAI(model=llm_model, google_api_key=api_key)
                        chain = prompt | llm
                        response = chain.invoke({
                            "clauses": clauses_str,
                            "schema": schema_str,
                            "text": raw_text
                        })
                    else:
                        raise api_err

                # Convert response.content to string safely (handling string and list types)
                raw_content = ""
                if isinstance(response.content, str):
                    raw_content = response.content
                elif isinstance(response.content, list):
                    for part in response.content:
                        if isinstance(part, str):
                            raw_content += part
                        elif isinstance(part, dict) and "text" in part:
                            raw_content += part["text"]
                        elif hasattr(part, "text"):
                            raw_content += part.text
                        elif hasattr(part, "get") and part.get("text"):
                            raw_content += part.get("text")
                else:
                    raw_content = str(response.content)

                st.session_state.raw_ai_outputs[file_name] = raw_content
                
                # RegEx isolation to extract JSON block safely
                match = re.search(r'\{.*\}', raw_content, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    try:
                        extracted_json = json.loads(json_str)
                        st.session_state.extraction_results[file_name] = extracted_json
                        
                        # Initialize verification states and edited values
                        st.session_state.verification_states[file_name] = {k: False for k in extracted_json.keys()}
                        st.session_state.edited_values[file_name] = {k: str(v) for k, v in extracted_json.items()}
                    except json.JSONDecodeError as jde:
                        st.error(f"JSON parsing error for {file_name}: {jde}")
                else:
                    st.error(f"Could not locate a valid JSON structure in AI response for {file_name}.")
            except Exception as e:
                st.error(f"An error occurred during extraction of {file_name}: {e}")

    if st.session_state.extraction_results:
        st.success(f"Successfully audited {len(st.session_state.extraction_results)} contract(s)!")

# --- DISPLAY NAVIGATION TABS AT TOP LEVEL (ALWAYS VISIBLE) ---
st.markdown("---")
tab_dash, tab_comp, tab_qa, tab_cal, tab_txt, tab_raw = st.tabs([
    "📋 Legal Audit Desk", 
    "⚖️ Comparative Matrix", 
    "💬 Ask the Contract (Q&A)", 
    "📅 Expiry & Compliance Alerts",
    "📄 Document Source Text", 
    "🔍 AI Audit Logs"
])

# 1. LEGAL AUDIT DESK (With verification checkmarks & overrides)
with tab_dash:
    if st.session_state.extraction_results:
        st.markdown("### 📋 Interactive Legal Audit Desk")
        st.write("Review, verify, and correct AI-extracted clauses before exporting your official report.")
        
        selected_file = st.selectbox("Select Agreement to Audit:", list(st.session_state.extraction_results.keys()))
        
        if selected_file:
            data = st.session_state.extraction_results[selected_file]
            
            st.markdown(f"#### Auditing Contract: `{selected_file}`")
            
            # Form grid layout for interactive checklist
            clauses_keys = list(data.keys())
            
            # We display clauses dynamically, allowing inline text modifications and verification
            for k in clauses_keys:
                clean_name = k.replace('_', ' ')
                
                # Retrieve states
                is_verified = st.session_state.verification_states[selected_file].get(k, False)
                current_val = st.session_state.edited_values[selected_file].get(k, str(data[k]))
                
                c_card, c_edit, c_check = st.columns([1.5, 2, 0.8])
                
                with c_card:
                    icon = "🏛️" if k == "Governing_Law" else "🛡️" if k == "Liability_Limit" else "📅" if k == "Expiration_Date" else "🔔" if k == "Notice_Days" else "🔒" if k == "Confidentiality_Included" else "📌"
                    badge_style = "badge-law" if k == "Governing_Law" else "badge-limit" if k == "Liability_Limit" else "badge-date" if k == "Expiration_Date" else "badge-notice" if k == "Notice_Days" else "badge-conf" if k == "Confidentiality_Included" else "badge-custom"
                    st.markdown(f"""
                    <div class="law-card">
                        <div>
                            <div class="law-card-icon">{icon}</div>
                            <div class="law-card-title">{clean_name}</div>
                            <div class="law-card-value">{current_val}</div>
                        </div>
                        <div class="law-card-badge {badge_style}">{"✓ Verified" if is_verified else "Pending Audit"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_edit:
                    new_val = st.text_input(
                        f"Override/Correct value for {clean_name}:",
                        value=current_val,
                        key=f"input_{selected_file}_{k}"
                    )
                    st.session_state.edited_values[selected_file][k] = new_val
                    
                with c_check:
                    st.write("")
                    st.write("")
                    verified = st.checkbox(
                        "Mark Verified",
                        value=is_verified,
                        key=f"check_{selected_file}_{k}"
                    )
                    st.session_state.verification_states[selected_file][k] = verified
                
                st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.1;'/>", unsafe_allow_html=True)
            
            # Download & PDF Generation Options
            st.markdown("### 📥 Export Verified Audit Reports")
            col_json, col_pdf = st.columns(2)
            
            with col_json:
                final_json = st.session_state.edited_values[selected_file]
                json_bytes = json.dumps(final_json, indent=4).encode('utf-8')
                st.download_button(
                    label="📥 Download Structured JSON File",
                    data=json_bytes,
                    file_name=f"audited_{selected_file.replace('.pdf', '')}.json",
                    mime="application/json"
                )
                
            with col_pdf:
                # Generate PDF using FPDF
                try:
                    pdf_report = FPDF()
                    pdf_report.add_page()
                    
                    # Header
                    pdf_report.set_font("Arial", 'B', 16)
                    pdf_report.cell(0, 15, "LEGAL CONTRACT AUDIT REPORT", 0, 1, 'C')
                    pdf_report.set_font("Arial", 'I', 10)
                    pdf_report.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
                    pdf_report.ln(5)
                    
                    # Project Info
                    pdf_report.set_font("Arial", 'B', 11)
                    pdf_report.cell(40, 8, "Document Name:", 0, 0, 'L')
                    pdf_report.set_font("Arial", size=11)
                    pdf_report.cell(0, 8, selected_file, 0, 1, 'L')
                    
                    pdf_report.set_font("Arial", 'B', 11)
                    pdf_report.cell(40, 8, "Audited Status:", 0, 0, 'L')
                    pdf_report.set_font("Arial", size=11)
                    tot_verified = sum(st.session_state.verification_states[selected_file].values())
                    tot_clauses = len(clauses_keys)
                    pdf_report.cell(0, 8, f"{tot_verified} of {tot_clauses} clauses verified", 0, 1, 'L')
                    pdf_report.ln(10)
                    
                    # Columns Header
                    pdf_report.set_fill_color(240, 240, 240)
                    pdf_report.set_font("Arial", 'B', 10)
                    pdf_report.cell(60, 10, "Clause Title", 1, 0, 'L', True)
                    pdf_report.cell(95, 10, "Verified Value", 1, 0, 'L', True)
                    pdf_report.cell(35, 10, "Status", 1, 1, 'C', True)
                    
                    # Rows
                    pdf_report.set_font("Arial", size=9)
                    for k in clauses_keys:
                        title_str = k.replace('_', ' ')
                        val_str = st.session_state.edited_values[selected_file][k]
                        stat_str = "Verified" if st.session_state.verification_states[selected_file][k] else "Pending"
                        
                        pdf_report.cell(60, 8, title_str, 1, 0, 'L')
                        pdf_report.cell(95, 8, val_str, 1, 0, 'L')
                        pdf_report.cell(35, 8, stat_str, 1, 1, 'C')
                        
                    pdf_output_bytes = pdf_report.output(dest='S').encode('latin-1', 'replace')
                    
                    st.download_button(
                        label="📥 Download PDF Legal Audit Report",
                        data=pdf_output_bytes,
                        file_name=f"legal_report_{selected_file.replace('.pdf', '')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as ex:
                    st.error(f"Error compiling PDF report: {ex}")
                    
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>📋 Legal Audit Desk is Locked</h3>
            <p>Upload a contract PDF or run the sample analysis to render the interactive legal checklist and PDF report generator.</p>
        </div>
        """, unsafe_allow_html=True)

# 2. COMPARATIVE MATRIX
with tab_comp:
    if st.session_state.extraction_results:
        st.markdown("### 📊 Legal Comparative Matrix")
        st.write("Compare audited and corrected terms across multiple agreements side-by-side.")
        
        rows = []
        for file_name, _ in st.session_state.extraction_results.items():
            row = {"Contract File": file_name}
            # Use current edited values (from session state) instead of raw values!
            row.update(st.session_state.edited_values[file_name])
            rows.append(row)
        
        df_comparison = pd.DataFrame(rows)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Export CSV Button
        st.markdown("### 💾 Export Matrix")
        csv_bytes = df_comparison.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Comparison Table (CSV)",
            data=csv_bytes,
            file_name="contract_comparison_matrix.csv",
            mime="text/csv"
        )
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>📊 Comparative Matrix is Locked</h3>
            <p>Upload contract PDFs or click <strong>🚀 Analyze Sample_Contract.pdf</strong> to compile the multi-document structured comparison view.</p>
        </div>
        """, unsafe_allow_html=True)

# 3. ASK THE CONTRACT (Q&A)
with tab_qa:
    if st.session_state.raw_texts:
        st.markdown("### 💬 Conversational Legal Assistant")
        st.write("Query the AI directly about contract terms, definitions, or liabilities.")
        
        qa_file = st.selectbox("Select Contract for Query:", list(st.session_state.raw_texts.keys()))
        user_question = st.text_input("Ask a question about this contract:")
        
        if st.button("💬 Ask AI Model") and user_question.strip():
            if model_provider == "Google Gemini" and (not api_key.strip() or api_key == "YOUR_API_KEY_HERE"):
                st.error("❌ Gemini API Key required to run Q&A.")
                st.stop()
            elif model_provider == "Anthropic Claude" and (not anthropic_key.strip() or anthropic_key == "YOUR_ANTHROPIC_KEY_HERE"):
                st.error("❌ Anthropic API Key required to run Q&A.")
                st.stop()

            contract_context = st.session_state.raw_texts[qa_file]
            with st.spinner("AI is reading context and drafting response..."):
                try:
                    if model_provider == "Google Gemini":
                        llm = ChatGoogleGenerativeAI(model=selected_model, google_api_key=api_key)
                    else:  # Claude
                        from langchain_anthropic import ChatAnthropic
                        llm = ChatAnthropic(model=selected_model, api_key=anthropic_key)
                        
                    qa_prompt = PromptTemplate.from_template(
                        "You are an expert legal AI assistant. Read the contract text below and answer the user's question.\n\n"
                        "Contract Text:\n"
                        "{text}\n\n"
                        "Question: {question}\n\n"
                        "Answer the question clearly and precisely, referencing specific numbers or terms where applicable. If the answer cannot be found, state that clearly.\n\n"
                        "Answer:"
                    )
                    chain = qa_prompt | llm
                    qa_response = chain.invoke({
                        "text": contract_context,
                        "question": user_question
                    })
                    
                    st.markdown(f"""
                    <div class="chat-bubble-user">
                        <strong>👤 Question:</strong><br>{user_question}
                    </div>
                    <div class="chat-bubble-ai">
                        <strong>🤖 Response ({selected_model}):</strong><br>{qa_response.content}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Failed to formulate answer: {e}")
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>💬 Conversational Legal Assistant is Locked</h3>
            <p>Upload a contract PDF or run the sample analysis to ask questions about the contract text.</p>
        </div>
        """, unsafe_allow_html=True)

# 4. CALENDAR & EXPIRY ALERTS
with tab_cal:
    if st.session_state.extraction_results:
        st.markdown("### 📅 Expiration Calendar Coordinator")
        st.write("Confirm dates and generate `.ics` calendar events to import directly into your calendar.")
        
        cal_file = st.selectbox("Select Contract for Calendar Sync:", list(st.session_state.extraction_results.keys()))
        
        if cal_file:
            # Load corrected Expiration Date string
            raw_expiry_str = st.session_state.edited_values[cal_file].get("Expiration_Date", "")
            st.info(f"Currently Configured Expiration Date: **{raw_expiry_str}**")
            
            confirmed_date = st.date_input(
                f"Confirm Expiration Date for {cal_file}:",
                value=datetime.today()
            )
            
            if st.button("📥 Generate Calendar Event (.ics)"):
                formatted_date = confirmed_date.strftime("%Y%m%d")
                ics_payload = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Autonomous Contract Parser//EN
BEGIN:VEVENT
UID:{int(datetime.now().timestamp())}@contractparser
DTSTAMP:{datetime.now().strftime("%Y%m%dT%H%M%SZ")}
DTSTART;VALUE=DATE:{formatted_date}
DTEND;VALUE=DATE:{formatted_date}
SUMMARY:Contract Expiration: {cal_file}
DESCRIPTION:Automated expiration alert generated by Autonomous Contract Intelligence Parser.\\nGoverning Law: {st.session_state.edited_values[cal_file].get('Governing_Law')}\\nLiability Limit: {st.session_state.edited_values[cal_file].get('Liability_Limit')}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""

                st.download_button(
                    label="💾 Download .ics File",
                    data=ics_payload,
                    file_name=f"expiration_{cal_file.replace('.pdf', '')}.ics",
                    mime="text/calendar"
                )
                st.success("Calendar file ready for download! Click the button above to import it.")
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>📅 Expiration Coordinator is Locked</h3>
            <p>Upload a contract PDF or run the sample analysis to create Expiration dates calendar sync invitations.</p>
        </div>
        """, unsafe_allow_html=True)

# 5. DOCUMENT SOURCE TEXT
with tab_txt:
    if st.session_state.raw_texts:
        st.markdown("### 📄 Raw Document Text Preview")
        txt_file = st.selectbox("Select File to View:", list(st.session_state.raw_texts.keys()))
        if txt_file:
            st.text_area("Extracted Plain Text", value=st.session_state.raw_texts[txt_file], height=400, disabled=True)
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>📄 Plain Text Viewer is Locked</h3>
            <p>Upload a PDF contract or run the sample analysis to inspect the plain text extracted by PyMuPDF.</p>
        </div>
        """, unsafe_allow_html=True)

# 6. AI AUDIT LOGS
with tab_raw:
    if st.session_state.raw_ai_outputs:
        st.markdown("### 🔍 Raw AI Extraction Logs")
        log_file = st.selectbox("Select Log to Inspect:", list(st.session_state.raw_ai_outputs.keys()))
        
        if log_file:
            # Bulletproof requirement: print raw response inside 'View Raw AI Output' st.expander
            with st.expander("View Raw AI Output", expanded=True):
                st.text_area("Raw AI Content Output", value=st.session_state.raw_ai_outputs[log_file], height=200, disabled=True)
                
            st.markdown("### Cleaned isolated JSON block parsed:")
            st.json(st.session_state.extraction_results[log_file])
    else:
        st.markdown("""
        <div class="placeholder-card">
            <h3>🔍 Raw AI Logs are Locked</h3>
            <p>Upload a PDF contract or run the sample analysis to view the raw response.content inside the mandatory expanders.</p>
        </div>
        """, unsafe_allow_html=True)