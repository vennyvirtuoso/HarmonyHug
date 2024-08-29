import streamlit as st
from chatbot import HarmonyHug

def main():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>CalmMate: Your Caring Mental Health Companion</h1>", unsafe_allow_html=True)
    
    # Let the user select the type of chatbot they want to interact with
    chatbot_type = st.selectbox(
        "Select the type of conversation you want:",
        ("Cognitive Behavioral Therapy (CBT)", "Stress Management Routines")
    )
    
    # Map user selection to the appropriate internal chatbot type
    chatbot_type_map = {
        "Cognitive Behavioral Therapy (CBT)": "cbt",
        "Stress Management Routines": "stress_management"
    }
    
    chatbot = HarmonyHug(chatbot_type_map[chatbot_type])

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    with st.form(key='chat_form'):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button and user_input:
        response = chatbot.get_reply(user_input)
        st.session_state.conversation_history.append(("Query", user_input))
        st.session_state.conversation_history.append(("Assistant", response))
    
    for speaker, message in st.session_state.conversation_history:
        st.write(f"**{speaker}:** {message}")

if __name__ == "__main__":
    main()
