from django.shortcuts import render

# Create your views here.


def main(request):
    template = 'main/main.html'
    return render(request,template,{})
