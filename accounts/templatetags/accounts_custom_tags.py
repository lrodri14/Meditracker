"""
    This accounts_custom_tags.py file contains all the template tags needed to provide account app specific template
    functionality.
"""

from django import template

register = template.Library()

@register.simple_tag
def get_destination(chat_instance, user):
    """
        DOCSTRING:
        This get_destination template tag will return the value returned from calling a specific instance get_destination()
        method. It takes two obligatory parameters: chat_instance which expects a Chat class instance and user, which expects
        a CustomUser class instance.
    """
    return chat_instance.get_destination(user)
