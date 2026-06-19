import streamlit as st
import google.generativeai as genai

# 1. Page Configuration & Times New Roman Styling
st.set_page_config(page_title="Professional Paraphrasing Tool", layout="centered")

st.markdown("""
<style>
    * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    .stTextArea textarea {
        font-size: 16px !important;
        height: 250px !important;
    }
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        padding: 10px 24px;
        border-radius: 4px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 2. Safe Gemini API Configuration
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.error("Please add GEMINI_API_KEY in Streamlit Secrets.")

st.title("✍️ Advanced Paraphrasing Tool")
st.write("Professional plagiarism removal system powered by Gemini.")

# 3. Input Area
user_input = st.text_area("Paste your original text here:", placeholder="Type or paste content here...", key="input_box")

# 4. Logic for 1000-Word Limit
if user_input:
    words = user_input.split()
    if len(words) > 1000:
        st.error("⚠️ Alert: Input exceeds 1000 words! Extra text has been auto-removed.")
        user_input = " ".join(words[:1000])

# 5. Paraphrase Button
if st.button("Paraphrase It"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Paraphrasing..."):
            try:
                system_prompt = (
                    "You are an expert paraphrasing engine. Rewrite the user's text to completely remove plagiarism "
                    "while strictly adhering to these rules:\n"
                    "1. Keep original meaning 100% intact using context-aware synonyms.\n"
                    "2. Break long and complex sentences into shorter, readable ones.\n"
                    "3. Flip grammatical voice (Active to Passive / Passive to Active) for at least 2 lines in every 10 lines.\n"
                    "4. Strictly prevent 'The Four-Word Rule' violation. Never use 4 consecutive words identical to the source text.\n"
                    "5. Exception: Retain Proper Nouns, technical terminologies, and specific phrases exactly as they are.\n"
                    "6. Retain all HTML formatting, headings (H1, H2, H3), bold text, and list structures exactly. Only paraphrase the text inside them."
                )
                
                model = genai.GenerativeModel(
                    model_name="models/gemini-1.5-flash",
                    system_instruction=system_prompt
                )
                
                response = model.generate_content(user_input)
                st.session_state.output_text = response.text
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 6. Output Area
output_content = st.session_state.get('output_text', '')
st.text_area("Paraphrased Output:", value=output_content, placeholder="Your plagiarism-free text will appear here...", key="output_box")
