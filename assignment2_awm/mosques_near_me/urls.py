
from django.urls import path
from django.views.generic import TemplateView

from mosques_near_me import views

app_name = "mosques_near_me"

urlpatterns = [

    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='login'),
    path('', TemplateView.as_view(template_name='index.html'), name="home"),

]