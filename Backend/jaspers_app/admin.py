from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Deelnemer, Cursus

# Inline voor Deelnemer om weer te geven binnen Cursus admin
class DeelnemerInline(admin.TabularInline):
    """
    Toont een lijst van deelnemers die gekoppeld zijn aan een specifieke cursus.
    """
    model = Deelnemer
    extra = 0 # Geen extra lege formulieren tonen voor nieuwe deelnemers standaard
    
    fields = ('get_full_name', 'email') 
    readonly_fields = ('get_full_name', 'email')

    def get_full_name(self, obj):
        """
        Deze methode haalt de volledige naam van de deelnemer op.
        """
        return str(obj) 
    get_full_name.short_description = 'Volledige Naam Deelnemer'

# Admin klasse voor Cursus
class CursusAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Cursus model.
    """
    inlines = [DeelnemerInline]
    list_display = ('cursus', 'cursusdatum', 'refresher', 'geldigheid_jaren', 'geldigheid_datum') 
    save_on_top = True # <-- Voeg deze regel toe om opslaan-knoppen bovenaan te tonen

# Admin klasse voor Deelnemer
class DeelnemerAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Deelnemer model.
    """
    list_display = ('voornaam', 'tussenvoegsel', 'achternaam', 'email', 'get_cursus_display') 
    
    fields = (
        'aanhef', 'voornaam', 'tussenvoegsel', 'achternaam',
        'bedrijfsnaam', 'email', 'geboortedatum', 'telefoonnummer',
        'windaId', 'notes',
        'get_cursus_display'
    )
    
    readonly_fields = ('get_cursus_display',)

    def get_cursus_display(self, obj):
        """
        Retourneert een hyperlink naar de gekoppelde cursus in de admin.
        """
        if obj.cursus:
            url = reverse('admin:%s_%s_change' % (obj.cursus._meta.app_label, obj.cursus._meta.model_name), args=[obj.cursus.pk])
            return format_html('<a href="{}">{}</a>', url, str(obj.cursus))
        return "Geen cursus gekoppeld"
    get_cursus_display.short_description = 'Afgeronde cursus(sen)'
    
# Registreer je modellen met hun Admin klassen
admin.site.register(Cursus, CursusAdmin)
admin.site.register(Deelnemer, DeelnemerAdmin)
