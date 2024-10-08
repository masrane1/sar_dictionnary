from django.db import models
from django.contrib.auth.models import User

class Mot(models.Model):
    mot_sar = models.CharField(max_length=100)
    sig_mot_sar = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    phr_sar = models.TextField()
    sig_phr_sar = models.TextField()

    def __str__(self):
        return self.mot_sar

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mots_consultes = models.ManyToManyField(Mot, related_name='consultations')
    score_jeux = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Image(models.Model):
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galerie/')
    legende = models.CharField(max_length=255)

    def __str__(self):
        return f"Image pour {self.mot.mot_sar}"