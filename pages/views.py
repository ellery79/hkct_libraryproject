from django.shortcuts import render
from infos.models import Info

# Create your views here.
def index(request):
    info_query = Info.objects.all()
    context = {
        'info_query': info_query,
    }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')