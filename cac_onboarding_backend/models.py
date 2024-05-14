from django.db import models

class User(models.Model):
    username = models.CharField(max_length=25)
    email_address = models.EmailField(max_length= 150)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username
    

class Location(models.Model):
    streetname = models.CharField(max_length=150)
    durationtime = models.IntegerField()
    importance = models.IntegerField()

    def __str__(self) :
        return self.streetname





