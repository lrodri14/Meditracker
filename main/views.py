from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    template = 'main/main.html'
    return render(request, template, {})
