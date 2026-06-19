import streamlit as st
from google import genai
from google.genai import types

# Page Styling
st.set_page_config(page_title="Professional Paraphrasing Tool", layout="centered")

st.markdown("""
<style>
    * { font-family: 'Times New Roman', Times, serif !important; }
    .stTextArea textarea { font-size: 16px !important; height: 200px !important; }
    div.stButton > button:first-child {
        background-color: #1E3A8A; color: white; font-weight: bold; width: 100%; padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
client = None
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Please add GEMINI_API_KEY in Streamlit Secrets.")

st.title("✍️ Advanced Paraphrasing Tool")

# Input Text
user_input = st.text_area("Paste your original text here:", placeholder="Type or paste content here...", key="my_input")

output_placeholder = ""

# Process Button
if st.button("Paraphrase It"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    elif client is None:
        st.error("API client is not configured.")
    else:
        with st.spinner("Paraphrasing..."):
            try:
                system_prompt = (
                    "You are an expert paraphrasing engine. Rewrite the user's text to completely remove plagiarism "
                    "while keeping the original meaning intact. Break long sentences into shorter ones. Do not copy consecutive words."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    ),
                )
                output_placeholder = response.text
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Output Area (Directly displays the result)
st.text_area("Paraphrased Output:", value=output_placeholder, placeholder="Your plagiarism-free text will appear here...", key="my_output")
