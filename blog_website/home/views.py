from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post

# Create your views here.
def home(request):
    allPosts = Post.objects.all()
    print(allPosts)
    context = {'allPosts': allPosts}
    return render(request,'home/home.html',context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, type(phone), content)

        if len(name)==2 or ('.com' not in email or '@' not in email) or (len(phone)<10 or not phone.isnumeric()) or len(content)<3:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'Your message has been successfully sent')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    allPosts = Post.objects.filter(title__icontains=query)
    params = {'allPosts':allPosts,'query':query} 
    return render(request,'home/search.html',params)