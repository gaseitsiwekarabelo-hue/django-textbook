from django.http import HttpResponse

def hello_world(request):
    return HttpResponse(
        "<h1>hello_world App</h1>"
        "<p>Welcome to hello_world!</p>")

# Create your views here.
