from list.models import Item
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('User Info', {'fields': ['user']}),
        ('Date Info',         {'fields': ['created']}),
    ]
    readonly_fields = ("user",'created',)
    list_display = ('text', 'user','created')
    search_fields = ['text']
    list_filter = ['created']
    date_hierarchy = 'created'

admin.site.register(Item,ItemAdmin)
