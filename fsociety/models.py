from django.db import models
import wikipedia
# Create your models here.
import requests

class Crops(models.Model):
    name=models.TextField(max_length=20,blank=False)
    maxtemp=models.IntegerField(blank=False)
    mintemp=models.IntegerField(blank=False)
    maxppt=models.IntegerField(blank=False)
    minppt=models.IntegerField(blank=False)
    photo_url=models.URLField(max_length=400,blank=True)
    def json(self):
        text=wikipedia.summary(self.name, sentences=4)
        text=text.strip()
        url=wikipedia.page(self.name).url
        try:
            photo=self.photo_url
        except:
            photo=''
        return ({
            "name":self.name,
            "maxtemp":self.maxtemp,
            "mintemp":self.mintemp,
            "maxppt":self.maxppt,
            "minppt":self.minppt,
            "wikipedia":text,
            "wikipedia_url":url,
            "photo_url":photo,
        })

    def __str__(self):
        return (self.name)