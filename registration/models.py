from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profile/' + filename

# Create your models here.

# Modelo para el perfil de usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Imagen de perfil', upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(verbose_name='Biografía', null=True, blank=True)
    link = models.URLField(verbose_name='Enlace', max_length=200, null=True, blank=True)
    created = models.DateTimeField(verbose_name='Fecha creación perfil', auto_now_add=True)
    trial_month = models.DateTimeField(verbose_name='Fecha final de prueba', null=True, blank=True, validators=[MinValueValidator(timezone.now)])
    date_subscription = models.DateTimeField(verbose_name='Fecha suscripción', null=True, blank=True, validators=[MinValueValidator(timezone.now)])
    subscription_month = models.DateTimeField(verbose_name='Fecha final suscripción', null=True, blank=True, validators=[MinValueValidator(timezone.now)])
    is_trial = models.BooleanField(default=True)
    is_subscribed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['user__username']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
       Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Profile)
def update_profile_status(sender, instance, created, **kwargs):
    if created:
        # Calcular la fecha de finalización de la prueba
        instance.trial_month = timezone.now() + timezone.timedelta(minutes=20)
        instance.save()

@receiver(post_save, sender=Profile)
def check_trial_expiration(sender, instance, **kwargs):
    if instance.trial_month and instance.trial_month <= timezone.now():
        instance.is_trial = False
        instance.save()



@receiver(post_save, sender=Profile)
def check_subscription_expiration(sender, instance, **kwargs):
    # Esta señal verifica si la suscripción ha expirado
    if instance.subscription_month and instance.subscription_month <= timezone.now():
        instance.is_subscribed = False
        instance.save()