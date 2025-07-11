import streamlit as st
from src.medex.term_ex import MedicalTermsExtraction
from src.medex.file_converter import texter
import os
import io
import sys

# Set your API key securely in .streamlit/secrets.toml or via environment variable
# api_key = st.secrets["GeminiApiKey"]  # or use st.secrets["GeminiApiKey"]
# api_key = os.getenv('GeminiApiKey')

def extract_terms(file_path):
    api_key = "AIzaSyBv2kivOgbC74UrwDd1BUVqxRkfoGXpSpk"
    model = "gemini-2.5-flash"
    text = texter(file_path)
    mte = MedicalTermsExtraction(api_key, model, text)

    # Redirect stdout to capture printed outputs
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        mte.dextraction()
        diagnosis_output = buffer.getvalue().strip()
        buffer.truncate(0); buffer.seek(0)

        mte.pextraction()
        procedural_output = buffer.getvalue().strip()
        buffer.truncate(0); buffer.seek(0)

        mte.mextraction()
        modifier_output = buffer.getvalue().strip()

    finally:
        sys.stdout = sys.__stdout__  # Restore stdout

    return diagnosis_output, procedural_output, modifier_output

def main():
    st.set_page_config(page_title="Medical Term Extractor", layout="wide")
    st.title("🩺 Medical Term Extraction App")
    st.markdown("Upload a medical record file (`.txt`) to extract **diagnosis**, **procedural**, and **modifier** terms using the Gemini model.")

    uploaded_file = st.file_uploader("📄 Choose a medical chart `.txt` file", type=["txt"])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ File uploaded successfully. Extracting terms...")

        try:
            diagnosis, procedure, modifier = extract_terms(temp_path)

            st.subheader("✅ Diagnosis Terms")
            st.code(diagnosis if diagnosis else "No diagnosis terms found.")

            st.subheader("🛠️ Procedural Terms")
            st.code(procedure if procedure else "No procedural terms found.")

            st.subheader("🔧 Modifier Terms")
            st.code(modifier if modifier else "No modifier terms found.")

        except Exception as e:
            st.error(f"❌ An error occurred during extraction: {e}")

if __name__ == "__main__":
    main()

