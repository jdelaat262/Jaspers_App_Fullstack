from django.db import models

class Deelnemer(models.Model):
    aanhef = models.CharField(max_length=5, blank=True)
    voornaam = models.CharField(max_length=100)
    tussenvoegsel = models.CharField(max_length=50, blank=True)
    achternaam = models.CharField(max_length=100)
    bedrijfsnaam = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    geboortedatum = models.DateField(blank=True, null=True)
    refresher = models.BooleanField(default=False)
    cursus = models.CharField(max_length=200)
    cursusdatum = models.DateField()
    geldigheid = models.CharField(max_length=50) # Bijv. "1 jaar" of "custom"
    winda_id = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"