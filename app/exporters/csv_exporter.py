# ============================================================================
# ARCOS SIG Form Application - CSV Exporter
# ============================================================================
# This file contains functionality for exporting application data to CSV format.
# It collects data from all tabs and formats it into a downloadable CSV file.
# ============================================================================

import streamlit as st
import pandas as pd
from app.helpers import load_callout_reasons

def export_to_csv():
    """Export all form data to CSV and return CSV data"""
    # Collect data from all tabs
    data = []
    
    # Add location hierarchy data
    data.append({"Tab": "Location Hierarchy", "Section": "Labels", "Response": str(st.session_state.hierarchy_data["labels"])})
    
    # Add each location entry separately for better readability
    for i, entry in enumerate(st.session_state.hierarchy_data["entries"]):
        if entry["level1"] or entry["level2"] or entry["level3"] or entry["level4"]:
            location_str = f"Level 1: {entry['level1']}, Level 2: {entry['level2']}, Level 3: {entry['level3']}, Level 4: {entry['level4']}"
            timezone_str = entry["timezone"] if entry["timezone"] else st.session_state.hierarchy_data["timezone"]
            codes_str = ", ".join([code for code in entry["codes"] if code])
            
            # Get enabled callout types
            callout_types_str = ", ".join([ct for ct, enabled in entry.get("callout_types", {}).items() if enabled])
            
            # Get callout reasons
            callout_reasons_str = entry.get("callout_reasons", "")
            
            data.append({
                "Tab": "Location Hierarchy", 
                "Section": f"Location Entry #{i+1}", 
                "Response": f"{location_str}, Time Zone: {timezone_str}, Codes: {codes_str}"
            })
            
            # Add matrix data from the integrated callout types
            if entry["level4"] and callout_types_str:
                data.append({
                    "Tab": "Matrix of Locations and CO Types", 
                    "Section": entry["level4"], 
                    "Response": callout_types_str
                })
            
            # Add matrix data from the integrated callout reasons
            if entry["level4"] and callout_reasons_str:
                data.append({
                    "Tab": "Matrix of Locations and Reasons", 
                    "Section": entry["level4"], 
                    "Response": callout_reasons_str
                })
    
    # Add job classifications
    for i, job in enumerate(st.session_state.job_classifications):
        if job["title"]:
            ids_str = ", ".join([id for id in job["ids"] if id])
            data.append({
                "Tab": "Job Classifications",
                "Section": f"{job['title']} ({job['type']})",
                "Response": f"IDs: {ids_str}, Recording: {job['recording'] if job['recording'] else 'Same as title'}"
            })
    
    # Add callout reasons
    if 'selected_callout_reasons' in st.session_state:
        # Load reasons
        callout_reasons = load_callout_reasons()
        selected_reasons = [r for r in callout_reasons if r.get("ID") in st.session_state.selected_callout_reasons]
        
        data.append({
            "Tab": "Callout Reasons",
            "Section": "Selected Reasons",
            "Response": ", ".join([f"{r.get('ID')}: {r.get('Callout Reason Drop-Down Label')}" for r in selected_reasons])
        })
        
        if 'default_callout_reason' in st.session_state and st.session_state.default_callout_reason:
            default_reason = next((r for r in callout_reasons if r.get("ID") == st.session_state.default_callout_reason), None)
            if default_reason:
                data.append({
                    "Tab": "Callout Reasons",
                    "Section": "Default Reason",
                    "Response": f"{default_reason.get('ID')}: {default_reason.get('Callout Reason Drop-Down Label')}"
                })
    
    # Add trouble locations
    for i, location in enumerate(st.session_state.trouble_locations):
        if location["location"]:
            data.append({
                "Tab": "Trouble Locations",
                "Section": location["location"],
                "Response": f"ID: {location['id']}, Recording Needed: {'Yes' if location['recording_needed'] else 'No'}, Pronunciation: {location['verbiage'] if location['verbiage'] else 'Standard'}"
            })
    
    # Add event types
    for event in st.session_state.event_types:
        if event["use"] and event["description"]:
            data.append({
                "Tab": "Event Types",
                "Section": event["description"],
                "Response": f"ID: {event['id']}, In Dropdown: {'Yes' if event['use_in_dropdown'] else 'No'}, Override: {'Yes' if event['include_in_override'] else 'No'}"
            })
    
    # Add all other responses
    for key, value in st.session_state.responses.items():
        if not key.startswith("matrix_") and not key.startswith("reason_") and value:  # Skip matrix entries, reason checkboxes, and empty responses
            if "_" in key:
                parts = key.split("_", 1)
                if len(parts) > 1:
                    tab, section = parts
                    data.append({
                        "Tab": tab,
                        "Section": section,
                        "Response": value
                    })
    
    # Create DataFrame and return CSV
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    return csv