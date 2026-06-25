# ⚖️ Autonomous Contract Intelligence Parser

An eye-catching, production-ready legal clause extractor built with **Streamlit**, **LangChain**, and **Google Gemini 2.5 Flash**. This application parses unstructured legal contract PDFs and extracts key clauses into structured JSON format.

---

## 🚀 Key Features

* **High-Fidelity NLP Extraction**: Uses Google's advanced **Gemini 2.5 Flash** model to locate and extract legal parameters.
* **Structured Dashboard**: Renders extracted clauses in a modern dark-themed SaaS dashboard using glassmorphism styling, hover micro-animations, and status badges.
* **Precise PDF Parsing**: Employs **PyMuPDF** (`fitz`) for fast, binary-level text extraction from PDF pages.
* **Bulletproof JSON Handling**: Utilizes fallback RegEx isolation (`re.search`) to ensure robust JSON loading even if the LLM includes conversational text or preambles.
* **Secure Secrets Management**: Fully configured to use Streamlit Secrets to prevent API keys from leaking into version control.
* **Export & Download**: Download your structured legal insights as a formatted JSON file with a single click.

---

## 🛠️ Tech Stack

* **Frontend Framework**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangChain Core](https://github.com/langchain-ai/langchain)
* **AI Model**: [Google Gemini 2.5 Flash (via ChatGoogleGenerativeAI)](https://deepmind.google/technologies/gemini/)
* **PDF Reader**: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
* **PDF Generator**: [FPDF](https://pyfpdf.readthedocs.io/en/latest/)

---

## 📦 Getting Started

### 1. Clone the repository & Navigate
```bash
git clone https://github.com/your-username/contract-intelligence-parser.git
cd contract-intelligence-parser
```

### 2. Install Dependencies
Make sure you have Python installed, then install the required packages:
```bash
pip install streamlit pymupdf langchain-google-genai langchain-core fpdf
```

### 3. Generate a Sample Contract (Optional)
Run the script to generate a sample 1-page PDF contract (`Sample_Contract.pdf`) for instant testing:
```bash
python make_pdf.py
```

### 4. Configure Your Gemini API Key
To protect your key, do not hardcode it in the source code. Instead, create a local secrets file:
```bash
mkdir .streamlit
notepad .streamlit/secrets.toml
```
Paste your Gemini API key in the `secrets.toml` file:
```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### 5. Run the Application
Start the Streamlit local dev server:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 📊 Extracted Parameters Matrix

The parser is pre-engineered to search for and extract the following parameters:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `Governing_Law` | String | Jurisdiction governing the terms of the contract. |
| `Liability_Limit` | String | Financial liability cap defined in the contract. |
| `Expiration_Date` | String | Formal expiration or termination date. |
| `Notice_Days` | String | Number of days required for notice of termination. |
| `Confidentiality_Included` | Boolean | Whether non-disclosure/confidentiality clauses are active. |

---

## 📄 License
This project is open-source and free to use.
