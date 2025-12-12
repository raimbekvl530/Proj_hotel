from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('panel/', views.admin_panel, name='panel'),
    path('profile/', views.profile_view, name='profile'),  # если нужно
]