from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

urlpatterns = [
    path('login/'
    , auth_views.LoginView.as_view(template_name="account/login.html", redirect_authenticated_user=True)
    , name="account-login"),
    path('register/', views.register, name="account-register"),
    path('logout/', auth_views.LogoutView.as_view(template_name = "account/logout.html"), 
    name="account-logout")

]   