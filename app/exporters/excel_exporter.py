# ============================================================================
# ARCOS SIG Form Application - Excel Exporter
# ============================================================================
# This file contains functionality for exporting application data to Excel format.
# It creates a workbook with multiple sheets for the different configuration tabs.
# ============================================================================

import streamlit as st
import pandas as pd
import io
from app.helpers import load_callout_reasons
from app.config import ARCOS_RED

def export_to_excel():
    """
    Export data to Excel format with formatting similar to the original SIG
    
    Returns:
        bytes: Excel file as bytes object
    """
    # Use pandas to create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Create a DataFrame for Location Hierarchy
    location_data = []
    for entry in st.session_state.hierarchy_data["entries"]:
        if entry["level1"] or entry["level2"] or entry["level3"] or entry["level4"]:
            location_data.append({
                "Level 1": entry["level1"],
                "Level 2": entry["level2"],
                "Level 3": entry["level3"],
                "Level 4": entry["level4"],
                "Time Zone": entry["timezone"] if entry["timezone"] else st.session_state.hierarchy_data["timezone"],
                "Code 1": entry["codes"][0] if len(entry["codes"]) > 0 else "",
                "Code 2": entry["codes"][1] if len(entry["codes"]) > 1 else "",
                "Code 3": entry["codes"][2] if len(entry["codes"]) > 2 else "",
                "Code 4": entry["codes"][3] if len(entry["codes"]) > 3 else "",
                "Code 5": entry["codes"][4] if len(entry["codes"]) > 4 else ""
            })
    
    # Create a DataFrame for the hierarchy data
    if location_data:
        hierarchy_df = pd.DataFrame(location_data)
        hierarchy_df.to_excel(writer, sheet_name='Location Hierarchy', index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Location Hierarchy']
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': ARCOS_RED,
            'font_color': 'white',
            'border': 1
        })
        
        # Apply formatting
        for col_num, value in enumerate(hierarchy_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a DataFrame for Matrix of Locations and CO Types from the hierarchy data
    matrix_data = []
    for entry in st.session_state.hierarchy_data["entries"]:
        if entry["level4"]:
            row_data = {
                "Location": entry["level4"],
                "Normal": "X" if entry.get("callout_types", {}).get("Normal", False) else "",
                "All Hands on Deck": "X" if entry.get("callout_types", {}).get("All Hands on Deck", False) else "",
                "Fill Shift": "X" if entry.get("callout_types", {}).get("Fill Shift", False) else "",
                "Travel": "X" if entry.get("callout_types", {}).get("Travel", False) else "",
                "Notification": "X" if entry.get("callout_types", {}).get("Notification", False) else "",
                "Notification (No Response)": "X" if entry.get("callout_types", {}).get("Notification (No Response)", False) else ""
            }
            
            matrix_data.append(row_data)
    
    # Add matrix sheet
    if matrix_data:
        matrix_df = pd.DataFrame(matrix_data)
        matrix_df.to_excel(writer, sheet_name='Matrix of CO Types', index=False)
        
        # Format the matrix sheet
        worksheet = writer.sheets['Matrix of CO Types']
        for col_num, value in enumerate(matrix_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a DataFrame for Matrix of Locations and Reasons from the hierarchy data
    reasons_data = []
    for entry in st.session_state.hierarchy_data["entries"]:
        if entry["level4"] and entry.get("callout_reasons", ""):
            # Create hierarchical path for display
            hierarchy_path = []
            if entry["level1"]:
                hierarchy_path.append(entry["level1"])
            if entry["level2"]:
                hierarchy_path.append(entry["level2"])
            if entry["level3"]:
                hierarchy_path.append(entry["level3"])
            
            path_str = " > ".join(hierarchy_path)
            
            reasons_data.append({
                "Level 1": entry["level1"],
                "Level 2": entry["level2"],
                "Level 3": entry["level3"],
                "Level 4": entry["level4"],
                "Callout Reasons": entry["callout_reasons"]
            })
    
    # Add reasons sheet
    if reasons_data:
        reasons_df = pd.DataFrame(reasons_data)
        reasons_df.to_excel(writer, sheet_name='Matrix of Reasons', index=False)
        
        # Format the reasons sheet
        worksheet = writer.sheets['Matrix of Reasons']
        for col_num, value in enumerate(reasons_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a DataFrame for Job Classifications
    job_data = []
    for job in st.session_state.job_classifications:
        if job["title"]:
            job_data.append({
                "Type": job["type"],
                "Classification": job["title"],
                "ID 1": job["ids"][0] if len(job["ids"]) > 0 else "",
                "ID 2": job["ids"][1] if len(job["ids"]) > 1 else "",
                "ID 3": job["ids"][2] if len(job["ids"]) > 2 else "",
                "ID 4": job["ids"][3] if len(job["ids"]) > 3 else "",
                "ID 5": job["ids"][4] if len(job["ids"]) > 4 else "",
                "Recording": job["recording"]
            })
    
    if job_data:
        job_df = pd.DataFrame(job_data)
        job_df.to_excel(writer, sheet_name='Job Classifications', index=False)
        
        # Format the job sheet
        worksheet = writer.sheets['Job Classifications']
        for col_num, value in enumerate(job_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a DataFrame for Callout Reasons
    if 'selected_callout_reasons' in st.session_state:
        callout_reasons = load_callout_reasons()
        selected_reasons = [r for r in callout_reasons if r.get("ID") in st.session_state.selected_callout_reasons]
        
        if selected_reasons:
            reason_data = [{
                "ID": r.get("ID", ""),
                "Callout Reason": r.get("Callout Reason Drop-Down Label", ""),
                "Use?": "X" if r.get("ID") in st.session_state.selected_callout_reasons else "",
                "Default?": "X" if r.get("ID") == st.session_state.default_callout_reason else "",
                "Verbiage": r.get("Verbiage", "")
            } for r in callout_reasons]  # Include all reasons with "Use?" marked
            
            reason_df = pd.DataFrame(reason_data)
            reason_df.to_excel(writer, sheet_name='Callout Reasons', index=False)
            
            # Format the reasons sheet
            worksheet = writer.sheets['Callout Reasons']
            for col_num, value in enumerate(reason_df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
    # Create a DataFrame for Trouble Locations
    trouble_data = []
    for location in st.session_state.trouble_locations:
        if location["location"]:
            trouble_data.append({
                "Recording Needed": "X" if location["recording_needed"] else "",
                "ID": location["id"],
                "Trouble Location": location["location"],
                "Pronunciation": location["verbiage"]
            })
            
    if trouble_data:
        trouble_df = pd.DataFrame(trouble_data)
        trouble_df.to_excel(writer, sheet_name='Trouble Locations', index=False)
        
        # Format the trouble locations sheet
        worksheet = writer.sheets['Trouble Locations']
        for col_num, value in enumerate(trouble_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a sheet for Event Types
    event_data = []
    for event in st.session_state.event_types:
        if event["description"]:
            event_data.append({
                "ID": event["id"],
                "Description": event["description"],
                "Use?": "X" if event["use"] else "",
                "Use in Dropdown": "X" if event["use_in_dropdown"] else "",
                "Override": "X" if event["include_in_override"] else ""
            })
    
    if event_data:
        event_df = pd.DataFrame(event_data)
        event_df.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Format the event types sheet
        worksheet = writer.sheets['Event Types']
        for col_num, value in enumerate(event_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Create a sheet for other responses
    other_data = []
    for key, value in st.session_state.responses.items():
        if not key.startswith("matrix_") and not key.startswith("reason_") and value:  # Skip matrix entries, reason checkboxes and empty responses
            if "_" in key:
                parts = key.split("_", 1)
                if len(parts) > 1:
                    tab, section = parts
                    other_data.append({
                        "Tab": tab,
                        "Section": section,
                        "Response": value
                    })
    
    if other_data:
        other_df = pd.DataFrame(other_data)
        other_df.to_excel(writer, sheet_name='Other Configurations', index=False)
        
        # Format the other sheet
        worksheet = writer.sheets['Other Configurations']
        for col_num, value in enumerate(other_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    # Close the writer and get the output
    writer.close()
    
    # Seek to the beginning of the stream
    output.seek(0)
    
    return output.getvalue()