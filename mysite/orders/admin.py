from orders.models import Orders
from django.contrib import admin

class OrdersAdmin(admin.ModelAdmin):
    fieldsets = [
        ('date', {'fields': ['date']}),
        ('credit card',         {'fields': ['credit_card']}),
        ('expiration',         {'fields': ['expiry_date']}),
        ('security code',         {'fields': ['card_security_code']}),
        ('person_id',         {'fields': ['person_id']}),
        ('dog_id',         {'fields': ['dog_id']}),
    ]
    readonly_fields = ("person_id",'date','dog_id',)
    list_filter = ['date']
    date_hierarchy = 'date'

admin.site.register(Orders,OrdersAdmin)



