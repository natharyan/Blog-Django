from django.shortcuts import render,HttpResponse

# Create your views here.
def blogHome(request):
    return HttpResponse("This is blogHome. We will keep all the blog posts here")

def blogPost(request, slug):
    return HttpResponse(f"This is blogPost: {slug}")