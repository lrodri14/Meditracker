"""
    This views.py file contains the views needed for the main app to work. It is composed of a single view: main -> This
    view is responsible for rendering the main page of the application.
"""

from django.shortcuts import render
from utilities.main_utilities import collect_quote

# Create your views here.


def main(request):
    """
        DOCSTRING: This main view is used to render the main page of the application. It expects one single argument:
        request, which expects a request object.
    """
    template = 'main/main.html'
    quote, author = collect_quote()
    context = {'quote': quote, 'author': author}
    return render(request, template, context)
