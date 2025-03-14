# ============================================================================
# ARCOS SIG Form Application - Callout Type Configuration Tab
# ============================================================================
# This file contains the functionality for the Callout Type Configuration tab.
# It renders the form for configuring different Callout Types in ARCOS.
# ============================================================================

import streamlit as st
import pandas as pd
from app.styles import styled_header
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Callout Type Configuration form with interactive elements"""
    styled_header("Callout Type Configuration", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab is used to configure the different Callout Types in ARCOS. Each callout type can have different behaviors
        and settings that determine how it works in the system.
        
        Key areas to configure include:
        - Callout attributes (abandon time, auto-extend, message elements)
        - Overlap configuration (eligibility for other callouts)
        - Schedule exception overrides (which exceptions can be overridden)
        
        For each callout type, carefully consider how it should behave in your organization and configure it accordingly.
        """)
    
    # Initialize callout type configurations if not in session state
    if 'callout_type_configs' not in st.session_state:
        st.session_state.callout_type_configs = initialize_default_callout_configs()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Basic Configuration", "Overlap Settings", "Exception Overrides"])
    
    with tab1:
        render_basic_configuration()
        
    with tab2:
        render_overlap_configuration()
        
    with tab3:
        render_exception_overrides()
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Need Help?", "section")
    
    help_topic = st.selectbox(
        "Select topic for help",
        ["Callout Types", "Callout Attributes", "Overlap Configuration", "Exception Overrides", "Best Practices"]
    )
    
    if st.button("Get Help"):
        help_response = get_contextual_help(help_topic, "Callout Type Configuration")
        st.info(help_response)

def render_basic_configuration():
    """Render the basic callout type configuration section"""
    styled_header("Basic Callout Type Configuration", "section")
    
    # Display table of all callout types
    st.markdown("""
    Configure basic attributes for each callout type. These settings control the behavior of callouts 
    including when they should be abandoned, whether working records auto-extend, and what custom message
    elements are needed.
    """)
    
    # Add new callout type button
    if st.button("➕ Add New Callout Type"):
        new_config = {
            "name": "",
            "description": "",
            "abandon_after_minutes": "60",
            "stop_accepting_after_minutes": "30",
            "auto_extend": False,
            "custom_message": "",
            "allow_overlap_start": False,
            "allow_overlap_end": False,
            "overlap_minutes": "0",
            "exceptions_to_override": []
        }
        st.session_state.callout_type_configs.append(new_config)
        st.rerun()
    
    # Display each callout type in a collapsible section
    for i, config in enumerate(st.session_state.callout_type_configs):
        with st.expander(f"{config['name'] if config['name'] else 'New Callout Type'} Configuration", expanded=i==0):
            col1, col2 = st.columns(2)
            
            with col1:
                config['name'] = st.text_input("Callout Type Name", 
                                             value=config['name'],
                                             key=f"ct_name_{i}")
                
                config['description'] = st.text_area("Description", 
                                                 value=config['description'],
                                                 key=f"ct_desc_{i}")
                
                config['abandon_after_minutes'] = st.text_input("Abandon After (minutes)", 
                                                          value=config['abandon_after_minutes'],
                                                          key=f"ct_abandon_{i}")
                
                config['stop_accepting_after_minutes'] = st.text_input("Stop Accepting After (minutes)", 
                                                                  value=config['stop_accepting_after_minutes'],
                                                                  key=f"ct_stop_{i}")
            
            with col2:
                config['auto_extend'] = st.checkbox("Working Records Auto-Extend", 
                                                 value=config['auto_extend'],
                                                 key=f"ct_extend_{i}")
                
                config['custom_message'] = st.text_area("Custom Message Elements", 
                                                     value=config['custom_message'],
                                                     key=f"ct_message_{i}")
            
            # Delete button
            if st.button("🗑️ Remove Callout Type", key=f"del_ct_{i}"):
                st.session_state.callout_type_configs.pop(i)
                st.rerun()

def render_overlap_configuration():
    """Render the overlap configuration section"""
    styled_header("Overlap Configuration", "section")
    
    st.markdown("""
    Configure whether employees working on one callout should be eligible for other callouts.
    You can specify different overlap rules for the start and end of shifts.
    """)
    
    # Create a table-like display for overlap settings
    col_headers = st.columns([3, 2, 2, 2])
    col_headers[0].write("**Callout Type**")
    col_headers[1].write("**Allow Start Overlap**")
    col_headers[2].write("**Allow End Overlap**")
    col_headers[3].write("**Overlap Minutes**")
    
    for i, config in enumerate(st.session_state.callout_type_configs):
        cols = st.columns([3, 2, 2, 2])
        
        cols[0].write(config['name'] if config['name'] else f"Callout Type #{i+1}")
        
        # Fixed version of the checkbox with lambda function
        cols[1].checkbox("Allow", 
                       value=config['allow_overlap_start'],
                       key=f"ct_overlap_start_{i}",
                       on_change=lambda i=i, val=True: update_overlap(i, "start", val))
        
        cols[2].checkbox("Allow", 
                       value=config['allow_overlap_end'],
                       key=f"ct_overlap_end_{i}",
                       on_change=lambda i=i, val=True: update_overlap(i, "end", val))
        
        # Fixed version of the text input with lambda function 
        cols[3].text_input("Minutes", 
                         value=config['overlap_minutes'],
                         key=f"ct_overlap_mins_{i}",
                         on_change=lambda i=i, val=None: update_overlap_minutes(i, val))
        
        # Add separator
        st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

