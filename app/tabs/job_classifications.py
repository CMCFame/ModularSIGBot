# ============================================================================
# ARCOS SIG Form Application - Job Classifications Tab
# ============================================================================
# This file contains the functionality for the Job Classifications tab.
# It renders the form for listing the job titles of employees in the ARCOS database.
# ============================================================================

import streamlit as st
import pandas as pd
import uuid
from app.styles import styled_header

def render_form():
    """Render the Job Classifications form with interactive elements"""
    styled_header("Job Classifications", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab is used to list the Job Classifications (job titles) of the employees that will be in the ARCOS database.
        
        List the Job Classifications (job titles) of the employees and assign each a unique ID (typically taken from your HR system).
        If you have more than one ID for a Job Class, you can separate up to 5 in different columns.
        
        If applicable, indicate Journeyman and Apprentice classes. If your company requires the option to have a duty position or classification spoken to employees
        when being called out, please indicate the verbiage.
        """)
    
    # Initialize the job classifications if not already in session state
    if 'job_classifications' not in st.session_state:
        st.session_state.job_classifications = [
            {"type": "", "title": "", "ids": ["", "", "", "", ""], "recording": ""}
        ]
    
    # Generate a unique identifier for this session
    session_id = str(uuid.uuid4())[:8]
    
    # Add new job classification button - with a unique key
    if st.button("➕ Add Job Classification", key=f"add_job_class_{session_id}"):
        st.session_state.job_classifications.append(
            {"type": "", "title": "", "ids": ["", "", "", "", ""], "recording": ""}
        )
        st.rerun()
    
    # Display and edit job classifications - avoiding nested columns
    for i, job in enumerate(st.session_state.job_classifications):
        st.markdown(f"<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Job Classification #{i+1}</b></p>", unsafe_allow_html=True)
        
        # Type and title in separate container
        type_title_container = st.container()
        with type_title_container:
            type_title_cols = st.columns([2, 3])
            with type_title_cols[0]:
                job["type"] = st.selectbox(
                    "Type", 
                    ["", "Journeyman", "Apprentice"], 
                    index=["", "Journeyman", "Apprentice"].index(job["type"]) if job["type"] in ["", "Journeyman", "Apprentice"] else 0,
                    key=f"job_type_{i}_{session_id}"
                )
            with type_title_cols[1]:
                job["title"] = st.text_input("Job Classification Title", value=job["title"], key=f"job_title_{i}_{session_id}")
        
        # IDs in separate container
        st.markdown("<p><b>Job Classification IDs</b> (up to 5)</p>", unsafe_allow_html=True)
        ids_container = st.container()
        with ids_container:
            id_cols = st.columns(5)
            for j in range(5):
                with id_cols[j]:
                    # Ensure we have enough id slots
                    while len(job["ids"]) <= j:
                        job["ids"].append("")
                    job["ids"][j] = st.text_input(f"ID {j+1}", value=job["ids"][j], key=f"job_id_{i}_{j}_{session_id}")
        
        # Recording in separate container
        recording_container = st.container()
        with recording_container:
            job["recording"] = st.text_input(
                "Recording Verbiage (what should be spoken during callout)", 
                value=job["recording"], 
                key=f"job_rec_{i}_{session_id}",
                help="Leave blank if same as Job Title"
            )
        
        # Delete button in separate container - with unique key
        delete_container = st.container()
        with delete_container:
            if st.button("🗑️ Remove", key=f"del_job_{i}_{session_id}"):
                st.session_state.job_classifications.pop(i)
                st.rerun()
    
    # Preview in separate container
    preview_container = st.container()
    with preview_container:
        styled_header("Classifications Preview", "section")
        
        if st.session_state.job_classifications:
            # Create display data
            job_data = []
            for job in st.session_state.job_classifications:
                if job["title"]:  # Only include jobs with titles
                    job_data.append({
                        "Type": job["type"],
                        "Title": job["title"],
                        "IDs": ", ".join([id for id in job["ids"] if id]),
                        "Recording": job["recording"] if job["recording"] else "(Same as title)"
                    })
            
            if job_data:
                job_df = pd.DataFrame(job_data)
                st.dataframe(job_df, use_container_width=True)
            else:
                st.info("Add job classifications to see the preview.")
        else:
            st.info("No job classifications added yet.")

def validate_job_classifications():
    """Validate job classifications data"""
    if 'job_classifications' not in st.session_state:
        return False, "No job classifications found"
    
    valid_count = 0
    for job in st.session_state.job_classifications:
        if job["title"]:
            valid_count += 1
            
            # Check if at least one ID is specified
            if not any(job["ids"]):
                return False, f"Job '{job['title']}' needs at least one ID"
    
    if valid_count == 0:
        return False, "At least one job classification is required"
    
    return True, f"{valid_count} valid job classifications found"