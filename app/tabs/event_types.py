# ============================================================================
# ARCOS SIG Form Application - Event Types Tab
# ============================================================================
# This file contains the functionality for the Event Types tab.
# It renders the form for configuring the different Event Types in ARCOS.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from datetime import datetime
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Event Types form with interactive elements matching the Excel format"""
    styled_header("Event Types", "tab")
    
    # Display descriptive text
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        Following are the "Event Types" that are currently used in ARCOS.
        
        - Place an "X" in the "Use?" column for each Schedule Exception you want included in your system.
        - Place an "X" in the "Use in Schedule Module Dropdown" for those Events types used as exceptions and needed in the "Add Dropdown".
        - Add additional Event Types at the bottom of the list. Include all working Event Types as well.
        - Click on the drop-down arrow in cell B3 and select "X" to view only those Schedule Exceptions you will be using.
        - Answer the questions in columns D-G, where appropriate.
        """)
    
    # Main content area
    styled_header("Event Types Configuration", "section")
    
    # Last Revision Date
    date_cols = st.columns([3, 1])
    with date_cols[0]:
        st.write("Last Revision Date:")
    with date_cols[1]:
        current_date = datetime.now().strftime("%m/%d/%Y")
        revision_date = st.text_input("", value=current_date, key="revision_date", 
                                     label_visibility="collapsed")
    
    # Create a scrollable container for the table
    with st.container():
        # Header row for mobile columns
        header_cols = st.columns([2, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2])
        
        with header_cols[0]:
            st.write("Event Description")
        with header_cols[1]:
            st.write("Use?")
        with header_cols[2]:
            st.write("Use in Schedule Module Dropdown")
        with header_cols[3]:
            st.write("Include in Override ALL?")
        with header_cols[4]:
            st.write("If an override occurs on this Schedule Exception and the employee is called and results in a non-accept, should the employee be Charged or Excused?")
        with header_cols[5]:
            st.write("If an employee is skipped during a callout due to being on this Schedule Exception, should he be Charged or Excused?")
        with header_cols[6]:
            st.write("Can the employee place themselves on this Exception on Inbound?")
        with header_cols[7]:
            st.write("Allow users to be released from this schedule record via Mobile?")
        with header_cols[8]:
            st.write("Allow users to automatically enter rest status from this schedule record via Mobile?")
        with header_cols[9]:
            st.write("Allow users to make themselves unavailable using this schedule record via Mobile?")
        with header_cols[10]:
            st.write("Allow users to place themselves on this status via rest status via Mobile?")
        with header_cols[11]:
            st.write("What is the minimum duration users can place themselves on this schedule record? (In Hours)")
        with header_cols[12]:
            st.write("What is the maximum duration users can place themselves on this schedule record? (In Hours)")
        
        # Add button for new event type
        if st.button("➕ Add New Event Type"):
            # Generate new ID (just increment the highest existing ID)
            existing_ids = [int(event["id"]) for event in st.session_state.event_types]
            new_id = str(max(existing_ids) + 1) if existing_ids else "2000"
            
            # Add new empty event type
            st.session_state.event_types.append({
                "id": new_id,
                "description": "",
                "use": False,
                "use_in_dropdown": False,
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
            })
            st.rerun()
        
        # Filter options
        filter_cols = st.columns([3, 1])
        with filter_cols[0]:
            st.write("Filter Event Types:")
        with filter_cols[1]:
            show_active_only = st.checkbox("Show active only", value=False, key="show_active_events")
        
        # Apply filter
        filtered_events = st.session_state.event_types
        if show_active_only:
            filtered_events = [event for event in filtered_events if event["use"]]
        
        # Divider
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        
        # Create each row for event types
        for i, event in enumerate(filtered_events):
            # Event row
            event_cols = st.columns([2, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2])
            
            with event_cols[0]:
                # Description
                event["description"] = st.text_input(
                    "Description", 
                    value=event["description"], 
                    key=f"event_desc_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[1]:
                # Use checkbox
                event["use"] = st.checkbox(
                    "Use", 
                    value=event["use"], 
                    key=f"event_use_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[2]:
                # Use in dropdown checkbox
                event["use_in_dropdown"] = st.checkbox(
                    "Use in Dropdown", 
                    value=event["use_in_dropdown"], 
                    key=f"event_dropdown_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[3]:
                # Override checkbox
                event["include_in_override"] = st.checkbox(
                    "Include in Override", 
                    value=event["include_in_override"], 
                    key=f"event_override_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[4]:
                # Charged or excused selection for non-accept
                event["charged_or_excused"] = st.selectbox(
                    "Charged or Excused", 
                    ["", "Charged", "Excused"], 
                    index=0 if not event["charged_or_excused"] else 
                          (1 if event["charged_or_excused"] == "Charged" else 2),
                    key=f"event_charge1_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[5]:
                # Charged or excused selection for skipped
                event["employee_on_exception"] = st.selectbox(
                    "Charged or Excused", 
                    ["", "Charged", "Excused"], 
                    index=0 if not event["employee_on_exception"] else 
                          (1 if event["employee_on_exception"] == "Charged" else 2),
                    key=f"event_charge2_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[6]:
                # Can place on inbound selection
                event["available_on_inbound"] = st.selectbox(
                    "Available on Inbound", 
                    ["", "Yes", "No"], 
                    index=0 if not event["available_on_inbound"] else 
                          (1 if event["available_on_inbound"] == "Yes" else 2),
                    key=f"event_inbound_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[7]:
                # Release via mobile
                event["release_mobile"] = st.checkbox(
                    "Release via Mobile", 
                    value=event["release_mobile"], 
                    key=f"event_release_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[8]:
                # Auto rest status
                event["release_auto"] = st.checkbox(
                    "Auto Rest", 
                    value=event["release_auto"], 
                    key=f"event_auto_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[9]:
                # Make unavailable
                event["make_unavailable"] = st.checkbox(
                    "Make Unavailable", 
                    value=event["make_unavailable"], 
                    key=f"event_unavail_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[10]:
                # Place on status
                event["place_status"] = st.checkbox(
                    "Place Status", 
                    value=event["place_status"], 
                    key=f"event_status_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[11]:
                # Min duration
                event["min_duration"] = st.text_input(
                    "Min Duration", 
                    value=event["min_duration"], 
                    key=f"event_min_{i}",
                    label_visibility="collapsed"
                )
            
            with event_cols[12]:
                # Max duration
                event["max_duration"] = st.text_input(
                    "Max Duration", 
                    value=event["max_duration"], 
                    key=f"event_max_{i}",
                    label_visibility="collapsed"
                )
            
            # Add remove button for this event type
            remove_cols = st.columns([12, 1])
            with remove_cols[1]:
                if st.button("🗑️", key=f"remove_event_{i}"):
                    st.session_state.event_types.pop(i)
                    st.rerun()
            
            # Add a horizontal line between rows for better readability
            st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    # Side panel with help content
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Help section
        styled_header("Need Help?", "section")
        help_topic = st.selectbox(
            "Select topic for help",
            ["Event Types", "Schedule Exceptions", "Override Configuration", "Mobile Configuration"]
        )
        
        if st.button("Get Help"):
            help_response = get_contextual_help(help_topic, "Event Types")
            st.info(help_response)