from person.models import Person
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Info', {'fields': ['user']}),
        ('first name',         {'fields': ['first_name']}),
        ('last name',         {'fields': ['last_name']}),
        ('address',         {'fields': ['address']}),
        ('city',         {'fields': ['city']}),
        ('zipcode',         {'fields': ['zipcode']}),
        ('state',         {'fields': ['state']}),
        ('email',         {'fields': ['email']}),
        ('numDogs',         {'fields': ['numDogs']}),
    ]
    readonly_fields = ("user",'numDogs',)
    list_display = ('user', 'first_name','last_name',
                    'address','city','numDogs')

admin.site.register(Person,PersonAdmin)
