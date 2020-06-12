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
        photo=self.photo_url
        try:
            text=wikipedia.summary(self.name, sentences=4)
            text=text.strip()
            url=wikipedia.page(self.name).url
            
        except:
            photo=''
            text=""
            url=""
            
        return ({
            "name":self.name,
            "maxtemp":self.maxtemp,
            "mintemp":self.mintemp,
            "maxppt":self.maxppt,
            "minppt":self.minppt,
            "wikipedia":text,
            "wikipedia_url":url,
            "photo_url":photo,
            "nutrient":"https://www.google.com/search?q=nutrient+in+"+str(self.name),
            "howto":"https://www.google.com/search?q=how+to+plant+"+str(self.name),
        })

    def __str__(self):
        return (self.name)