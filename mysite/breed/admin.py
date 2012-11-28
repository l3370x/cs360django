from breed.models import Breed
from django.contrib import admin

class BreedAdmin(admin.ModelAdmin):
    fieldsets = [
        ('breed', {'fields': ['breed']}),
        ('dog_id',         {'fields': ['dog_id']}),
    ]
    readonly_fields = ("dog_id",)
    list_display = ('breed', 'dog_id')

admin.site.register(Breed,BreedAdmin)
