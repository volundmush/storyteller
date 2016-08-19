from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.dispatch import receiver
from world.database.groups.models import Group, GroupPermissions
from evennia.utils.create import create_channel


@receiver(post_save, sender=Group)
def setup_group(sender, **kwargs):
    """
    This function is called whenever a new group is created. It's necessary to initialize all of the default settings!
    """

    if kwargs['created']:
        instance = kwargs['instance']
        if not GroupPermissions.objects.all():
            for entry in ['manage', 'moderate', 'gbadmin', 'ic', 'ooc', 'titleself', 'titleother']:
                GroupPermissions.objects.create(name=entry)
        rank_1_perms = ['manage', 'moderate', 'gbadmin', 'ic', 'ooc', 'titleself', 'titleother']
        rank_2_perms = rank_1_perms
        rank_3_perms = ['moderate', 'manage', 'ic', 'ooc']
        rank_4_perms = []
        rank_all_perms = ['ic', 'ooc']
        rank1 = instance.ranks.create(num=1,name="Leader")
        rank1.perms.add(*GroupPermissions.objects.filter(name__in=rank_1_perms))
        rank2 = instance.ranks.create(num=2,name="Second in Command")
        rank2.perms.add(*GroupPermissions.objects.filter(name__in=rank_2_perms))
        rank3 = instance.ranks.create(num=3,name="Officer")
        rank3.perms.add(*GroupPermissions.objects.filter(name__in=rank_3_perms))
        rank4 = instance.ranks.create(num=4,name="Member")
        instance.default_permissions.add(*GroupPermissions.objects.filter(name__in=rank_all_perms))
        instance.start_rank = rank4
        instance.alert_rank = rank3
        instance.ooc_channel = create_channel('group_%s_ooc' % instance.key, typeclass='typeclasses.channels.GroupOOC')
        instance.ooc_channel.init_locks(instance)
        instance.ic_channel = create_channel('group_%s_ic' % instance.key, typeclass='typeclasses.channels.GroupIC')
        instance.ic_channel.init_locks(instance)
        instance.save()