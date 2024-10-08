from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Mot, UserProfile, Image
from django.db.models import Q
import random

def accueil(request):
    query = request.GET.get('q')
    if query:
        mots = Mot.objects.filter(Q(sig_mot_sar__icontains=query) | Q(mot_sar__icontains=query))
    else:
        mots = Mot.objects.all()
    return render(request, 'accueil.html', {'mots': mots})

def detail_mot(request, mot_id):
    mot = Mot.objects.get(id=mot_id)
    if request.user.is_authenticated:
        UserProfile.objects.get(user=request.user).mots_consultes.add(mot)
    return render(request, 'detail_mot.html', {'mot': mot})

@login_required
def jeux(request):
    mots = list(Mot.objects.all())
    mot_choisi = random.choice(mots)
    choix = random.sample(mots, min(4, len(mots)))
    if mot_choisi not in choix:
        choix[0] = mot_choisi
    random.shuffle(choix)
    
    if request.method == 'POST':
        reponse = request.POST.get('reponse')
        if reponse == mot_choisi.mot_sar:
            profile = UserProfile.objects.get(user=request.user)
            profile.score_jeux += 1
            profile.save()
            message = "Correct !"
        else:
            message = "Incorrect. La bonne réponse était : " + mot_choisi.mot_sar
        return render(request, 'jeux.html', {'mot': mot_choisi, 'choix': choix, 'message': message})
    
    return render(request, 'jeux.html', {'mot': mot_choisi, 'choix': choix})

@login_required
def profil(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profil.html', {'profile': profile})

@login_required
def galerie(request):
    if not request.user.is_staff:
        return redirect('accueil')
    images = Image.objects.all()
    return render(request, 'galerie.html', {'images': images})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('accueil')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})