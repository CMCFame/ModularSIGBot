# ============================================================================
# ARCOS SIG Form Application - Global Configuration Options Tab
# ============================================================================
# This file contains the functionality for the Global Configuration Options tab.
# It renders the form for configuring global settings in ARCOS.
# ============================================================================

import streamlit as st
from app.styles import styled_header
from app.ai_assistant import get_contextual_help

def render_form():
    """Render the Global Configuration Options form with interactive elements"""
    styled_header("Global Configuration Options", "tab")
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab outlines the global configuration options available in ARCOS that apply across the system.
        These settings control fundamental behaviors of the ARCOS system, including:
        
        - Roster administration preferences
        - Global callout behavior
        - ARCOS add-on features
        - Roster resequencing options
        - Paycodes configuration
        - Voice Response Unit (VRU) settings
        
        Please provide your preferences for each section and consult with your ARCOS project manager
        if you have questions about specific options.
        """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Roster Preferences", 
        "Callout Options", 
        "ARCOS Add-Ons",
        "Resequence Options",
        "Paycodes",
        "VRU Configuration"
    ])
    
    with tab1:
        render_roster_preferences()
        
    with tab2:
        render_callout_options()
        
    with tab3:
        render_arcos_addons()
        
    with tab4:
        render_resequence_options()
        
    with tab5:
        render_paycodes()
        
    with tab6:
        render_vru_configuration()
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    styled_header("Need Help?", "section")
    
    help_topic = st.selectbox(
        "Select topic for help",
        ["Roster Administration", "Callout Behavior", "ARCOS Add-Ons", 
         "Resequencing Options", "Paycodes", "VRU Configuration"]
    )
    
    if st.button("Get Help"):
        help_response = get_contextual_help(help_topic, "Global Configuration Options")
        st.info(help_response)

def render_roster_preferences():
    """Render the roster administration preferences section"""
    styled_header("Roster Administration Preferences", "section")
    
    st.markdown("""
    Configure how rosters are managed and sorted within ARCOS. These settings affect how
    employees are organized and selected during callouts.
    """)
    
    # Roster sorting methods
    sorting_method = st.selectbox(
        "Roster Sorting Method",
        ["Seniority", "Rotating", "Alphabetical", "Custom"],
        index=0,
        key="roster_sorting_method"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Roster_Sorting"] = sorting_method
    
    # Pointer-based progression
    use_pointer = st.checkbox(
        "Use pointer-based callout progression",
        value=True,
        help="When enabled, ARCOS tracks who was last called and resumes from that point",
        key="use_pointer"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Use_Pointer"] = "Yes" if use_pointer else "No"
    
    # Exclusive rosters
    use_exclusive_rosters = st.checkbox(
        "Implement exclusive rosters that take precedence over others",
        value=False,
        help="When enabled, certain rosters will always be called before others",
        key="use_exclusive_rosters"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Exclusive_Rosters"] = "Yes" if use_exclusive_rosters else "No"
    
    # Additional roster preferences
    st.markdown("### Additional Roster Preferences")
    
    roster_prefs = st.multiselect(
        "Select additional roster preferences",
        ["Comment", "Mask", "NoAdd", "NoRemove", "NoUpdate", "DoNotReset"],
        default=[],
        help="Select preferences that apply to your roster administration",
        key="roster_prefs"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Roster_Preferences"] = ", ".join(roster_prefs)

def render_callout_options():
    """Render the callout options section"""
    styled_header("Callout Behavior Options", "section")
    
    st.markdown("""
    Configure global callout behavior options that apply across all callout types
    unless overridden by specific callout type settings.
    """)
    
    # Blast calling
    enable_blast = st.checkbox(
        "Enable blast calling for specific rosters",
        value=False,
        help="When enabled, ARCOS can call multiple employees simultaneously for faster response",
        key="enable_blast"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Blast_Calling"] = "Enabled" if enable_blast else "Disabled"
    
    # CTT handling
    ctt_method = st.selectbox(
        "Closest to the Trouble (CTT) Sorting Method",
        ["None", "Drive Time", "Straight Line", "Work Location", "Custom"],
        index=0,
        help="Method used to determine which employees are closest to the trouble location",
        key="ctt_method"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_CTT_Method"] = ctt_method
    
    # Overlap times
    overlap_minutes = st.number_input(
        "Default overlap time allowed at end of callouts (minutes)",
        min_value=0,
        max_value=120,
        value=30,
        step=5,
        help="How many minutes before the end of a shift an employee can be called out",
        key="overlap_minutes"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Overlap_Minutes"] = str(overlap_minutes)
    
    # Additional callout options
    st.markdown("### Additional Callout Options")
    
    callout_options = st.multiselect(
        "Select additional callout options",
        ["DNCA (Do Not Call Again)", "Default to Include All", "Override All Schedule Exceptions", "Allow Partial Fills"],
        default=[],
        help="Select additional global callout options",
        key="callout_options"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Additional_Callout_Options"] = ", ".join(callout_options)

def render_arcos_addons():
    """Render the ARCOS add-ons section"""
    styled_header("ARCOS Add-On Features", "section")
    
    st.markdown("""
    Mark which ARCOS add-on features are included in your contract.
    If you're unsure about which add-ons are included, please consult your ARCOS sales representative.
    """)
    
    # ARCOS Mobile
    mobile_enabled = st.checkbox(
        "ARCOS Mobile functionality",
        value=True,
        help="Allows employees to respond to callouts via mobile app",
        key="mobile_enabled"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_ARCOS_Mobile"] = "Enabled" if mobile_enabled else "Disabled"
    
    # Web & Inbound Callout Activations
    web_activations = st.checkbox(
        "Web & Inbound Callout Activations",
        value=True,
        help="Allows callouts to be initiated via web interface or inbound calls",
        key="web_activations"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Web_Activations"] = "Enabled" if web_activations else "Disabled"
    
    # Other add-ons
    st.markdown("### Other Add-On Features")
    
    other_addons = st.multiselect(
        "Select other add-on features included in your contract",
        ["Email Alerts", "Batched Reporting", "Closest to the Trouble (CTT)", 
         "Crew Management", "Vacation Management", "Mutual Aid", "Qualifications"],
        default=[],
        help="Select all add-on features included in your contract",
        key="other_addons"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Other_Addons"] = ", ".join(other_addons)

def render_resequence_options():
    """Render the resequence options section"""
    styled_header("Roster Resequencing Options", "section")
    
    st.markdown("""
    Configure how roster resequencing works in ARCOS. These settings control when rosters
    are updated and how changes are applied to future roster periods.
    """)
    
    # First effective switchover date
    switchover_date = st.date_input(
        "First effective switchover date",
        help="Date when the first roster resequencing should occur",
        key="switchover_date"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Switchover_Date"] = switchover_date.strftime("%m/%d/%Y")
    
    # Days between switchovers
    days_between = st.number_input(
        "Number of days between switchovers",
        min_value=1,
        max_value=365,
        value=7,
        step=1,
        help="How many days should elapse between roster switchovers",
        key="days_between"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Days_Between_Switchovers"] = str(days_between)
    
    # Apply changes to future rosters
    apply_to_future = st.checkbox(
        "Apply changes to a roster to future rosters",
        value=True,
        help="When enabled, changes made to the current roster will automatically apply to future roster periods",
        key="apply_to_future"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Apply_To_Future"] = "Yes" if apply_to_future else "No"
    
    # Number of future roster periods
    future_periods = st.number_input(
        "Number of future roster periods to maintain",
        min_value=1,
        max_value=52,
        value=13,
        step=1,
        help="How many future roster periods ARCOS should maintain",
        key="future_periods"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Future_Periods"] = str(future_periods)

def render_paycodes():
    """Render the paycodes section"""
    styled_header("Paycodes Configuration", "section")
    
    st.markdown("""
    Configure the paycodes used in ARCOS for tracking overtime and other work categories.
    These should align with the paycodes used in your payroll system.
    """)
    
    # Paycode fields
    st.markdown("### Overtime Tracking Paycodes")
    
    ot_paycode = st.text_input(
        "Overtime Paycode",
        value="OT",
        help="Paycode used for tracking overtime hours",
        key="ot_paycode"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_OT_Paycode"] = ot_paycode
    
    dt_paycode = st.text_input(
        "Double Time Paycode",
        value="DT",
        help="Paycode used for tracking double time hours",
        key="dt_paycode"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_DT_Paycode"] = dt_paycode
    
    # Additional paycodes
    st.markdown("### Additional Paycodes")
    
    st.markdown("""
    Enter any additional paycodes used in your organization for tracking different types of work.
    Format: One paycode per line with description (e.g., "ST - Straight Time")
    """)
    
    additional_paycodes = st.text_area(
        "Additional Paycodes",
        value="",
        height=150,
        help="Enter one paycode per line with description",
        key="additional_paycodes"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Additional_Paycodes"] = additional_paycodes

def render_vru_configuration():
    """Render the VRU configuration section"""
    styled_header("Voice Response Unit (VRU) Configuration", "section")
    
    st.markdown("""
    Configure settings for the Voice Response Unit (VRU) that handles telephone interactions
    with employees during callouts and when employees call in to update their status.
    """)
    
    # Maximum active devices
    max_devices = st.number_input(
        "Maximum number of devices an employee can have active at one time",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        help="How many contact devices (phone numbers) an employee can have active simultaneously",
        key="max_devices"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Max_Devices"] = str(max_devices)
    
    # Modifiable devices
    modifiable_devices = st.multiselect(
        "Which devices should employees be allowed to modify through the Inbound system?",
        ["Home Phone", "Cell Phone", "Pager", "Alternate Phone", "Temporary"],
        default=["Cell Phone", "Temporary"],
        help="Select which device types employees can modify via inbound calls",
        key="modifiable_devices"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Modifiable_Devices"] = ", ".join(modifiable_devices)
    
    # Maximum temporary numbers
    max_temp_numbers = st.number_input(
        "Maximum number of temporary numbers allowed per employee",
        min_value=0,
        max_value=5,
        value=1,
        step=1,
        help="How many temporary contact numbers an employee can register",
        key="max_temp_numbers"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_Max_Temp_Numbers"] = str(max_temp_numbers)
    
    # Additional VRU settings
    st.markdown("### Additional VRU Settings")
    
    vru_prompts = st.multiselect(
        "Configure additional VRU prompts and behaviors",
        ["Require PIN for all transactions", "Allow employees to check callout history", 
         "Enable spoken employee number confirmation", "Enable extended self-service options"],
        default=[],
        help="Select additional VRU configuration options",
        key="vru_prompts"
    )
    
    # Store in session state
    st.session_state.responses["Global_Configuration_Options_VRU_Prompts"] = ", ".join(vru_prompts)