from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.gis.geos import Point
from django.http import JsonResponse
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


def user_logout(request):
    logout(request)
    return redirect("/")


@login_required
def update_location(request):
    current_location = request.POST.get("userlocation", None)
    if not current_location:
        return JsonResponse({"message": "No location found."}, status=400)

    try:
        profile = request.user.userprofile

        if not profile:
            raise ValueError("Can't get user profile")

        coordinates = [float(coordinate) for coordinate in current_location.split(',')]
        profile.user_location = Point(coordinates, srid=4326)
        profile.save()

        update_msg = f'Update current location for {request.user.username} to {coordinates}'

        return JsonResponse({"message": update_msg}, status=200)
    except:
        return JsonResponse({"Error: ": "No Location found"}, status=400)