from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('mot/<int:mot_id>/', views.detail_mot, name='detail_mot'),
    path('jeux/', views.jeux, name='jeux'),
    path('profil/', views.profil, name='profil'),
    path('galerie/', views.galerie, name='galerie'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accueil'), name='logout'),
]