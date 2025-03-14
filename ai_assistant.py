# ============================================================================
# ARCOS SIG Form Application - AI Assistant
# ============================================================================
# This file contains the AI assistant functionality that helps users complete
# their ARCOS configuration by providing contextual advice and answering questions.
# ============================================================================

import streamlit as st
from app.openai_client import get_openai_response

def render_ai_assistant(current_tab):
    """
    Render the AI Assistant panel with chat functionality
    
    Args:
        current_tab (str): The currently selected tab name
    """
    st.markdown('<p class="section-header">AI Assistant</p>', unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input("Ask anything about ARCOS configuration:")
    
    if st.button("Ask AI Assistant"):
        if user_question:
            # Get context for the current tab
            context = f"The user is working on the ARCOS System Implementation Guide form. They are currently viewing the '{current_tab}' tab."
            
            # Show spinner while getting response
            with st.spinner("Getting response..."):
                # Get response from OpenAI
                response = get_openai_response(user_question, context)
                
                # Store in chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Display chat history
    st.markdown('<p class="section-header">Chat History</p>', unsafe_allow_html=True)
    
    if "chat_history" in st.session_state and st.session_state.chat_history:
        # Show recent messages
        recent_messages = st.session_state.chat_history[-6:]  # Show last 6 messages
        for msg in recent_messages:
            if msg["role"] == "user":
                st.markdown(f"<div style='background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin-bottom: 8px;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background-color: #e6f7ff; padding: 8px; border-radius: 5px; margin-bottom: 8px;'><b>Assistant:</b> {msg['content']}</div>", unsafe_allow_html=True)
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.info("No chat history yet. Ask a question to get started.")

def get_contextual_help(topic, tab_name):
    """
    Get contextual help for a specific topic within a tab
    
    Args:
        topic (str): The specific topic or field to get help with
        tab_name (str): The name of the current tab
        
    Returns:
        str: AI-generated help text
    """
    help_query = f"Explain in detail what I need to know about {topic} when configuring the {tab_name} tab in ARCOS. Include examples and best practices."
    
    with st.spinner("Loading help..."):
        help_response = get_openai_response(help_query)
        
        # Store in chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({"role": "user", "content": f"Help with {topic}"})
        st.session_state.chat_history.append({"role": "assistant", "content": help_response})
    
    return help_response