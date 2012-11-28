from pictures.models import Picture
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

class PicAdmin(AdminImageMixin, admin.ModelAdmin):
    fieldsets = [
        ('dog_id',         {'fields': ['dog_id']}),
        ('image',         {'fields': ['image']}),
        ('theImage',         {'fields': ['theImage']}),
    ]
    readonly_fields = ("dog_id",'theImage',)
    list_display = ('dog_id','image','theImage')

admin.site.register(Picture,PicAdmin)
