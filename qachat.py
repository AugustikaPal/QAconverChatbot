import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field and submit button
with st.form(key='chat_form', clear_on_submit=True):
    input_text = st.text_input("Input: ", key="input")
    submit = st.form_submit_button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history with dynamic styling
st.subheader("Chat History")

for role, text in st.session_state['chat_history']:
    text_color = "#000000"  # Default color
    bg_color = "#e2ffe2" if role == "You" else "#cce5ff"
    st.markdown(
        f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; "
        f"font-size: 18px; color: {text_color}; margin-bottom: 5px;'>"
        f"<strong>{role}:</strong> {text}</div>",
        unsafe_allow_html=True
    )