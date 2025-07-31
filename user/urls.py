from django.urls import path 
from django.views.decorators.csrf import csrf_exempt
from . import views 

urlpatterns = [
    path("",views.home_view,name='home'),
    path("login",views.login_page,name='login'),
    path("logout",csrf_exempt(views.logout_page),name='logout'),
    path("profile/", views.profile_view, name='profile'),
    path("signup/<int:user_type>/",views.signup_view,name='signup'),
    path("verify_mfa/", views.verify_mfa, name='verify_mfa'),
    path("disable-2fa/", views.disable_2fa, name='disable_2fa'),
    path("activate_mfa/", views.activate_mfa, name='activate_mfa'),
    path("privacy_policy/", views.privacy_policy, name='privacy_policy'), 
    path("account_delete_procedure/", views.account_delete_procedure, name='account_delete_procedure'),    
]