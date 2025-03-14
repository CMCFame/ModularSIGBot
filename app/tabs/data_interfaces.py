# ============================================================================
# ARCOS SIG Form Application - Data and Interfaces Tab
# ============================================================================
# This file contains the functionality for the Data and Interfaces tab.
# It renders the form for configuring the data elements and interfaces required
# for the ARCOS system.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Data and Interfaces form with interactive elements"""
    styled_header("Data and Interfaces", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab outlines the data elements and interfaces required for the ARCOS system.
        It's important to properly configure how employee data will be loaded and updated,
        how web traffic will be handled, and how other interfaces will operate.
        
        Coordinate with your IT department to ensure all necessary connections and data flows
        are established correctly before your ARCOS implementation.
        """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Employee Data", 
        "Web Traffic Interface", 
        "HR Interface",
        "Overtime Interface",
        "Contact Devices"
    ])
    
    with tab1:
        render_employee_data()
        
    with tab2:
        render_web_traffic()
        
    with tab3:
        render_hr_interface()
        
    with tab4:
        render_overtime_interface()
        
    with tab5:
        render_contact_devices()
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Need Help?", "section")
    
    help_topic = st.selectbox(
        "Select topic for help",
        ["Employee Data Elements", "Web Traffic Requirements", 
         "HR Interface", "Overtime Tracking", "Contact Devices Configuration"]
    )
    
    if st.button("Get Help"):
        help_response = get_contextual_help(help_topic, "Data and Interfaces")
        st.info(help_response)

def render_employee_data():
    """Render the employee data section"""
    styled_header("Employee Data Configuration", "section")
    
    st.markdown("""
    Specify the employee data elements that need to be transferred to ARCOS and
    how they should be handled.
    """)
    
    # Required data elements
    st.markdown("### Required Data Elements")
    
    required_elements = ["Employee ID", "Name", "Job Classification", "Location", "Contact Information"]
    optional_elements = ["Seniority Date", "Hire Date", "Department", "Manager", "Shift", "Skills/Qualifications", "License Information"]
    
    selected_required = st.multiselect(
        "Select required data elements to transfer to ARCOS",
        required_elements,
        default=required_elements,
        key="required_data_elements"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Required_Elements"] = ", ".join(selected_required)
    
    # Optional data elements
    st.markdown("### Optional Data Elements")
    
    selected_optional = st.multiselect(
        "Select optional data elements to transfer to ARCOS",
        optional_elements,
        default=[],
        key="optional_data_elements"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Optional_Elements"] = ", ".join(selected_optional)
    
    # Employee ID configuration
    st.markdown("### Employee ID Configuration")
    
    leading_zeros = st.radio(
        "Do employee IDs include leading zeros?",
        ["Yes", "No", "Not Applicable"],
        index=1,
        key="leading_zeros"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Leading_Zeros"] = leading_zeros
    
    id_format = st.radio(
        "Is the employee ID fixed or variable length?",
        ["Fixed Length", "Variable Length"],
        index=0,
        key="id_format"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_ID_Format"] = id_format
    
    if id_format == "Fixed Length":
        id_length = st.number_input(
            "Fixed length of employee ID",
            min_value=1,
            max_value=20,
            value=6,
            step=1,
            key="id_length"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_ID_Length"] = str(id_length)
    
    # Personally Identifiable Information
    st.markdown("### Personally Identifiable Information (PII)")
    
    pii_elements = st.multiselect(
        "Which data elements are considered PII at your company?",
        ["Employee ID", "Name", "Home Address", "Personal Phone Number", "Email Address", "SSN", "Date of Birth"],
        default=["Home Address", "Personal Phone Number", "SSN", "Date of Birth"],
        key="pii_elements"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_PII_Elements"] = ", ".join(pii_elements)

def render_web_traffic():
    """Render the web traffic interface section"""
    styled_header("Web Traffic Interface Configuration", "section")
    
    st.markdown("""
    Allow web traffic to and from the required ARCOS hostnames for all web traffic.
    Your IT department will need to ensure these hostnames are accessible through
    your corporate firewall.
    """)
    
    # Hostname configuration
    st.markdown("### Required Hostnames")
    
    hostnames = [
        "prod.rostermonster.com",
        "backup.rostermonster.com",
        "qa.rostermonster.com"
    ]
    
    for hostname in hostnames:
        st.checkbox(
            hostname,
            value=True,
            help=f"Allow traffic to and from {hostname}",
            key=f"hostname_{hostname}"
        )
    
    # Network restrictions
    st.markdown("### Network Restrictions")
    
    network_restrictions = st.radio(
        "Are there any network restrictions that might impact access to ARCOS services?",
        ["Yes", "No", "Not Sure"],
        index=2,
        key="network_restrictions"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Network_Restrictions"] = network_restrictions
    
    if network_restrictions == "Yes":
        restriction_details = st.text_area(
            "Please describe the network restrictions",
            value="",
            height=100,
            key="restriction_details"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_Restriction_Details"] = restriction_details
    
    # Security requirements
    st.markdown("### Security Requirements")
    
    security_requirements = st.multiselect(
        "Select any specific security requirements for web traffic",
        ["HTTPS Only", "IP Whitelisting", "VPN Required", "Client Certificates", "Specific Ports"],
        default=["HTTPS Only"],
        key="security_requirements"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Security_Requirements"] = ", ".join(security_requirements)

def render_hr_interface():
    """Render the HR interface section"""
    styled_header("HR Interface Configuration", "section")
    
    st.markdown("""
    Configure how employee records will be initially loaded into ARCOS and how they will be updated.
    Proper configuration ensures your ARCOS system always has up-to-date employee information.
    """)
    
    # Initial load method
    st.markdown("### Initial Data Load")
    
    initial_load = st.radio(
        "How will employee records be initially loaded into ARCOS?",
        ["CSV File", "Direct Database Connection", "Web Service/API", "Other"],
        index=0,
        key="initial_load"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Initial_Load"] = initial_load
    
    if initial_load == "Other":
        other_load = st.text_input(
            "Please specify other initial load method",
            value="",
            key="other_load"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_Other_Load"] = other_load
    
    # Update method
    st.markdown("### Ongoing Updates")
    
    update_method = st.radio(
        "How will employee data be updated in ARCOS?",
        ["Manual Updates", "Automated Electronic Updates", "Hybrid Approach"],
        index=1,
        key="update_method"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Update_Method"] = update_method
    
    if update_method in ["Automated Electronic Updates", "Hybrid Approach"]:
        update_frequency = st.selectbox(
            "How frequently will electronic updates occur?",
            ["Real-time", "Hourly", "Daily", "Weekly", "Monthly", "Other"],
            index=2,
            key="update_frequency"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_Update_Frequency"] = update_frequency
    
    # Fields not to overwrite
    st.markdown("### Update Protection")
    
    protected_fields = st.multiselect(
        "Which fields should NOT be overwritten during electronic updates?",
        ["Contact Devices", "Availability Status", "Qualifications", "Custom Notes", "Roster Position"],
        default=["Custom Notes", "Roster Position"],
        key="protected_fields"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Protected_Fields"] = ", ".join(protected_fields)

def render_overtime_interface():
    """Render the overtime interface section"""
    styled_header("Overtime Interface Configuration", "section")
    
    st.markdown("""
    Configure how overtime hours will be updated in ARCOS. This affects how callouts
    are distributed to ensure fair allocation of overtime opportunities.
    """)
    
    # Overtime update method
    st.markdown("### Overtime Hours Updates")
    
    ot_update_method = st.radio(
        "Will employee overtime hours be updated manually or electronically?",
        ["Manually", "Electronically", "Both"],
        index=1,
        key="ot_update_method"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_OT_Update_Method"] = ot_update_method
    
    if ot_update_method in ["Electronically", "Both"]:
        ot_loading = st.radio(
            "If updating electronically, should the hours load immediately or after a preview period?",
            ["Immediately", "After Preview"],
            index=0,
            key="ot_loading"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_OT_Loading"] = ot_loading
        
        ot_frequency = st.selectbox(
            "How frequently will overtime hours be updated?",
            ["Real-time", "Hourly", "Daily", "Weekly", "Pay Period", "Other"],
            index=2,
            key="ot_frequency"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_OT_Frequency"] = ot_frequency
    
    # Required fields
    if ot_update_method in ["Manually", "Both"]:
        st.markdown("### Manual Entry Required Fields")
        
        manual_ot_fields = st.multiselect(
            "If entering overtime manually, which fields are required?",
            ["Employee ID", "Date", "Hours", "Paycode", "Job Classification", "Location", "Callout Type"],
            default=["Employee ID", "Date", "Hours", "Paycode"],
            key="manual_ot_fields"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_Manual_OT_Fields"] = ", ".join(manual_ot_fields)
    
    # Multiple paycodes
    st.markdown("### Paycode Configuration")
    
    multiple_paycodes = st.checkbox(
        "Do you need multiple paycodes for different types of overtime?",
        value=True,
        help="Different paycodes might be used for different rates or types of overtime",
        key="multiple_paycodes"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Multiple_Paycodes"] = "Yes" if multiple_paycodes else "No"
    
    if multiple_paycodes:
        paycode_list = st.text_area(
            "List the paycodes with descriptions (one per line)",
            value="OT - Regular Overtime\nDT - Double Time\nHT - Holiday Time",
            height=100,
            key="paycode_list"
        )
        
        # Store in session state
        st.session_state.responses["Data_Interfaces_Paycode_List"] = paycode_list

def render_contact_devices():
    """Render the contact devices section"""
    styled_header("Contact Devices Configuration", "section")
    
    st.markdown("""
    Configure settings for employee contact devices. These settings determine how
    employees will be contacted during callouts and how they can update their contact information.
    """)
    
    # Stand By device
    st.markdown("### Primary Contact Method")
    
    require_standby = st.radio(
        "Does the Employee Record require a Stand By device?",
        ["Yes", "No", "Optional"],
        index=0,
        help="A Stand By device is the primary contact method for the employee",
        key="require_standby"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Require_Standby"] = require_standby
    
    # Number of devices
    st.markdown("### Device Limits")
    
    max_devices = st.number_input(
        "How many contact devices should each employee be able to register?",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        key="max_contact_devices"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Max_Contact_Devices"] = str(max_devices)
    
    # Temporary contact info
    st.markdown("### Temporary Contact Information")
    
    temp_contact_method = st.radio(
        "How will temporary contact information be managed?",
        ["Employee Self-Service", "Supervisor/Admin Only", "Both"],
        index=2,
        key="temp_contact_method"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Temp_Contact_Method"] = temp_contact_method
    
    temp_duration = st.selectbox(
        "Maximum duration for temporary contact information",
        ["24 hours", "48 hours", "72 hours", "1 week", "2 weeks", "Until manually removed"],
        index=2,
        key="temp_duration"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Temp_Duration"] = temp_duration
    
    # Device verification
    st.markdown("### Device Verification")
    
    verification_method = st.radio(
        "How should new contact devices be verified?",
        ["Automatic Test Call/Text", "Manual Verification", "No Verification Required"],
        index=0,
        key="verification_method"
    )
    
    # Store in session state
    st.session_state.responses["Data_Interfaces_Verification_Method"] = verification_method