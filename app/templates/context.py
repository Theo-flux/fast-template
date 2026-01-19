"""Email template configuration"""

import datetime

EMAIL_COLORS = {
    # Brand colors
    "primary": "#2D8331",
    "secondary": "#6c757d",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    # Text colors
    "text_primary": "#2E2E2E",
    "text_secondary": "#666666",
    "text_muted": "#999999",
    "white": "#ffffff",
    # Background colors
    "bg_light": "#f8f9fa",
    "bg_white": "#ffffff",
    "bg_dark": "#343a40",
    # Border colors
    "border": "#dee2e6",
}

EMAIL_STYLES = {
    "button_padding": "12px 24px",
    "button_radius": "4px",
    "heading_size": "24px",
    "text_size": "14px",
    "year": datetime.datetime.now().year,
}

EMAIL_ASSETS = {}


def get_template_context(**kwargs):
    """Get base context for email templates"""
    return {**EMAIL_COLORS, **EMAIL_STYLES, **EMAIL_ASSETS, **kwargs}
