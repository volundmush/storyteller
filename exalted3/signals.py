from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.dispatch import receiver
from storyteller.exalted3.models import Persona, Stat


@receiver(post_save, sender=Persona)
def setup_stats(sender, **kwargs):
    """
    This function is called whenever a new group is created. It's necessary to initialize all of the default settings!
    """
    print "signal fired!"
    if kwargs['created']:
        Stat.objects.get_or_create(persona=kwargs['instance'])