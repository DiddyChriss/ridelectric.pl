from django.db import models


class ContactModels(models.Model):                  #creating of data in models
    name = models.CharField(max_length=200)
    surname = models.CharField(blank=True, max_length=200)
    company = models.CharField(blank=True, max_length=200)
    date = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=200)
    question = models.TextField()
    confirmation = models.BooleanField(null=True)

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self, *args, **kwargs):
        return (self.name)                        #show database form models as a name not "search object (id=nr)"


