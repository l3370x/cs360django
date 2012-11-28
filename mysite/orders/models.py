from django.db import models
from django import forms

class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    credit_card = models.IntegerField()
    expiry_date = models.DateField()
    card_security_code = models.IntegerField()
    person_id = models.ForeignKey('person.Person')
    dog_id = models.ForeignKey('dog.Dog')


from django.contrib.admin.widgets import AdminDateWidget 


class OrdersForm(forms.Form):
    credit_card = forms.CharField(max_length=20)
    expiry_date = forms.DateField(widget = AdminDateWidget)
    card_security_code = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=3)

