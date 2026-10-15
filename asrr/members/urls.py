from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user),
    path('register/', views.register_user),
    path('profile/', views.profile),
    path('logout/', views.logout_user),
    path('sunnah/', views.sunnah_pref),
    path('csrf/', views.csrf_cookie)
]
