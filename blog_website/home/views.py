from django.shortcuts import render,HttpResponse, redirect
from home.models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from blog.models import Post

# HTML Pages
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
        
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request,'Your message has been successfully sent')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>73:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsAuthor,allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found')
    params = {'allPosts':allPosts,'query':query} 
    return render(request,'home/search.html',params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check form submission
        if pass1 != pass2:
            messages.error(request,'Passwords do not match')
            return redirect('home') 
        else:
            # Create the user
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,'Your account has been successfully created')
            return redirect('home') 
    else:
        return HttpResponse('404 - Not Found')
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials, please try again')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return redirect('home')
