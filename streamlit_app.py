import streamlit as st
from chatbot import create_azure_sql_agent
from dotenv import load_dotenv

load_dotenv(override=True)

# Set page config
st.set_page_config(
    page_title="SQL Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
        color: #000000;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #ffffff;
    }
    .chat-message.bot {
        background-color: #f0f2f6;
        color: #000000;
    }
    .chat-message div {
        color: inherit;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 SQL Chatbot")
st.markdown("Ask questions about your database in natural language.")

# Initialize chatbot
@st.cache_resource
def initialize_chatbot():
    return create_azure_sql_agent()

try:
    agent = initialize_chatbot()
    st.success("Connected to database successfully!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()

# Function to display chat messages
def display_chat_message(role, content):
    with st.container():
        st.markdown(f"""
            <div style="
                padding: 1.5rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                background-color: {'#2b313e' if role == 'user' else '#f0f2f6'};
                color: {'#ffffff' if role == 'user' else '#000000'};
            ">
                {content}
            </div>
        """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    display_chat_message(message["role"], message["content"])

# Chat input
user_input = st.chat_input("Ask a question about your data...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    display_chat_message("user", user_input)

    with st.spinner("Getting answer..."):
        try:
            # Get the response from the agent
            response = agent.run(user_input)
            
            # Add response to chat history
            st.session_state.chat_history.append({"role": "bot", "content": response})
            display_chat_message("bot", response)

        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            st.error(error_message)
            st.session_state.chat_history.append({"role": "bot", "content": error_message})
            display_chat_message("bot", error_message)

with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot helps you interact with your database using natural language.
    
    **Features:**
    - Natural language queries
    - Interactive chat interface
    
    **Example queries:**
    - "Show me the count of mortgages by branch"
    - "How many members do we have per portfolio manager"
    - "What's the total revenue by branch?"
    """)
    
    # Add a clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun() 