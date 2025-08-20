from django.contrib import admin
from .models import Deelnemer, Cursus # Importeer je modellen

# Registreer je modellen hier
admin.site.register(Deelnemer)
admin.site.register(Cursus)
