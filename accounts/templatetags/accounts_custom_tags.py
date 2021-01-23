from django import template

register = template.Library()

@register.simple_tag
def get_destination(chat_instance, user):
    return chat_instance.get_destination(user)
