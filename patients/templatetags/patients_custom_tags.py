"""
    DOCSTRING:
    This patients_custom_tags.py file contains the custom template tags that the appointments app needs
    to profile extra functionality in our template logic, it consists of a single custom tag.
"""

# Imports
from django import template

# Register needed to register our tags in our templates
register = template.Library()

# Decorator used to add extra functionality to our tag, this return a string.
@register.simple_tag
def current_url(key, value, urlencode=None):
    """
        DOCSTRING:
        This current_url function is used in our templates with the purpose of preventing filtering break
        whenever pagination is present in our templates, the default behavior with filtering is that whenever
        we click in our next page button, the filter will break and the server will return the filters cleared
        page, this function will solve this problem, following the next steps:
        1. Wait for the parameters values.
        2. Set the 'page' key-value pair, for this we will collect the key 'page' and the 'value' from the
        {{page.next_page_number}} or {{page.previous_page_number}} value.
        3. Set the url to '?key=value' for the page parameter.
        4. If the urlencode is present, then we will split the value by '&' to get the key-value parameters
        5. When the step 4 is done, we will filter the values and split them by the "=" symbol and return the values
           that are not the same as the key.
        6. Join all these values
        7. Format the querystring, with the key-value pair with the encoded url value.
        8. If the urlencode parameter is None, then the url will be returned with the 'page' key only.
    """

    url = '?{}={}'.format(key, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != key, querystring)
        encoded_url = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_url)

    return url