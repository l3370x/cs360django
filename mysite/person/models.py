from django.db import models
from django.contrib.auth.models import User
from django import forms

from dog.models import *

class Person(models.Model):
    def __unicode__(self):
        return self.first_name
    def numDogs(self):
        return len(Dog.objects.filter(foster_id=Person.objects.get(user=self.user.id)))
    user = models.ForeignKey(User,editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=20)
    email = models.EmailField()

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)

class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zipcode = forms.IntegerField()
    state = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)
    confirm = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)
