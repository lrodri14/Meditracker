"""
    This views.py file contains the views needed for the main app to work. It is composed of a single view: main -> This
    view is responsible for rendering the main page of the application.
"""

from django.shortcuts import render

# Create your views here.


def main(request):
    """
        DOCSTRING: This main view is used to render the main page of the application. It expects one single argument:
        request, which expects a request object.
    """
    template = 'main/main.html'
    return render(request, template, {})
