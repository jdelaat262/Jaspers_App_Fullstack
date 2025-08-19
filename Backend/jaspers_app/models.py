from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    
    # De __str__ methode geeft een leesbare naam
    # van de objecten in de Django Admin
    def __str__(self):
        return self.name
