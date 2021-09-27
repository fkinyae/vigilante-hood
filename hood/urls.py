from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('',views.welcome, name='welcome'),
    path('signup/', views.usersignup, name='signup'),
    path('activate/<uidb64>/<token>/',views.activate_account, name='activate'),
    path('registration/', include('django_registration.backends.activation.urls')),
    path('registration/', include('django.contrib.auth.urls')),
    path('password_change/', views.PasswordsChangeView.as_view(), name='password_change'),
    path('profile/',views.view_profile, name='profile'),
    path('edit-profile/',views.edit_profile, name='edit-profile'),
    path('hood/', views.hood_view, name = 'hood'),
    path('all_businesses/<int:id>/', views.all_businesses, name = 'all_businesses'),
    path('business/<int:id>/', views.each_hood, name = 'business'),
    path('posts/<int:id>/', views.write_post, name = 'write_post'),
    path('all_posts/<int:id>/', views.all_posts, name = 'all_posts'),
    path('search/', views.search_hoods, name = 'search')

]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)