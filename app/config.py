# ============================================================================
# ARCOS SIG Form Application - Configuration
# ============================================================================
# This file contains the configuration settings and constants used throughout
# the application, including color schemes, default values, and page setup.
# ============================================================================

import streamlit as st

# Define color scheme to match ARCOS branding
ARCOS_RED = "#e3051b"
ARCOS_LIGHT_RED = "#ffcccc"
ARCOS_GREEN = "#99cc99"
ARCOS_BLUE = "#6699ff"

# Default values
DEFAULT_CALLOUT_TYPES = [
    "Normal", 
    "All Hands on Deck", 
    "Fill Shift", 
    "Travel", 
    "Notification", 
    "Notification (No Response)"
]

DEFAULT_CALLOUT_REASONS = [
    "Gas Leak", 
    "Gas Fire", 
    "Gas Emergency", 
    "Car Hit Pole", 
    "Wires Down"
]

# Application paths
DATA_PATH = "data/"
STRUCTURE_JSON_PATH = f"{DATA_PATH}sig_structure.json"
DESCRIPTIONS_JSON_PATH = f"{DATA_PATH}sig_descriptions.json"
CALLOUT_REASONS_JSON_PATH = f"{DATA_PATH}callout_reasons.json"
SYSTEM_PROMPT_PATH = "prompt.txt"

# OpenAI configuration
DEFAULT_MODEL = "gpt-4o-2024-08-06"
DEFAULT_MAX_TOKENS = 800
DEFAULT_TEMPERATURE = 0.7

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="ARCOS SIG Form",
        layout="wide",
        initial_sidebar_state="expanded"
    )