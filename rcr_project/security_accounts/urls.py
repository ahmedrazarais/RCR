
from django.urls import path,include
from . import views

urlpatterns = [
 
    path("signup/<str:user_type>/" , views.signup_home , name="accounts_signup"),
    path("login/<str:user_type>/" , views.login_home , name="accounts_login"),
    path("profile/" , views.accounts_setting_home , name="accounts_profile"),
    path("recovery/<str:update_type>/" , views.recovery_view , name="accounts_recovery"),
    path("set_new_email/" , views.set_new_email_view , name="accounts_set_new_email"),
    path("set_new_password/" , views.set_new_password_view , name="accounts_set_new_password"),

    path("logout_account/" , views.logout , name="accounts_logout"),
   

    
]


