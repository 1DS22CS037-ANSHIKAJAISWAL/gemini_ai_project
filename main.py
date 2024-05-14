import os
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

# Import necessary modules and functions for Gemini Pro model
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)

# Set page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)


# Function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


# Load Gemini Pro model
model = load_gemini_pro_model()

# Initialize chat_session flag
chat_session_initialized = False

# Use Streamlit's option_menu to select the functionality
with st.sidebar:
    selected = option_menu("Gemini AI", ["ChatBot",
                                         "Image Captioning",
                                         "Embed text",
                                         "Ask me anything"],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill',
                                                     'textarea-t', 'patch-question-fill'],
                           default_index=0)

# Depending on the selected option, execute the corresponding functionality
if selected == "ChatBot":
    # streamlit page_title
    st.title("🤖 ChatBot")

    # Check if 'chat_session' has been initialized
    if not chat_session_initialized:
        # Start a new chat session
        chat_session = model.start_chat(history=[])

        # Assign the initialized chat session object to a session_state variable
        st.session_state.chat_session = chat_session
        chat_session_initialized = True
        print("Initialized chat session:", st.session_state.chat_session)

    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask Gemini Pro...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini Pro model and get response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display gemini-pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image captioning Page
if selected=="Image Captioning":

    # streamlit page title
    st.title("📷 Snap Narrate")

    uploaded_image=st.file_uploader("Upload an image...",type=["jpg", "jpeg","png"])

    if st.button("Generate Caption"):
        image=Image.open(uploaded_image)

        col1, col2=st.columns(2)

        with col1:
            resized_image=image.resize((800, 500))
            st.image(resized_image)

        default_prompt="write a short caption for this image"

        # getting the response from gemini-pro-vision model
        caption=gemini_pro_vision_response(default_prompt,image)

        with col2:
            st.info(caption)

# text embedding page
if selected=="Embed text":
    st.title("🔡 Embed Text")

    # input text box
    input_text=st.text_area(label="",placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        response=embedding_model_response(input_text)
        st.markdown(response)

# question answer page
if selected=="Ask me anything":
    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt=st.text_area(label="",placeholder="Ask Gemini-Pro...")

    if st.button("Get an answer"):
        response=gemini_pro_response(user_prompt)
        st.markdown(response)


