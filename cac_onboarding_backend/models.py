from django.db import models

class User(models.Model):
    username = models.CharField(max_length=25)
    email_address = models.EmailField(max_length= 150)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username