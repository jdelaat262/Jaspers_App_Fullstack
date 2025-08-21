from django.contrib import admin
from django.utils.html import format_html # Importeer format_html
from django.urls import reverse # Importeer reverse
from .models import Deelnemer, Cursus

# Inline voor Deelnemer om weer te geven binnen Cursus admin
class DeelnemerInline(admin.TabularInline):
    """
    Toont een lijst van deelnemers die gekoppeld zijn aan een specifieke cursus.
    """
    model = Deelnemer # Dit is het model dat we in de inline willen zien
    extra = 0 # Geen extra lege formulieren tonen voor nieuwe deelnemers standaard
    
    # Velden die getoond moeten worden in de inline tabel
    # 'get_full_name' en 'email' zijn methoden of velden die we willen weergeven
    fields = ('get_full_name', 'email') 
    readonly_fields = ('get_full_name', 'email') # Maak ze alleen-lezen in deze weergave

    def get_full_name(self, obj):
        """
        Deze methode haalt de volledige naam van de deelnemer op.
        Het gebruikt de __str__ methode van het Deelnemer model.
        """
        return str(obj) 
    get_full_name.short_description = 'Volledige Naam Deelnemer' # Label voor de kolom in de admin

# Admin klasse voor Cursus
class CursusAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Cursus model.
    """
    inlines = [DeelnemerInline] # Voeg de inline toe aan de Cursus admin detailpagina
    # Velden die getoond moeten worden in de lijstweergave van Cursussen
    list_display = ('cursus', 'cursusdatum', 'refresher', 'geldigheid_jaren', 'geldigheid_datum') 

# Admin klasse voor Deelnemer (optioneel, maar goede praktijk om te definiëren)
class DeelnemerAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Deelnemer model.
    """
    # Velden die getoond moeten worden in de lijstweergave van Deelnemers
    list_display = ('voornaam', 'tussenvoegsel', 'achternaam', 'email', 'get_cursus_display') # Gebruik de custom methode hier
    
    # Velden die getoond moeten worden in de detailweergave (wijzigingsformulier)
    # De 'cursus' zelf wordt ook getoond, maar 'get_cursus_display' wordt gebruikt voor de tekstweergave
    fields = (
        'aanhef', 'voornaam', 'tussenvoegsel', 'achternaam',
        'bedrijfsnaam', 'email', 'geboortedatum', 'telefoonnummer',
        'windaId', 'notes',
        'get_cursus_display' # Toon de cursus als tekst
    )
    
    # Maak de custom weergave van de cursus alleen-lezen
    readonly_fields = ('get_cursus_display',)

    def get_cursus_display(self, obj):
        """
        Retourneert een hyperlink naar de gekoppelde cursus in de admin.
        """
        if obj.cursus:
            # Genereer de URL naar de admin detailpagina van de gekoppelde cursus
            url = reverse('admin:%s_%s_change' % (obj.cursus._meta.app_label, obj.cursus._meta.model_name), args=[obj.cursus.pk])
            # Gebruik format_html om een veilige HTML-hyperlink te maken
            return format_html('<a href="{}">{}</a>', url, str(obj.cursus))
        return "Geen cursus gekoppeld"
    get_cursus_display.short_description = 'Afgeronde cursus(sen)' # Nieuw label
    
# Registreer je modellen met hun Admin klassen
admin.site.register(Cursus, CursusAdmin)
admin.site.register(Deelnemer, DeelnemerAdmin)