def render_exception_overrides():
    """Render the exception overrides section"""
    styled_header("Exception Overrides Configuration", "section")
    
    st.markdown("""
    Configure which schedule exceptions should be overridable for each callout type.
    Some exceptions (like FMLA or Rest) may have legal or safety implications when overridden.
    """)
    
    # Get all event types that are being used
    if 'event_types' in st.session_state:
        active_event_types = [event for event in st.session_state.event_types if event["use"]]
    else:
        active_event_types = [
            {"id": "1001", "description": "Working - Normal Shift"},
            {"id": "1018", "description": "Sick"},
            {"id": "1024", "description": "Vacation"},
            {"id": "1123", "description": "FMLA"},
            {"id": "1124", "description": "Funeral"}
        ]
    
    # Render a table for each callout type
    for i, config in enumerate(st.session_state.callout_type_configs):
        if config['name']:
            with st.expander(f"Override Settings for {config['name']}", expanded=i==0):
                st.write(f"Select which exceptions can be overridden for {config['name']} callouts:")
                
                # Initialize exceptions_to_override if not present
                if 'exceptions_to_override' not in config:
                    config['exceptions_to_override'] = []
                
                # Create a grid of checkboxes
                cols_per_row = 3
                for j in range(0, len(active_event_types), cols_per_row):
                    # Create a row of columns
                    cols = st.columns(cols_per_row)
                    
                    # Fill each column with a checkbox
                    for k in range(cols_per_row):
                        idx = j + k
                        if idx < len(active_event_types):
                            event = active_event_types[idx]
                            event_id = event["id"]
                            
                            # Check if this event is in the exceptions_to_override list
                            is_checked = event_id in config['exceptions_to_override']
                            
                            # Create the checkbox
                            checkbox_val = cols[k].checkbox(
                                event["description"],
                                value=is_checked,
                                key=f"override_{i}_{event_id}"
                            )
                            
                            # Update the list based on checkbox value
                            if checkbox_val and event_id not in config['exceptions_to_override']:
                                config['exceptions_to_override'].append(event_id)
                            elif not checkbox_val and event_id in config['exceptions_to_override']:
                                config['exceptions_to_override'].remove(event_id)

def update_overlap(idx, position, value):
    """Update overlap settings for a callout type"""
    if position == "start":
        st.session_state.callout_type_configs[idx]['allow_overlap_start'] = value
    else:
        st.session_state.callout_type_configs[idx]['allow_overlap_end'] = value

def update_overlap_minutes(idx, value):
    """Update overlap minutes for a callout type"""
    st.session_state.callout_type_configs[idx]['overlap_minutes'] = value

def initialize_default_callout_configs():
    """Initialize default callout type configurations"""
    return [
        {
            "name": "Normal",
            "description": "Standard emergency callouts",
            "abandon_after_minutes": "60",
            "stop_accepting_after_minutes": "30",
            "auto_extend": True,
            "custom_message": "",
            "allow_overlap_start": False,
            "allow_overlap_end": True,
            "overlap_minutes": "30",
            "exceptions_to_override": ["1252", "1424", "1500"]  # Personal Request, Out Working, Rest Time
        },
        {
            "name": "All Hands on Deck",
            "description": "Major emergency requiring all available personnel",
            "abandon_after_minutes": "120",
            "stop_accepting_after_minutes": "90",
            "auto_extend": True,
            "custom_message": "This is an emergency all hands situation. Please respond immediately.",
            "allow_overlap_start": True,
            "allow_overlap_end": True,
            "overlap_minutes": "60",
            "exceptions_to_override": ["1252", "1424", "1500", "1188", "1372"]  # More exceptions
        },
        {
            "name": "Fill Shift",
            "description": "Scheduled overtime to fill vacant shifts",
            "abandon_after_minutes": "240",
            "stop_accepting_after_minutes": "120",
            "auto_extend": False,
            "custom_message": "",
            "allow_overlap_start": False,
            "allow_overlap_end": False,
            "overlap_minutes": "0",
            "exceptions_to_override": []
        }
    ]