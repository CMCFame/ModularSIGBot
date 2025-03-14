# ============================================================================
# ARCOS SIG Form Application - Tabs Package
# ============================================================================
# This file initializes the tabs package for the ARCOS SIG Form application.
# It imports and exports all tab-specific modules.
# ============================================================================

# Import tab modules
from app.tabs.location_hierarchy import render_form as location_hierarchy
from app.tabs.trouble_locations import render_form as trouble_locations
from app.tabs.job_classifications import render_form as job_classifications
from app.tabs.callout_reasons import render_form as callout_reasons
from app.tabs.event_types import render_form as event_types
from app.tabs.callout_type_config import render_form as callout_type_config
from app.tabs.global_config import render_form as global_config
from app.tabs.data_interfaces import render_form as data_interfaces
from app.tabs.additions import render_form as additions
from app.tabs.generic_tab import render_form as generic_tab

# Export all tab modules
__all__ = [
    'location_hierarchy',
    'trouble_locations',
    'job_classifications',
    'callout_reasons',
    'event_types',
    'callout_type_config',
    'global_config',
    'data_interfaces',
    'additions',
    'generic_tab'
]