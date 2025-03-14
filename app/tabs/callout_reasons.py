# ============================================================================
# ARCOS SIG Form Application - Callout Reasons Tab
# ============================================================================
# This file contains the functionality for the Callout Reasons tab.
# It renders the form for configuring the Callout Reasons available in ARCOS.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from app.helpers import load_callout_reasons
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Callout Reasons form with interactive elements"""
    styled_header("Callout Reasons", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab shows the Callout Reasons available in ARCOS.
        
        Select which callout reasons you would like to use in your ARCOS system. You can filter the list to find specific reasons,
        and mark which one should be the default. Each reason has pre-recorded verbiage that will be spoken during callouts.
        """)
    
    # Load callout reasons
    callout_reasons = load_callout_reasons()
    
    # Store selected reasons in session state if not already there
    if 'selected_callout_reasons' not in st.session_state:
        st.session_state.selected_callout_reasons = [r["ID"] for r in callout_reasons if r.get("Use?") == "x"]
    
    if 'default_callout_reason' not in st.session_state:
        default_reasons = [r["ID"] for r in callout_reasons if r.get("Default?") == "x"]
        st.session_state.default_callout_reason = default_reasons[0] if default_reasons else ""
    
    # Split the UI into left and right parts (filters/list on left, preview on right)
    # Using separate containers to avoid nesting issues
    
    # 1. Filters section
    filter_container = st.container()
    with filter_container:
        styled_header("Filter Callout Reasons", "section")
        
        # Use separate containers for each row of filters
        filter_row1 = st.container()
        with filter_row1:
            filter_cols1 = st.columns([3, 1, 1])
            
            with filter_cols1[0]:
                search_term = st.text_input("Search by name or ID", key="search_callout_reasons")
            
            with filter_cols1[1]:
                show_selected_only = st.checkbox("Show selected only", key="show_selected_only")
            
            with filter_cols1[2]:
                # Bulk operations
                if st.button("Clear All Selections"):
                    st.session_state.selected_callout_reasons = []
                    st.rerun()
    
    # Apply filters
    filtered_reasons = callout_reasons.copy()  # Create a copy to avoid modifying the original
    
    if search_term:
        search_term = search_term.lower().strip()  # Normalize and clean the search term
        
        # Create a new filtered list based on search term
        filtered_reasons = []
        for reason in callout_reasons:
            # Convert values to strings to avoid type errors
            reason_id = str(reason.get("ID", "")).lower()
            reason_label = str(reason.get("Callout Reason Drop-Down Label", "")).lower()
            
            # Check if search term appears in either ID or label
            if search_term in reason_id or search_term in reason_label:
                filtered_reasons.append(reason)
    
    # Apply selected-only filter
    if show_selected_only:
        filtered_reasons = [r for r in filtered_reasons if r.get("ID") in st.session_state.selected_callout_reasons]
    
    # 2. Results count and pagination in separate container
    pagination_container = st.container()
    with pagination_container:
        styled_header("Select Callout Reasons to Use", "section")
        
        # Show count of filtered results
        if search_term or show_selected_only:
            st.write(f"Showing {len(filtered_reasons)} of {len(callout_reasons)} reasons")
        
        # Pagination controls in separate row
        items_per_page = 15
        total_reasons = len(filtered_reasons)
        total_pages = max(1, (total_reasons + items_per_page - 1) // items_per_page)
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        # Cap current page to valid range
        st.session_state.current_page = min(st.session_state.current_page, total_pages - 1)
        st.session_state.current_page = max(st.session_state.current_page, 0)
        
        if total_pages > 1:
            page_container = st.container()
            with page_container:
                page_cols = st.columns([1, 3, 1])
                
                with page_cols[0]:
                    if st.button("◀ Previous", disabled=st.session_state.current_page == 0):
                        st.session_state.current_page = max(0, st.session_state.current_page - 1)
                        st.rerun()
                
                with page_cols[1]:
                    st.write(f"Page {st.session_state.current_page + 1} of {total_pages}")
                
                with page_cols[2]:
                    if st.button("Next ▶", disabled=st.session_state.current_page >= total_pages - 1):
                        st.session_state.current_page = min(total_pages - 1, st.session_state.current_page + 1)
                        st.rerun()
    
    # 3. Display paginated results
    render_paginated_reasons(filtered_reasons, items_per_page, total_reasons)
    
    # 4. Preview section in separate container
    render_selected_reasons_preview(callout_reasons)

def render_paginated_reasons(filtered_reasons, items_per_page, total_reasons):
    """Render the paginated list of callout reasons"""
    results_container = st.container()
    with results_container:
        # Calculate pagination indices
        start_idx = st.session_state.current_page * items_per_page
        end_idx = min(start_idx + items_per_page, total_reasons)
        
        if total_reasons == 0:
            st.info("No callout reasons match your filter criteria.")
        else:
            current_page_reasons = filtered_reasons[start_idx:end_idx]
            
            # Create separate container for each reason to avoid nesting issues
            for i, reason in enumerate(current_page_reasons):
                reason_container = st.container()
                with reason_container:
                    reason_id = str(reason.get("ID", ""))
                    reason_label = reason.get("Callout Reason Drop-Down Label", "")
                    is_default = reason_id == st.session_state.default_callout_reason
                    
                    reason_cols = st.columns([5, 2, 2])
                    with reason_cols[0]:
                        # Format row with alternating background for readability
                        background = "#f9f9f9" if i % 2 == 0 else "#ffffff"
                        
                        # Create checkbox for selection
                        default_checked = reason_id in st.session_state.selected_callout_reasons
                        is_checked = st.checkbox(
                            f"{reason_id}: {reason_label}",
                            value=default_checked,
                            key=f"reason_{reason_id}"
                        )
                        
                        # Update session state based on checkbox
                        if is_checked and reason_id not in st.session_state.selected_callout_reasons:
                            st.session_state.selected_callout_reasons.append(reason_id)
                        elif not is_checked and reason_id in st.session_state.selected_callout_reasons:
                            st.session_state.selected_callout_reasons.remove(reason_id)
                    
                    with reason_cols[1]:
                        st.write(f"Verbiage: {reason.get('Verbiage', '')}")
                    
                    with reason_cols[2]:
                        # Set as default button
                        if st.button(f"Set as Default", key=f"default_{reason_id}", 
                                   disabled=not is_checked):
                            st.session_state.default_callout_reason = reason_id
                            # Update the JSON data
                            for r in filtered_reasons:
                                r["Default?"] = "x" if r["ID"] == reason_id else ""
                            st.rerun()
                    
                    # Add a separator
                    if i < len(current_page_reasons) - 1:
                        st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

def render_selected_reasons_preview(callout_reasons):
    """Render a preview of the selected callout reasons"""
    preview_container = st.container()
    with preview_container:
        styled_header("Selected Callout Reasons", "section")
        
        selected_count = len(st.session_state.selected_callout_reasons)
        st.write(f"You have selected {selected_count} callout reason(s).")
        
        # Display selected reasons
        if selected_count > 0:
            selected_reasons = [r for r in callout_reasons if str(r.get("ID", "")) in st.session_state.selected_callout_reasons]
            
            # Create a DataFrame for display
            import pandas as pd
            selected_df = pd.DataFrame([{
                "ID": r.get("ID", ""),
                "Reason": r.get("Callout Reason Drop-Down Label", ""),
                "Default": "✓" if r.get("ID") == st.session_state.default_callout_reason else ""
            } for r in selected_reasons])
            
            st.dataframe(selected_df, use_container_width=True)
            
            # Export selected reasons button
            if st.button("Update Configuration"):
                # Update the Use? and Default? flags in the callout_reasons.json file
                for r in callout_reasons:
                    r["Use?"] = "x" if r["ID"] in st.session_state.selected_callout_reasons else ""
                    r["Default?"] = "x" if r["ID"] == st.session_state.default_callout_reason else ""
                
                # Try to save the updated json
                try:
                    import json
                    from app.config import CALLOUT_REASONS_JSON_PATH
                    with open(CALLOUT_REASONS_JSON_PATH, 'w') as file:
                        json.dump(callout_reasons, file, indent=2)
                    st.success("Callout Reasons configuration updated successfully!")
                except Exception as e:
                    st.error(f"Error saving configuration: {str(e)}")
        else:
            st.info("No callout reasons selected. Please select from the list on the left.")