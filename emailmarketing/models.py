from django.db import models

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(max_length=100, verbose_name='Email')

    class Meta:
        verbose_name = 'Suscriptor'
        verbose_name_plural = 'Suscriptores'
        ordering = ['email']
        
    
    def __str__(self):
        return self.name