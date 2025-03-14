# ============================================================================
# ARCOS SIG Form Application - Session Manager
# ============================================================================
# This file handles initialization and management of the Streamlit session state.
# It ensures that all necessary state variables are created and properly maintained.
# ============================================================================

import streamlit as st
from app.config import DEFAULT_CALLOUT_TYPES, DEFAULT_CALLOUT_REASONS

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    # General app state
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Location Hierarchy"
        
    # Location hierarchy data
    if 'hierarchy_data' not in st.session_state:
        # Initialize with some sample data, now including callout types and reasons
        st.session_state.hierarchy_data = {
            "levels": ["Level 1", "Level 2", "Level 3", "Level 4"],
            "labels": ["Parent Company", "Business Unit", "Division", "OpCenter"],
            "entries": [
                {
                    "level1": "", 
                    "level2": "", 
                    "level3": "", 
                    "level4": "", 
                    "timezone": "", 
                    "codes": ["", "", "", "", ""],
                    "callout_types": {
                        "Normal": False,
                        "All Hands on Deck": False,
                        "Fill Shift": False,
                        "Travel": False,
                        "Notification": False,
                        "Notification (No Response)": False
                    },
                    "callout_reasons": ""
                }
            ],
            "timezone": "ET / CT / MT / PT"
        }
    
    # Ensure all hierarchy entries have callout_types and callout_reasons fields
    if 'hierarchy_data' in st.session_state:
        for entry in st.session_state.hierarchy_data["entries"]:
            if "callout_types" not in entry:
                entry["callout_types"] = {
                    "Normal": False,
                    "All Hands on Deck": False,
                    "Fill Shift": False,
                    "Travel": False,
                    "Notification": False,
                    "Notification (No Response)": False
                }
            if "callout_reasons" not in entry:
                entry["callout_reasons"] = ""
        
    # Callout types and reasons
    if 'callout_types' not in st.session_state:
        st.session_state.callout_types = DEFAULT_CALLOUT_TYPES
    
    if 'callout_reasons' not in st.session_state:
        st.session_state.callout_reasons = DEFAULT_CALLOUT_REASONS
        
    # Job classifications
    if 'job_classifications' not in st.session_state:
        st.session_state.job_classifications = [
            {"type": "", "title": "", "ids": ["", "", "", "", ""], "recording": ""}
        ]
        
    # Event types
    if 'event_types' not in st.session_state:
        st.session_state.event_types = initialize_default_event_types()
        
    # Trouble locations
    if 'trouble_locations' not in st.session_state:
        st.session_state.trouble_locations = [
            {"recording_needed": True, "id": "", "location": "", "verbiage": ""}
        ]

def initialize_default_event_types():
    """Initialize default event types for the application"""
    return [
        {
            "id": "1001",
            "description": "Working - Normal Shift",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        },
        {
            "id": "1018",
            "description": "Sick",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        },
        # More default event types can be added here
    ]

def get_current_tab():
    """Get the currently selected tab name"""
    return st.session_state.current_tab if 'current_tab' in st.session_state else "Location Hierarchy"

def set_current_tab(tab_name):
    """Set the currently selected tab name"""
    st.session_state.current_tab = tab_name