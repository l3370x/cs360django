from django.db import models
from django import forms


class Quality(models.Model):
    def __unicode__(self):
        return self.quality
    quality = models.CharField(max_length=50)
    dog_id = models.ForeignKey('dog.Dog',editable=False)

