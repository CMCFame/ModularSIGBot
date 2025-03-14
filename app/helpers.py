# ============================================================================
# ARCOS SIG Form Application - Helpers
# ============================================================================
# This file contains utility functions used throughout the application.
# These are general-purpose functions that don't fit into other specific modules.
# ============================================================================

import streamlit as st
import json
import pandas as pd
from app.config import CALLOUT_REASONS_JSON_PATH, DESCRIPTIONS_JSON_PATH

def render_color_key():
    """Render the color key header similar to the Excel file"""
    st.markdown("""
    <div style="margin-bottom: 15px; border: 1px solid #ddd; padding: 10px;">
        <h3>Color Key</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 5px;">
            <div class="color-key-box" style="background-color: #ffcccc;">Delete</div>
            <div class="color-key-box" style="background-color: #99cc99;">Changes</div>
            <div class="color-key-box" style="background-color: #6699ff;">Moves</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def load_callout_reasons():
    """Load callout reasons from JSON file"""
    try:
        with open(CALLOUT_REASONS_JSON_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading callout reasons: {str(e)}")
        # Return a basic set if file can't be loaded
        return [
            {"ID": "0", "Callout Reason Drop-Down Label": "", "Use?": "x", "Default?": "x", "Verbiage": "n/a"},
            {"ID": "1001", "Callout Reason Drop-Down Label": "Broken Line", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1002", "Callout Reason Drop-Down Label": "Depression Road", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1003", "Callout Reason Drop-Down Label": "Depression Yard", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1007", "Callout Reason Drop-Down Label": "Emergency", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1008", "Callout Reason Drop-Down Label": "Odor", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"}
        ]

def load_sig_descriptions():
    """Load SIG descriptions from JSON file"""
    try:
        with open(DESCRIPTIONS_JSON_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading SIG descriptions: {str(e)}")
        return {}

def load_sig_structure():
    """Load SIG structure from JSON file"""
    try:
        with open(STRUCTURE_JSON_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading SIG structure: {str(e)}")
        return {}

def generate_unique_id(prefix="id"):
    """Generate a unique identifier for UI elements"""
    import uuid
    return f"{prefix}_{str(uuid.uuid4())[:8]}"

def format_data_for_display(data, style="table"):
    """Format data for display in various formats"""
    if style == "table" and isinstance(data, list) and len(data) > 0:
        return pd.DataFrame(data)
    elif style == "code":
        return json.dumps(data, indent=2)
    else:
        return data

def validate_location_name(name):
    """Validate that location name follows ARCOS requirements
    
    Rules:
    - Must contain a blank space per 25 contiguous characters
    - Maximum length of 50 characters
    """
    if len(name) > 50:
        return False, "Location name exceeds maximum length of 50 characters"
        
    # Check for blank space per 25 contiguous characters
    chars_without_space = 0
    for char in name:
        if char == ' ':
            chars_without_space = 0
        else:
            chars_without_space += 1
            if chars_without_space > 25:
                return False, "Location name must contain a blank space per 25 contiguous characters"
    
    return True, "Valid location name"