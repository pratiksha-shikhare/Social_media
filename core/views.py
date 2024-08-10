# from django.contrib.auth.models import User
# from django.contrib import messages, auth
# from django.shortcuts import redirect, render
from datetime import datetime
from .models import LikePost, Profile
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile, Post

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user= user_object)
    posts = Post.objects.all()
    return render(request, 'index.html', {"user_profile":user_profile, "posts":posts})

def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST.get("caption")
        
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect("/")
    else:
        return redirect("/")

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect("/")    
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect("/")
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    return render(request, "profile.html", {"user_profile":user_profile, "user_object":user_object, "user_posts":user_posts, "user_post_length":user_post_length})


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get("image") == None:
            image = user_profile.profileimg
            bio = request.POST.get("bio")
            location = request.POST.get("location")
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
            bio = request.POST.get("bio")
            location = request.POST.get("location")
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect("settings")

    return render(request, "settings.html", {"user_profile":user_profile})
    

def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        print(username, email, password, password2)
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                # log user in
                user_login = auth.authenticate(username=username, password=password)
                if user_login is not None:
                    auth.login(request, user_login)
                    
                    # create profile object
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect("settings")
                else:
                    messages.info(request, "Authentication failed")
                    return redirect('signup')
        else:
            messages.info(request, "Passwords must match!!")
            return redirect('signup')
    else:
        return render(request, 'signup.html')

# def signin(request):
#     if request.method == "POST":
#         print("Post is calling")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         print(username, password)
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             print("Loginis working")
#             # return redirect("/")
#             return render(request, "index.html")
#         else:
#             messages.info(request, "Credentials Invalid")
#             return redirect("signin.html")
#     else:
#         return render(request, "signin.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("signin")
    else:
        return render(request, "signin.html")


login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")

