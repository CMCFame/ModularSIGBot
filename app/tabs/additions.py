# ============================================================================
# ARCOS SIG Form Application - Additions Tab
# ============================================================================
# This file contains the functionality for the Additions tab.
# It renders the form for configuring additional settings in ARCOS.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Additions form with interactive elements"""
    styled_header("Additions", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab outlines additional configuration options and data elements that may be required
        for your ARCOS system. These include specialized features like Closest-to-the-Trouble,
        qualifications, Journeyman/Apprentice rules, email alerts, and vacation management.
        
        Please provide your preferences for each section based on your operational needs.
        """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "CTT Configuration", 
        "Qualifications", 
        "J/A Rule Usage",
        "Email Alerts",
        "Vacation Management"
    ])
    
    with tab1:
        render_ctt_configuration()
        
    with tab2:
        render_qualifications()
        
    with tab3:
        render_ja_rule_usage()
        
    with tab4:
        render_email_alerts()
        
    with tab5:
        render_vacation_management()
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Need Help?", "section")
    
    help_topic = st.selectbox(
        "Select topic for help",
        ["Closest to the Trouble", "Qualifications", "J/A Rules", 
         "Email Alerts Configuration", "Vacation Management"]
    )
    
    if st.button("Get Help"):
        help_response = get_contextual_help(help_topic, "Additions")
        st.info(help_response)

def render_ctt_configuration():
    """Render the Closest-to-the-Trouble configuration section"""
    styled_header("Closest-to-the-Trouble (CTT) Configuration", "section")
    
    st.markdown("""
    Configure how the Closest-to-the-Trouble functionality works in ARCOS.
    This feature helps identify which employees are closest to an emergency location.
    """)
    
    # Truck in Garage functionality
    st.markdown("### Equipment Location")
    
    truck_in_garage = st.radio(
        "Will CTT use 'Truck in Garage' functionality?",
        ["Yes", "No", "Not Sure"],
        index=1,
        help="This determines whether vehicle/equipment location is considered",
        key="truck_in_garage"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Truck_In_Garage"] = truck_in_garage
    
    # CTT sort base
    st.markdown("### Location Basis")
    
    ctt_sort_base = st.radio(
        "Should the CTT sort be based on Level 4 Address or employee home address?",
        ["Level 4 Address", "Employee Home Address", "Both"],
        index=1,
        help="Determines which address is used as the starting point for distance calculations",
        key="ctt_sort_base"
    )
    
    # Store in session state
    st.session_state.responses["Additions_CTT_Sort_Base"] = ctt_sort_base
    
    # CTT method
    st.markdown("### Distance Calculation")
    
    ctt_method = st.radio(
        "What should the CTT Method be at callout time?",
        ["Straight Line Distance", "Drive Time", "Custom Zone-based"],
        index=1,
        help="Method used to calculate distance/time to the trouble location",
        key="ctt_method"
    )
    
    # Store in session state
    st.session_state.responses["Additions_CTT_Method"] = ctt_method
    
    # Additional CTT options
    st.markdown("### Additional CTT Options")
    
    ctt_options = st.multiselect(
        "Select additional CTT options to enable",
        ["Consider both OT order and distance", "Honor qualification requirements", 
         "Use employee-specific travel speed", "Include travel time in callout message"],
        default=["Consider both OT order and distance", "Honor qualification requirements"],
        key="ctt_options"
    )
    
    # Store in session state
    st.session_state.responses["Additions_CTT_Options"] = ", ".join(ctt_options)

def render_qualifications():
    """Render the qualifications section"""
    styled_header("Qualifications Configuration", "section")
    
    st.markdown("""
    Configure how employee qualifications are managed and used during callouts.
    This ensures that employees assigned to callouts have the necessary skills and certifications.
    """)
    
    # Qualification version
    st.markdown("### Qualification System")
    
    qual_version = st.radio(
        "Which version of QUAL's is required for your organization?",
        ["Basic Qualifications", "CMS Version of QUAL's", "Extended Attributes", "Custom Implementation"],
        index=0,
        help="Determines the qualification management system used",
        key="qual_version"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Qual_Version"] = qual_version
    
    # Callout types with qualifications
    st.markdown("### Callout Types Using Qualifications")
    
    if 'callout_type_configs' in st.session_state:
        callout_types = [config["name"] for config in st.session_state.callout_type_configs if config["name"]]
    else:
        callout_types = ["Normal", "All Hands on Deck", "Fill Shift", "Travel", "Notification"]
    
    qual_callout_types = st.multiselect(
        "Which callout types should recognize qualifications?",
        callout_types,
        default=callout_types[:2],  # Default to first two callout types
        key="qual_callout_types"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Qual_Callout_Types"] = ", ".join(qual_callout_types)
    
    # Extended attributes
    st.markdown("### Qualification Attributes")
    
    need_extended = st.checkbox(
        "Do you need Extended Attributes for qualification management?",
        value=False,
        help="Extended attributes provide more detailed qualification tracking",
        key="need_extended"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Need_Extended"] = "Yes" if need_extended else "No"
    
    if need_extended:
        extended_attrs = st.text_area(
            "List the extended attributes needed (one per line)",
            value="Expiration Date\nCertifying Authority\nCertification Level\nRestrictions",
            height=100,
            key="extended_attrs"
        )
        
        # Store in session state
        st.session_state.responses["Additions_Extended_Attrs"] = extended_attrs

def render_ja_rule_usage():
    """Render the Journeyman/Apprentice rule usage section"""
    styled_header("Journeyman/Apprentice (J/A) Rule Configuration", "section")
    
    st.markdown("""
    Configure the Journeyman/Apprentice rules for your organization.
    These rules ensure proper supervision and safety compliance during callouts.
    """)
    
    # J/A rule requirements
    st.markdown("### Basic J/A Requirements")
    
    ja_requirements = st.radio(
        "What are your J/A Rule requirements?",
        ["No J/A rules needed", "Standard 1 Journeyman to 1 Apprentice", "Custom ratio", "Other safety rules"],
        index=1,
        help="Select the J/A rule implementation needed",
        key="ja_requirements"
    )
    
    # Store in session state
    st.session_state.responses["Additions_JA_Requirements"] = ja_requirements
    
    if ja_requirements == "Custom ratio":
        custom_ratio = st.text_input(
            "Specify custom J/A ratio (e.g., '1:2' for 1 Journeyman to 2 Apprentices)",
            value="1:2",
            key="custom_ratio"
        )
        
        # Store in session state
        st.session_state.responses["Additions_Custom_Ratio"] = custom_ratio
    
    # Apprentice limitations
    st.markdown("### Apprentice Limitations")
    
    one_apprentice = st.checkbox(
        "Should only one Apprentice be allowed to accept for any callout?",
        value=False,
        help="This restricts callouts to at most one apprentice",
        key="one_apprentice"
    )
    
    # Store in session state
    st.session_state.responses["Additions_One_Apprentice"] = "Yes" if one_apprentice else "No"
    
    single_unavailable = st.checkbox(
        "For single-person callouts, should Apprentices be unavailable?",
        value=True,
        help="This prevents apprentices from accepting single-person callouts",
        key="single_unavailable"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Single_Unavailable"] = "Yes" if single_unavailable else "No"
    
    # Additional J/A rules
    st.markdown("### Additional J/A Rules")
    
    additional_ja_rules = st.text_area(
        "Describe any additional J/A rules needed for your organization",
        value="",
        height=100,
        placeholder="Enter any additional rules or requirements for Journeyman/Apprentice relationships here...",
        key="additional_ja_rules"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Additional_JA_Rules"] = additional_ja_rules

def render_email_alerts():
    """Render the email alerts section"""
    styled_header("Email Alerts Configuration", "section")
    
    st.markdown("""
    Configure email alerts for different events in ARCOS. These alerts keep
    stakeholders informed of important system activities.
    """)
    
    # Email alerts required
    st.markdown("### Email Alert Requirements")
    
    email_alerts = st.radio(
        "Are email alerts required for your organization?",
        ["Yes", "No", "Not sure"],
        index=0,
        help="Determines if email alerts will be configured",
        key="email_alerts"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Email_Alerts"] = email_alerts
    
    if email_alerts == "Yes":
        # Alert events
        st.markdown("### Alert Events")
        
        alert_events = st.multiselect(
            "Which events should trigger email alerts?",
            ["Callout Complete", "Callout Done/Closed", "Audit Alert", "No Accept", 
             "No Response", "Callout Started", "Roster Changed", "Configuration Changed"],
            default=["Callout Complete", "Audit Alert", "No Accept"],
            key="alert_events"
        )
        
        # Store in session state
        st.session_state.responses["Additions_Alert_Events"] = ", ".join(alert_events)
        
        # Alert recipients
        st.markdown("### Alert Recipients")
        
        recipients = {}
        
        st.write("Specify who should receive each type of alert:")
        
        for event in alert_events:
            recipient_types = st.multiselect(
                f"Who should receive '{event}' alerts?",
                ["Supervisor", "Manager", "Dispatcher", "System Administrator", "Initiator", "Custom Email Group"],
                default=["Supervisor", "Initiator"] if "Callout" in event else ["System Administrator"],
                key=f"recipients_{event}"
            )
            
            recipients[event] = recipient_types
        
        # Store in session state as a formatted string
        recipients_str = "; ".join([f"{event}: {', '.join(recips)}" for event, recips in recipients.items()])
        st.session_state.responses["Additions_Alert_Recipients"] = recipients_str

def render_vacation_management():
    """Render the vacation management section"""
    styled_header("Vacation Management Configuration", "section")
    
    st.markdown("""
    Configure vacation management settings for your organization.
    This includes how vacation time is awarded, tracked, and managed.
    """)
    
    # Vacation leave groups
    st.markdown("### Vacation Leave Groups")
    
    vlg_config = st.radio(
        "How will Vacation Leave Groups (VLG's) be configured?",
        ["Standard Configuration", "Job Classification Based", "Location Based", "Custom Configuration"],
        index=0,
        help="Determines how vacation groups are organized",
        key="vlg_config"
    )
    
    # Store in session state
    st.session_state.responses["Additions_VLG_Config"] = vlg_config
    
    # Vacation award
    st.markdown("### Vacation Time Awarding")
    
    award_basis = st.radio(
        "When should vacation time be awarded to employees?",
        ["Hire Date Anniversary", "Common Date (e.g., January 1)", "Fiscal Year Start", "Custom Schedule"],
        index=0,
        help="Determines when employees receive their vacation allocation",
        key="award_basis"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Award_Basis"] = award_basis
    
    # Availability rules
    st.markdown("### Minimum Availability Requirements")
    
    st.write("How many employees can be unavailable without compromising emergency response?")
    
    min_available = st.slider(
        "Minimum percentage of employees that must be available",
        min_value=50,
        max_value=95,
        value=75,
        step=5,
        format="%d%%",
        help="Minimum percentage of employees that must be available at any time",
        key="min_available"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Min_Available"] = f"{min_available}%"
    
    # Additional vacation settings
    st.markdown("### Additional Vacation Settings")
    
    vacation_settings = st.multiselect(
        "Select additional vacation settings to enable",
        ["Allow vacation trades", "Enable vacation bidding", "Vacation blackout dates", 
         "Rollover unused vacation", "Supervisor approval required"],
        default=["Supervisor approval required"],
        key="vacation_settings"
    )
    
    # Store in session state
    st.session_state.responses["Additions_Vacation_Settings"] = ", ".join(vacation_settings)