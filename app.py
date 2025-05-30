import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
def configure_genai():
    # Try to get API key from Streamlit secrets first (for Streamlit Cloud)
    try:
        api_key = st.secrets["general"]["GOOGLE_API_KEY"]
    except:
        # If not in Streamlit Cloud, get from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("Please set your GOOGLE_API_KEY in .env file or Streamlit secrets")
        st.stop()
    
    genai.configure(api_key=api_key)

# Initialize Gemini model
def get_gemini_model():
    return genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure Gemini
configure_genai()
model = get_gemini_model()

# Set page config
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Gemini Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(prompt)
                response_text = response.text
                st.markdown(response_text)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"}) 
