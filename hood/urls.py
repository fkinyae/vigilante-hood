from django.urls import path,include
from . import views


urlpatterns = [
    #path('', views.login_view, name='login'),
    path('',views.welcome, name='welcome'),
    path('signup/', views.usersignup, name='signup'),
    path('activate/<uidb64>/<token>/',views.activate_account, name='activate'),
    path('registration/', include('django_registration.backends.activation.urls')),
    path('registration/', include('django.contrib.auth.urls')),
    
]