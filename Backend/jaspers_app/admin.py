from django.contrib import admin
from django.utils.html import format_html # Nodig voor hyperlinks
from django.urls import reverse # Nodig voor het genereren van URLs
from .models import Deelnemer, Cursus

# Inline voor Deelnemer om weer te geven binnen Cursus admin
class DeelnemerInline(admin.TabularInline):
    """
    Toont een lijst van deelnemers die gekoppeld zijn aan een specifieke cursus.
    """
    model = Deelnemer
    extra = 0 # Geen extra lege formulieren tonen voor nieuwe deelnemers standaard
    
    # Definieer expliciet de kolommen die getoond moeten worden in de inline tabel.
    # 'get_deelnemer_link' zal de eerste kolom zijn en de klikbare naam.
    # 'email' is de tweede kolom.
    fields = ('get_deelnemer_link', 'email') # <-- Deze regel is de sleutel!
    
    # Deze velden moeten ook alleen-lezen zijn in de inline.
    readonly_fields = ('get_deelnemer_link', 'email') # <-- Maak deze kolommen alleen-lezen
    
    def get_deelnemer_link(self, obj):
        """
        Retourneert de volledige naam van de deelnemer als een klikbare hyperlink
        naar zijn/haar admin detailpagina.
        Deze methode is nu verplaatst naar DeelnemerInline.
        """
        if obj.pk: # Controleer of het object al is opgeslagen
            # Bouw de URL naar de wijzigingspagina van de deelnemer
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
            # Gebruik format_html om een veilige HTML-link te maken
            return format_html('<a href="{}">{}</a>', url, str(obj)) # str(obj) geeft de volledige naam
        return str(obj) # Als het object nieuw is, toon alleen de naam
    get_deelnemer_link.short_description = 'Deelnemer' # Label voor de kolomkop in de inline

# Admin klasse voor Cursus
class CursusAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Cursus model.
    """
    inlines = [DeelnemerInline] # Voeg de inline toe aan de Cursus admin detailpagina
    list_display = ('cursus', 'cursusdatum', 'refresher', 'geldigheid_jaren', 'geldigheid_datum') 
    save_on_top = True # Opslaan-knoppen bovenaan

# Admin klasse voor Deelnemer
class DeelnemerAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Deelnemer model.
    """
    # list_display voor de LIJSTWEERGAVE van Deelnemers (op de Deelnemers overzichtspagina)
    list_display = ('voornaam', 'tussenvoegsel', 'achternaam', 'email', 'get_cursus_display') 
    
    # fields voor de DETAILWEERGAVE (wijzigingsformulier van een deelnemer)
    fields = (
        'aanhef', 'voornaam', 'tussenvoegsel', 'achternaam',
        'bedrijfsnaam', 'email', 'geboortedatum', 'telefoonnummer',
        'windaId', 'notes',
        'cursus' # De ForeignKey 'cursus' wordt hier als een dropdown getoond
    )
    
    # Maak de ForeignKey 'cursus' alleen-lezen in de detailweergave.
    # Dit toont het als een niet-bewerkbare dropdown. Als je het als tekst wilt,
    # moet je hier 'get_cursus_display' toevoegen en 'cursus' verwijderen uit fields.
    readonly_fields = ('cursus',) 

    def get_cursus_display(self, obj):
        """
        Retourneert een hyperlink naar de gekoppelde cursus in de admin.
        Deze methode wordt gebruikt in de list_display van DeelnemerAdmin.
        """
        if obj.cursus:
            url = reverse('admin:%s_%s_change' % (obj.cursus._meta.app_label, obj.cursus._meta.model_name), args=[obj.cursus.pk])
            return format_html('<a href="{}">{}</a>', url, str(obj.cursus))
        return "Geen cursus gekoppeld"
    get_cursus_display.short_description = 'Afgeronde cursus(sen)' # Label voor de kolom/veld
    
# Registreer je modellen met hun Admin klassen
admin.site.register(Cursus, CursusAdmin)
admin.site.register(Deelnemer, DeelnemerAdmin)
