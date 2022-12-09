from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .models import UserProfile
from .forms import RegisterUserForm
from django.shortcuts import render


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/menu")
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="user_registration/login.html", context={"login_form": form})


# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            form.save()
            new_profile = UserProfile(user=new_user, username=username, email=email)
            new_profile.save()
            return redirect("/register_success")
        else:
            return redirect("/")
    else:
        form = RegisterUserForm()
    return render(request=request, template_name="user_registration/register.html", context={"signup_form": form})
