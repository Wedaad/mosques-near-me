
from django.urls import path
from django.views.generic import TemplateView

from mosques_near_me import views

app_name = "mosques_near_me"

urlpatterns = [

    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='login'),
    path('', TemplateView.as_view(template_name='index.html'), name="home"),
    path('logout/', TemplateView.as_view(template_name='user_registration/logout.html'), name='logout'),
    path('map/', TemplateView.as_view(template_name='view_map.html'), name='map'),
    path('menu/', TemplateView.as_view(template_name='user_menu.html'), name='menu'),
    path('update/', views.update_location, name="update_location"),
    path('findmosques/', views.find_mosque, name="findmosques"),
    path('addFavourites/', views.addFavouriteMosque, name="favouriteMosque"),
    path('profile/', views.getFavouriteMosque, name="profile")

]