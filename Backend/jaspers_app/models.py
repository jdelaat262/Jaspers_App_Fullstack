from django.db import models

class Deelnemer(models.Model):
    aanhef = models.CharField(max_length=5, blank=True, null=True)
    voornaam = models.CharField(max_length=100, blank=True, null=True)
    tussenvoegsel = models.CharField(max_length=50, blank=True, null=True)
    achternaam = models.CharField(max_length=100, blank=True, null=True)
    bedrijfsnaam = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    geboortedatum = models.DateField(blank=True, null=True)
    refresher = models.BooleanField(default=False)
    cursus = models.CharField(max_length=200, blank=True, null=True)
    cursusdatum = models.DateField(blank=True, null=True)
    geldigheid_jaren = models.CharField(max_length=50, blank=True, null=True)
    geldigheid_datum = models.DateField(blank=True, null=True)
    windaId = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.voornaam}{' ' + self.tussenvoegsel if self.tussenvoegsel else ''} {self.achternaam}"