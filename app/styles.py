# ============================================================================
# ARCOS SIG Form Application - Styles
# ============================================================================
# This file contains the CSS styling and UI elements for the application.
# It provides a consistent look and feel across all parts of the app.
# ============================================================================

import streamlit as st
from app.config import ARCOS_RED, ARCOS_LIGHT_RED, ARCOS_GREEN, ARCOS_BLUE

def load_css():
    """Load custom CSS styling for the application"""
    st.markdown("""
    <style>
        .main-header {color: #e3051b; font-size: 2.5rem; font-weight: bold;}
        .tab-header {color: #e3051b; font-size: 1.5rem; font-weight: bold; margin-top: 1rem;}
        .section-header {font-size: 1.2rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem;}
        .info-box {background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;}
        .red-bg {background-color: #ffcccc;}
        .green-bg {background-color: #99cc99;}
        .blue-bg {background-color: #6699ff;}
        .stButton>button {background-color: #e3051b; color: white;}
        .stButton>button:hover {background-color: #b30000;}
        .help-btn {font-size: 0.8rem; padding: 2px 8px;}
        .st-emotion-cache-16idsys p {font-size: 14px;}
        .hierarchy-table th {background-color: #e3051b; color: white; text-align: center; font-weight: bold;}
        .hierarchy-table td {text-align: center; padding: 8px;}
        .color-key-box {padding: 5px; margin: 2px; display: inline-block; width: 80px; text-align: center;}
        .arcos-logo {max-width: 200px; margin-bottom: 10px;}
        .download-button {background-color: #28a745; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; display: inline-block; margin-top: 10px;}
        .download-button:hover {background-color: #218838; color: white; text-decoration: none;}
        /* Navigation styling */
        .stHorizontalBlock {
            gap: 5px;
        }
        .stButton button {
            width: 100%;
        }
        .navigation-button {
            width: 100%;
            text-align: center;
            color: black;
            background-color: #f0f0f0;
            padding: 10px 0;
            border-radius: 5px;
            margin: 0 2px;
            text-decoration: none;
            font-size: 0.9em;
            display: block;
        }
        .navigation-button-active {
            width: 100%;
            text-align: center;
            color: white;
            background-color: #e3051b;
            padding: 10px 0;
            border-radius: 5px;
            margin: 0 2px;
            text-decoration: none;
            font-size: 0.9em;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

def styled_header(text, level="tab"):
    """Generate a styled header with specified level (tab, section)"""
    if level == "tab":
        return st.markdown(f'<p class="tab-header">{text}</p>', unsafe_allow_html=True)
    elif level == "section":
        return st.markdown(f'<p class="section-header">{text}</p>', unsafe_allow_html=True)
    else:
        return st.write(text)
        
def styled_expander(title, content, expanded=False):
    """Create a styled expander with markdown content"""
    with st.expander(title, expanded=expanded):
        st.markdown(content)
        
def styled_info(text):
    """Display styled info box with given text"""
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)
