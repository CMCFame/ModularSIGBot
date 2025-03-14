# ============================================================================
# ARCOS SIG Form Application - Main Entry Point
# ============================================================================
# This file serves as the entry point for the ARCOS System Implementation Guide Form
# application. It initializes the Streamlit interface and coordinates the different
# modules of the application.
# ============================================================================

import streamlit as st
from app.config import setup_page_config
from app.styles import load_css
from app.session_manager import initialize_session_state
from app.tabs import (
    location_hierarchy, trouble_locations, job_classifications,
    callout_reasons, event_types, callout_type_config,
    global_config, data_interfaces, additions, generic_tab
)
from app.helpers import render_color_key
from app.ai_assistant import render_ai_assistant
from app.exporters.csv_exporter import export_to_csv
from app.exporters.excel_exporter import export_to_excel
from datetime import datetime

def main():
    """Main application function"""
    # Initialize page config
    setup_page_config()
    
    # Load CSS
    load_css()
    
    # Initialize session state only once
    if "initialized" not in st.session_state:
        initialize_session_state()
        st.session_state.initialized = True
    
    # List of available tabs
    tabs = [
        "Location Hierarchy",
        "Trouble Locations",
        "Job Classifications",
        "Callout Reasons",
        "Event Types",
        "Callout Type Configuration",
        "Global Configuration Options",
        "Data and Interfaces",
        "Additions"
    ]

    # Display ARCOS logo and title
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("https://www.arcos-inc.com/wp-content/uploads/2020/02/ARCOS-RGB-Red.svg", width=150)
        except Exception as e:
            # Fallback if image can't be loaded
            st.write("ARCOS")
            print(f"Error loading logo: {str(e)}")
    with col2:
        st.markdown('<p class="main-header">System Implementation Guide Form</p>', unsafe_allow_html=True)
        st.write("Complete your ARCOS configuration with AI assistance")

    # Display color key legend
    render_color_key()

    # Calculate progress
    completed_tabs = sum(1 for tab in tabs if any(key.startswith(tab.replace(" ", "_")) for key in st.session_state.responses))
    progress = completed_tabs / len(tabs)
    st.progress(progress)
    st.write(f"{int(progress * 100)}% complete")

    # Initialize selected_tab if not already set
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = "Location Hierarchy"
        
    # Create styled horizontal tab navigation using radio buttons
    selected_tab = st.radio(
        "Select tab:",
        tabs,
        index=tabs.index(st.session_state.selected_tab) if st.session_state.selected_tab in tabs else 0,
        horizontal=True
    )
    
    # Update current tab in session state if changed
    if selected_tab != st.session_state.selected_tab:
        st.session_state.selected_tab = selected_tab
        st.rerun()

    # Export buttons
    export_cols = st.columns(2)
    with export_cols[0]:
        if st.button("Export as CSV"):
            csv_data = export_to_csv()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"arcos_sig_{timestamp}.csv",
                mime="text/csv",
                key=f"download_csv_{timestamp}"
            )

    with export_cols[1]:
        if st.button("Export as Excel"):
            excel_data = export_to_excel()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"arcos_sig_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_excel_{timestamp}"
            )

    # Add a separator
    st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)
    
    # Split layout for content and AI assistant
    content_col, ai_col = st.columns([3, 1])
    
    with content_col:
        # Main content area - render the appropriate tab
        try:
            if selected_tab == "Location Hierarchy":
                location_hierarchy.render_form()
            elif selected_tab == "Trouble Locations":
                trouble_locations.render_form()
            elif selected_tab == "Job Classifications":
                job_classifications.render_form()
            elif selected_tab == "Callout Reasons":
                callout_reasons.render_form()
            elif selected_tab == "Event Types":
                event_types.render_form()
            elif selected_tab == "Callout Type Configuration":
                callout_type_config.render_form()
            elif selected_tab == "Global Configuration Options":
                global_config.render_form()
            elif selected_tab == "Data and Interfaces":
                data_interfaces.render_form()
            elif selected_tab == "Additions":
                additions.render_form()
            else:
                # For other tabs, use the generic form renderer
                generic_tab.render_form(selected_tab)
        except Exception as e:
            st.error(f"Error rendering tab: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with ai_col:
        # AI Assistant panel
        render_ai_assistant(selected_tab)

if __name__ == "__main__":
    main()