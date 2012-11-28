from django.db import models
from django import forms

class Dog(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    birthday = models.DateField()
    up_for_adoption = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    foster_id = models.ForeignKey('person.Person',editable=False)

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog

from django.forms.models import inlineformset_factory
from breed.models import Breed
from qualities.models import Quality
from pictures.models import Picture

MAX_BREEDS = 10

BreedFormSet = inlineformset_factory(Dog, 
    Breed, 
    can_delete=False,
    extra=4,max_num=MAX_BREEDS)

MAX_QUALS = 20

QualityFormSet = inlineformset_factory(Dog, 
    Quality, 
    can_delete=False,
    extra=4,max_num=MAX_QUALS)

MAX_PICS = 30

PictureFormSet = inlineformset_factory(Dog, 
    Picture, 
    can_delete=False,
    extra=2,max_num=MAX_QUALS)

class UserSubmittedDogForm(forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('date_added', )
