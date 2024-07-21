from .models import Profile
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
                
                # create profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user.id)
                new_profile.save()
                return redirect("signup")
        else:
            messages.info(request, "Password must match!!")
            return redirect('signup')
            
    else:
        return render(request, 'signup.html')