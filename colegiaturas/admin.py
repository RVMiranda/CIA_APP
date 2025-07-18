from django.contrib import admin

# Register your models here.
from .models import Descuento, Recargo, Colegiatura

admin.site.register(Descuento)
admin.site.register(Recargo)
admin.site.register(Colegiatura)