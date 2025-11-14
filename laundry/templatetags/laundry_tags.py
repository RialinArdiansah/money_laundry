from django import template
import locale

register = template.Library()

@register.filter
def intcomma(value):
    """Format number with comma separators"""
    try:
        return locale.format_string("%d", int(value), grouping=True)
    except (ValueError, TypeError):
        return value

@register.filter
def currency(value):
    """Format currency in Indonesian Rupiah format"""
    try:
        formatted = locale.format_string("%d", int(value), grouping=True)
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return value