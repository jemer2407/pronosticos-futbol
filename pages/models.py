from django.db import models

# Create your models here.

class Page(models.Model):
    
    title = models.CharField(verbose_name='Título', max_length=200)
    content = models.TextField(verbose_name='Contenido')
    # añadimos el campo order para que nuestro cliente pueda
    # ordernar las paginas como quiera
    order = models.SmallIntegerField(verbose_name='Orden', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')   # se crea automaticamente la primera vez que se crea el registro
    updated = models.DateTimeField(auto_now=True, verbose_name='Editado el')   # se actualiza cada vez que se edita un campo del registro

    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'
        ordering = ['order','title']
    
    def __str__(self):
        return self.title