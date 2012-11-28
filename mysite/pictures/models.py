from django.db import models
from django import forms
from sorl.thumbnail import ImageField


class Picture(models.Model):
    def content_file_name(instance, filename):
        return '/'.join(['dogs', str(instance.dog_id.id), filename])
    dog_id = models.ForeignKey('dog.Dog',editable=False)
    image  = ImageField(upload_to=content_file_name)
    def theImage(self):
        return '/static/'+str(filename)



