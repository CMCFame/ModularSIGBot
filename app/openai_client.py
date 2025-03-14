# ============================================================================
# ARCOS SIG Form Application - OpenAI Client
# ============================================================================
# This file contains the functionality for interacting with the OpenAI API.
# It handles initialization of the client, sending requests, and handling responses.
# ============================================================================

import openai
import streamlit as st
from app.config import DEFAULT_MODEL, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, SYSTEM_PROMPT_PATH

class DummyClient:
    """
    A dummy client for demo purposes when API key is not available.
    Simulates the structure of the OpenAI client.
    """
    def __init__(self):
        self.chat = self
        self.completions = self
    
    def create(self, **kwargs):
        from collections import namedtuple
        Choice = namedtuple('Choice', ['message'])
        Message = namedtuple('Message', ['content'])
        Response = namedtuple('Response', ['choices'])
        
        msg = Message(content="This is a placeholder response since the OpenAI API key is not configured. In a real deployment, this would be a helpful response from the AI model.")
        choices = [Choice(message=msg)]
        return Response(choices=choices)

def initialize_openai_client():
    """Initialize and return OpenAI client for API calls"""
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return client
    except Exception as e:
        print(f"Warning: OpenAI client initialization failed - {str(e)}")
        # Create a dummy client for demo purposes when API key is not available
        return DummyClient()

def load_system_prompt():
    """Load the system prompt from prompt.txt file"""
    try:
        with open(SYSTEM_PROMPT_PATH, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Warning: Failed to load system prompt - {str(e)}")
        return "You are a helpful expert on ARCOS system implementation."

def get_openai_response(prompt, context="", model=DEFAULT_MODEL, max_tokens=DEFAULT_MAX_TOKENS, temperature=DEFAULT_TEMPERATURE):
    """
    Get response from OpenAI API
    
    Args:
        prompt (str): The user's query
        context (str): Additional context about what the user is doing
        model (str): The OpenAI model to use
        max_tokens (int): Maximum tokens in the response
        temperature (float): Creativity of the response (0.0-1.0)
        
    Returns:
        str: The model's response text
    """
    client = initialize_openai_client()
    try:
        # Load the system prompt
        system_prompt = load_system_prompt()
        
        # Add context to the system prompt if provided
        if context:
            system_prompt += f"\n\nCurrent context: {context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"