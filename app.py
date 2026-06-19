import streamlit as st
from google import genai
from google.genai import types

# 1. Page Styling
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

# 2. API Connection
client = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Please add GEMINI_API_KEY in Streamlit Secrets.")
except Exception as e:
    st.error(f"Secret Error: {str(e)}")

st.title("✍️ Advanced Paraphrasing Tool")

# 3. Form Setup to stop data loss on refresh
with st.form(key="my_paraphrase_form"):
    user_input = st.text_area("Paste your original text here:", placeholder="Type or paste content here...")
    submit_button = st.form_submit_button(label="Paraphrase It")

# 4. Logic & Execution
if submit_button:
    if not user_input.strip():
        st.warning("Please enter some text first.")
    elif client is None:
        st.error("API configuration is missing.")
    else:
        with st.spinner("Paraphrasing... Please wait."):
            try:
                system_prompt = (
                    "You are an expert paraphrasing engine. Rewrite the user's text to completely remove plagiarism "
                    "while keeping the original meaning intact."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    ),
                )
                
                # Directly showing the output right under the form on successful execution
                st.success("Done!")
                st.text_area("Paraphrased Output:", value=response.text, height=250)
                
            except Exception as e:
                st.error(f"API Error: {str(e)}")
