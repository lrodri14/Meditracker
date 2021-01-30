"""
    This main_utilities.py file contains all the variable declarations and function for the main app to perform
    correctly.
"""
import requests
import random
from meditracker.settings import PAPERQUOTES_API_KEY


api_key = PAPERQUOTES_API_KEY
quote_tags = ['inspirational', 'knowledge', 'wisdom']
endpoint = 'http://api.paperquotes.com/apiv1/quotes?'
headers = {'Authorization': 'TOKEN {}'.format(api_key)}


def collect_quote():
    response = requests.get(endpoint, params={'tags': random.choice(quote_tags), 'limit': 100}, headers=headers).json()
    random_quote = random.choice(response['results'])
    quote = random_quote['quote']
    author = random_quote['author']
    if author is not None and author in quote:
        quote = quote.strip(author)
    return tuple([quote, author])
