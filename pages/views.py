from django.shortcuts import render
from infos.models import Info

# Create your views here.
def index(request):
    
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')