import streamlit as st
import openai

# Set up your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Streamlit App configuration
st.set_page_config(page_title="GPT Chat Interface", page_icon="💬")

# App title
st.title("GPT Chat Interface")

# Initialize session state to store conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

# Display chat history from session state
def display_chat_history():
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write("**You:** " + message["content"])
        else:
            st.write("**GPT:** " + message["content"])

# Get user input and display chat history
user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")
if user_input:
    # Append user message to messages
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Display updated chat history
    display_chat_history()

    # Get GPT response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )

    # Extract and display GPT response
    gpt_response = response["choices"][0]["message"]["content"]
    st.session_state["messages"].append({"role": "assistant", "content": gpt_response})
    
    # Clear the input field
    st.text_input("You:", key="user_input", placeholder="Type your message here...", value="", disabled=True)

# Display the chat history for all messages
display_chat_history()

# Option to clear chat history
if st.button("Clear Chat"):
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]
