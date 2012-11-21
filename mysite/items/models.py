from django.db import models

class Item(models.Model):
    text = models.CharField('Text',max_length=200)
    created = models.DateTimeField('Date Created',auto_now_add=True)

