from django.db import models
from django import forms


class Breed(models.Model):
    def __unicode__(self):
        return self.breed
    breed = models.CharField(max_length=50)
    dog_id = models.ForeignKey('dog.Dog',editable=False)



