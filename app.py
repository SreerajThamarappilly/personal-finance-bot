import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="Personal Finance Chatbot", page_icon="ST")

# Title of the App and Custom Intro Message
st.title("Personal Finance Chatbot")
st.markdown("""
Welcome to the Personal Finance Chatbot! 💸  
I am here to help you manage your money better. Feel free to ask me anything about saving, budgeting, investing, or planning for your financial future.
""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    # Set up initial system message to instruct the assistant internally without showing it to the user
    st.session_state.messages = [{"role": "system", "content": "You are an assistant that answers only questions about personal finance. You can discuss topics like saving money, budgeting, investing, retirement planning, managing debt, taxes, and other aspects related to personal finance. Do not answer questions that are not related to personal finance."}]

# Display chat history for user and assistant messages only
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip system messages to avoid showing instructions
        role, content = message["role"], message["content"]
        with st.chat_message(role):
            st.markdown(content)

# Collect user input
user_input = st.chat_input("Type your personal finance question...")

# Function to get a response from OpenAI
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    # Access the content directly as an attribute
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Add a custom logo image to enhance branding
st.sidebar.image("assets/st_logo.png", width=200)  # Load the custom logo from the assets directory

# Add additional design options in the sidebar
st.sidebar.title("Personal Finance Chatbot")
st.sidebar.markdown("""
This chatbot helps you with personal finance questions.
- **Ask about:** Budgeting, saving, investing, managing debt, and more.
""")
