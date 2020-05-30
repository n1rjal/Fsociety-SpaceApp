from django.db import models
import wikipedia
# Create your models here.
class Crops(models.Model):
    name=models.TextField(max_length=20,blank=False)
    maxtemp=models.IntegerField(blank=False)
    mintemp=models.IntegerField(blank=False)
    maxppt=models.IntegerField(blank=False)
    minppt=models.IntegerField(blank=False)

    def json(self):
        try:
            text=wikipedia.summary(self.name, sentences=4)
            text=text.strip()
            url=wikipedia.page(self.name).url
        except:
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
        })

    def __str__(self):
        return (self.name)