# ============================================================================
# ARCOS SIG Form Application - Generic Tab
# ============================================================================
# This file contains a generic tab renderer for tabs that don't have specific
# custom implementations. It renders a form based on the tab name and descriptions.
# ============================================================================

import streamlit as st
import json
from app.styles import styled_header
from app.helpers import load_sig_descriptions 
from app.ai_assistant import get_contextual_help

def render_form(tab_name):
    """
    Render a generic form for tabs that are not yet implemented with custom UI
    
    Args:
        tab_name (str): The name of the tab to render
    """
    styled_header(tab_name, "tab")
    
    # Load descriptions
    descriptions = load_sig_descriptions()
    
    try:
        if tab_name in descriptions:
            tab_desc = descriptions[tab_name]
            st.write(tab_desc["description"])
            
            # Create form fields for this tab
            for field_name, field_info in tab_desc["fields"].items():
                field_key = f"{tab_name}_{field_name}"
                
                # Create expandable section for each field
                with st.expander(f"{field_name}", expanded=False):
                    st.markdown(f"**Description:** {field_info['description']}")
                    
                    if "example" in field_info:
                        st.markdown(f"**Example:** {field_info['example']}")
                    
                    if "best_practices" in field_info:
                        st.markdown(f"**Best Practices:** {field_info['best_practices']}")
                    
                    # Get existing value from session state
                    existing_value = st.session_state.responses.get(field_key, "")
                    
                    # Display input field
                    response = st.text_area(
                        label=f"Enter your {field_name} details below",
                        value=existing_value,
                        height=150,
                        key=field_key
                    )
                    
                    # Store response in session state
                    st.session_state.responses[field_key] = response
                    
                    # Add a help button for this field
                    if st.button(f"Get more help with {field_name}", key=f"help_{field_key}"):
                        help_response = get_contextual_help(field_name, tab_name)
                        st.info(help_response)
        else:
            st.write(f"This tab allows you to configure {tab_name} settings in ARCOS.")
            
            # Generic text field for this tab
            tab_key = tab_name.replace(" ", "_").lower()
            existing_value = st.session_state.responses.get(tab_key, "")
            
            response = st.text_area(
                label=f"Enter {tab_name} details",
                value=existing_value,
                height=300,
                key=tab_key
            )
            
            st.session_state.responses[tab_key] = response
            
    except Exception as e:
        st.error(f"Error loading tab data: {str(e)}")
        
        # Generic text field as fallback
        tab_key = tab_name.replace(" ", "_").lower()
        existing_value = st.session_state.responses.get(tab_key, "")
        
        response = st.text_area(
            label=f"Enter {tab_name} details",
            value=existing_value,
            height=300,
            key=tab_key
        )
        
        st.session_state.responses[tab_key] = response