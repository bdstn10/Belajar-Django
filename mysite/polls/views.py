from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World, This Is My First Django App")


