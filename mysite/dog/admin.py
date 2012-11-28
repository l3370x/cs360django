from dog.models import Dog
from django.contrib import admin

class DogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('name', {'fields': ['name']}),
        ('description',         {'fields': ['description']}),
        ('birthday',         {'fields': ['birthday']}),
        ('foster_id',         {'fields': ['foster_id']}),
        ('date_added',         {'fields': ['date_added']}),
    ]
    readonly_fields = ("foster_id",'date_added',)
    search_fields = ['name']

admin.site.register(Dog,DogAdmin)
