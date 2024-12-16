from django.shortcuts import render

# Create your views here.

def administrator(request):
    title = 'Panel de administrador'
    return render(request, 'administrator/administrator.html', {
        'title':title
    })