from .models import Profile
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

# @login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    return render(request, "settings.html", {"user_profile":user_profile})
    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        # print(username, email, password, password2)
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username exists")
                return redirect('signup')
            else:
                user = User.objects.create(username=username, email=email, password=password)
                user.save()
                
                # log user
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                # create profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user.id)
                new_profile.save()
                return redirect("settings")
        else:
            messages.info(request, "Password must match!!")
            return redirect('signup')
            
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("signin.html")
    else:
        return render(request, "signin.html")

login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")

