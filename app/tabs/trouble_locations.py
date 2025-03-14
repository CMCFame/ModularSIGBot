# ============================================================================
# ARCOS SIG Form Application - Trouble Locations Tab
# ============================================================================
# This file contains the functionality for the Trouble Locations tab.
# It renders the form for configuring trouble locations that may be spoken
# to employees being called out.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Trouble Locations form with interactive elements"""
    styled_header("Trouble Locations - 2", "tab")
    
    # Instructions
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        On this tab you can define a set of Trouble Locations that may be spoken to employees being called out. This can be based on the originating location of a callout or a dropdown list. Your ARCOS project manager will discuss these options with you.
        
        Create a list below of all Trouble Locations for your company and provide pronunciations for locations which may not be obvious.
        
        If your company requires that spoken Trouble Locations be restricted by specific locations within ARCOS (when using a dropdown list), please inform your project manager.
        
        **IMPORTANT - DOUBLE CHECK WITH YOUR IMPLEMENTATION MANAGER ON THE NUMBER OF CALL RECORDINGS THAT ARE AVAILABLE IN YOUR CONTRACT**
        """)
    
    # Initialize trouble locations in session state if not already there
    if 'trouble_locations' not in st.session_state:
        st.session_state.trouble_locations = [
            {"recording_needed": True, "id": "", "location": "", "verbiage": ""}
        ]
    
    # Create table header
    st.markdown("""
    <div style="display: flex; margin-bottom: 10px; font-weight: bold; background-color: #e3051b; color: white; padding: 8px 0;">
        <div style="flex: 1; text-align: center;">Recording Needed</div>
        <div style="flex: 1; text-align: center;">ID</div>
        <div style="flex: 2; text-align: center;">Trouble Location</div>
        <div style="flex: 2; text-align: center;">Verbiage (Pronunciation)</div>
        <div style="flex: 0.5; text-align: center;">Action</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display existing entries
    for i, location in enumerate(st.session_state.trouble_locations):
        location_container = st.container()
        with location_container:
            cols = st.columns([1, 1, 2, 2, 0.5])
            
            with cols[0]:
                location["recording_needed"] = st.checkbox(
                    "Recording Needed", 
                    value=location.get("recording_needed", True),
                    key=f"rec_needed_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[1]:
                location["id"] = st.text_input(
                    "ID", 
                    value=location.get("id", ""),
                    key=f"loc_id_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[2]:
                location["location"] = st.text_input(
                    "Trouble Location", 
                    value=location.get("location", ""),
                    key=f"loc_name_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[3]:
                location["verbiage"] = st.text_input(
                    "Verbiage (Pronunciation)", 
                    value=location.get("verbiage", ""),
                    key=f"loc_verbiage_{i}",
                    label_visibility="collapsed",
                    placeholder="e.g., rok-ferd"
                )
            
            with cols[4]:
                if st.button("🗑️", key=f"del_loc_{i}", help="Remove this location"):
                    st.session_state.trouble_locations.pop(i)
                    st.rerun()
    
    # Add New Entry button
    if st.button("➕ Add Trouble Location"):
        st.session_state.trouble_locations.append(
            {"recording_needed": True, "id": "", "location": "", "verbiage": ""}
        )
        st.rerun()
    
    # Preview section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Trouble Locations Preview", "section")
    
    # Create a DataFrame for preview
    if st.session_state.trouble_locations:
        preview_data = []
        for location in st.session_state.trouble_locations:
            if location["location"]:  # Only show locations with names
                preview_data.append({
                    "Recording Needed": "X" if location["recording_needed"] else "",
                    "ID": location["id"],
                    "Trouble Location": location["location"],
                    "Pronunciation": location["verbiage"]
                })
        
        if preview_data:
            import pandas as pd
            preview_df = pd.DataFrame(preview_data)
            st.dataframe(preview_df, use_container_width=True)
        else:
            st.info("Add trouble locations to see the preview.")
    else:
        st.info("No trouble locations added yet.")
    
    # Example section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Example Entries", "section")
    
    example_data = [
        {"Recording Needed": "X", "ID": "001", "Trouble Location": "Rockford", "Pronunciation": "rok-ferd"},
        {"Recording Needed": "X", "ID": "002", "Trouble Location": "Paxton", "Pronunciation": "pak-stuhn"},
        {"Recording Needed": "", "ID": "003", "Trouble Location": "Chicago", "Pronunciation": ""}
    ]
    
    import pandas as pd
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True)
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Need Help?", "section")
    
    help_topic = st.selectbox(
        "Select topic for help",
        ["Trouble Locations", "Pronunciation Guide", "Recording Requirements", "Best Practices"]
    )
    
    if st.button("Get Help"):
        help_response = get_contextual_help(help_topic, "Trouble Locations")
        st.info(help_response)