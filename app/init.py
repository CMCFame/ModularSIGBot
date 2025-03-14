# ============================================================================
# ARCOS SIG Form Application - Main Package
# ============================================================================
# This file initializes the main app package for the ARCOS SIG Form application.
# It imports and exports the main modules and establishes the package structure.
# ============================================================================

# Import main modules
from app.config import setup_page_config, ARCOS_RED, ARCOS_LIGHT_RED, ARCOS_GREEN, ARCOS_BLUE
from app.styles import load_css, styled_header, styled_expander, styled_info
from app.helpers import render_color_key, load_callout_reasons, load_sig_descriptions
from app.session_manager import initialize_session_state, get_current_tab, set_current_tab
from app.openai_client import get_openai_response, initialize_openai_client
from app.ai_assistant import render_ai_assistant, get_contextual_help

# Import tab modules (via tabs package)
from app.tabs import (
    location_hierarchy, trouble_locations, job_classifications,
    callout_reasons, event_types, callout_type_config,
    global_config, data_interfaces, additions, generic_tab
)

# Import exporter modules (via exporters package)
from app.exporters import export_to_csv, export_to_excel

# Export all modules
__all__ = [
    # Config
    'setup_page_config', 'ARCOS_RED', 'ARCOS_LIGHT_RED', 'ARCOS_GREEN', 'ARCOS_BLUE',
    
    # Styles
    'load_css', 'styled_header', 'styled_expander', 'styled_info',
    
    # Helpers
    'render_color_key', 'load_callout_reasons', 'load_sig_descriptions',
    
    # Session management
    'initialize_session_state', 'get_current_tab', 'set_current_tab',
    
    # OpenAI
    'get_openai_response', 'initialize_openai_client',
    
    # AI Assistant
    'render_ai_assistant', 'get_contextual_help',
    
    # Tabs
    'location_hierarchy', 'trouble_locations', 'job_classifications',
    'callout_reasons', 'event_types', 'callout_type_config',
    'global_config', 'data_interfaces', 'additions', 'generic_tab',
    
    # Exporters
    'export_to_csv', 'export_to_excel'
]