# jaspers_app/admin.py
from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from .models import Deelnemer, Cursus

# --- Inline definities om gekoppelde items te tonen ---

class DeelnemerInCursusInline(admin.TabularInline):
    model = Cursus.deelnemers.through
    extra = 0
    can_delete = False
    verbose_name = "Gekoppelde Deelnemer"
    verbose_name_plural = "Gekoppelde Deelnemers"
    
    fields = ('deelnemer', 'get_deelnemer_email', 'preview_certificaat_knop')
    readonly_fields = ('deelnemer', 'get_deelnemer_email', 'preview_certificaat_knop')
    
    def get_deelnemer_email(self, obj):
        return obj.deelnemer.email if obj.deelnemer else '-'
    get_deelnemer_email.short_description = 'E-mail'

    def preview_certificaat_knop(self, obj):
        try:
            url = reverse('preview-certificate-html', args=[obj.deelnemer.id, obj.cursus.id])
            return format_html('<a class="button" href="{}">Preview Certificaat</a>', url)
        except Exception:
            return "URL fout"
    preview_certificaat_knop.short_description = "Certificaat"


# Inline voor het tonen van CURSUSSEN op de DEELNEMER detailpagina
class CursusInDeelnemerInline(admin.TabularInline):
    model = Cursus.deelnemers.through
    extra = 1
    verbose_name = "Gekoppelde Cursus"
    verbose_name_plural = "Gekoppelde Cursussen"

    fields = ('cursus', 'get_cursus_datum')
    readonly_fields = ('get_cursus_datum',)

    def get_cursus_datum(self, obj):
        return obj.cursus.cursusdatum if obj.cursus else '-'
    get_cursus_datum.short_description = 'Datum'


# --- ModelAdmin voor Cursus ---

@admin.register(Cursus)
class CursusAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Cursus model.
    """
    list_display = ('cursus', 'cursusdatum', 'refresher', 'aantal_deelnemers')
    inlines = [DeelnemerInCursusInline]
    search_fields = ('cursus',)
    date_hierarchy = 'cursusdatum'
    exclude = ('deelnemers',)

    # Voeg een extra veld toe voor de knop in de admin.
    readonly_fields = ('custom_add_deelnemer_button',)
    fields = ('cursus', 'cursusdatum', 'refresher', 'custom_add_deelnemer_button')

    def custom_add_deelnemer_button(self, obj):
        url = reverse('admin:jaspers_app_deelnemer_add')
        return format_html('<a class="button" href="{}">Nieuwe Deelnemer Toevoegen</a>', url)
    custom_add_deelnemer_button.short_description = "Nieuwe Deelnemer"
    
    def aantal_deelnemers(self, obj):
        return obj.deelnemers.count()
    aantal_deelnemers.short_description = "Aantal Deelnemers"


# --- ModelAdmin voor Deelnemer ---

@admin.register(Deelnemer)
class DeelnemerAdmin(admin.ModelAdmin):
    """
    Admin configuratie voor het Deelnemer model.
    """
    list_display = ('__str__', 'email', 'bedrijfsnaam', 'aantal_gevolgde_cursussen')
    inlines = [CursusInDeelnemerInline]
    search_fields = ('voornaam', 'achternaam', 'email', 'bedrijfsnaam', 'windaId')
    list_filter = ('geboortedatum',)

    def aantal_gevolgde_cursussen(self, obj):
        return obj.cursussen.count()
    aantal_gevolgde_cursussen.short_description = "Aantal Cursussen"