from django.db import models

# Create your models here.

class Contact_models(models.Model):                  #creating of data in models
    name         = models.CharField(max_length=200)
    surname      = models.CharField(blank=True, max_length=200)
    company      = models.CharField(blank=True, max_length=200)
    date         = models.DateTimeField(auto_now=True)
    email        = models.EmailField(max_length=200)
    question     = models.TextField()
    confirmation = models.BooleanField(null=True)

    def __str__(self, *args, **kwargs):
        return (self.name)                        #show database form models as a name not "search object (id=nr)"


