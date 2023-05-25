from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pdf/', views.pdf, name='pdf'),
    path('tpdf/', views.tpdf, name='tpdf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('verify/', views.verify, name='verify'),
    path('tverify/', views.tverify, name='tverify'),
    path('profile', views.profile, name='profile')
]