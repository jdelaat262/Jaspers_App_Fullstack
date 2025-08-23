from django.db import models

class Cursus(models.Model):
    """
    Dit model bewaart de gegevens van een cursus.
    """
    cursus = models.CharField(max_length=200, blank=True, null=True)
    cursusdatum = models.DateField(blank=True, null=True)
    refresher = models.BooleanField(default=False)
    geldigheid_jaren = models.CharField(max_length=50, blank=True, null=True)
    geldigheid_datum = models.DateField(blank=True, null=True)

    # NIEUW: De ManyToManyField toevoegen
    deelnemers = models.ManyToManyField(
        'Deelnemer', # Verwijst naar het Deelnemer model
        related_name='cursussen', # Aangepast naar 'cursussen'
        blank=True # Een cursus kan aangemaakt worden zonder direct deelnemers te hebben
    )

    class Meta:
        verbose_name_plural = "Cursussen"

    def __str__(self):
        return f"{self.cursus} op {self.cursusdatum}"

class Deelnemer(models.Model):
    """
    Dit model bewaart de persoonsgegevens van een deelnemer.
    """
    # VERWIJDERD: De ForeignKey naar Cursus.

    aanhef = models.CharField(max_length=5, blank=True, null=True)
    voornaam = models.CharField(max_length=100, blank=True, null=True)
    tussenvoegsel = models.CharField(max_length=50, blank=True, null=True)
    achternaam = models.CharField(max_length=100, blank=True, null=True)
    bedrijfsnaam = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    geboortedatum = models.DateField(blank=True, null=True)
    telefoonnummer = models.CharField(max_length=20, blank=True, null=True)
    windaId = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        # De twee Meta-klassen zijn samengevoegd in één
        verbose_name_plural = "Deelnemers"
        constraints = [
            models.UniqueConstraint(
                fields=['voornaam', 'achternaam', 'geboortedatum'],
                name='unieke_deelnemer_constraint'
            )
        ]

    def __str__(self):
        return f"{self.voornaam}{' ' + self.tussenvoegsel if self.tussenvoegsel else ''} {self.achternaam}"