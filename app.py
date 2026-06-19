import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration & Style
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

# 2. Initialize Session State so output doesn't disappear
if "paraphrased_result" not in st.session_state:
    st.session_state.paraphrased_result = ""

# 3. API Configuration
client = None
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Please add GEMINI_API_KEY in Streamlit Secrets.")

st.title("✍️ Advanced Paraphrasing Tool")

# 4. Input Area
user_input = st.text_area("Paste your original text here:", placeholder="Type or paste content here...", key="user_input_box")

# 5. Process Button
if st.button("Paraphrase It"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    elif client is None:
        st.error("API client configuration missing.")
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
                # Store directly in session state to prevent vanishing on reload
                st.session_state.paraphrased_result = response.text
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 6. Output Area (Reads directly from Session State)
st.text_area(
    "Paraphrased Output:", 
    value=st.session_state.paraphrased_result, 
    placeholder="Your plagiarism-free text will appear here...", 
    key="output_box"
)
