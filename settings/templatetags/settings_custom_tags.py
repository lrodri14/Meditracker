from django import template

register = template.Library()

@register.simple_tag
def current_url(key, value, urlencode):
    url = '?{}={}'.format(key, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != key, querystring)
        encoded_url = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_url)
    return url