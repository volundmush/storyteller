from __future__ import unicode_literals
from storyteller.models import Game
from storyteller.base.stats import Stat, CharacterStat
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match


class Attribute(Stat):
    category = 'Attribute'
    default = 1
    load_default = True


class PhysicalAttribute(Attribute):
    sub_category = 'Physical'


class SocialAttribute(Attribute):
    sub_category = 'Social'


class MentalAttribute(Attribute):
    sub_category = 'Mental'


class Skill(Stat):
    category = 'Skill'
    default = 0
    can_specialize = True


class PhysicalSkill(Skill):
    sub_category = 'Physical'


class SocialSkill(Skill):
    sub_category = 'Social'


class MentalSkill(Skill):
    sub_category = 'Mental'


class Advantage(Stat):
    category = 'Advantage'


class PowerStat(Advantage):
    id = 1
    name = 'PowerStat'
    default = 1
    load_default = True


class CharacterWillpowerStat(CharacterStat):

    def load(self):
        if self.rating == 99:
            self.rating = self.handler.template.template.willpower
            self.save()

class Willpower(Advantage):
    id = 2
    name = 'Willpower'
    use = CharacterWillpowerStat
    load_default = True
    default = 99




class GameData(object):
    load_stats = None
    load_x = None
    load_y = None
    load_z = None
    load_custom = None
    load_merits = None
    load_pools = None
    load_templates = None
    load_sheet = None

    def __init__(self, gamename):
        self.game, created = Game.objects.get_or_create(key=gamename)

        for prep in (self.prepare_stats, self.prepare_x, self.prepare_y, self.prepare_z,
                     self.prepare_custom, self.prepare_merits, self.prepare_pools, self.prepare_templates):
            prep()

    def prepare_stats(self):
        self.stats = [stat(self) for stat in self.load_stats]
        self.stats_dict = {stat.id: stat for stat in self.stats}
        self.stats_name = {stat.name: stat for stat in self.stats}

    def prepare_x(self):
        self.x_splats = [Spl(self) for Spl in self.load_x]
        self.x_splats_dict = {spl.id: spl for spl in self.x_splats}

    def prepare_y(self):
        self.y_splats = ()
        self.y_splats_dict = {}

    def prepare_z(self):
        self.z_splats = ()
        self.z_splats_dict = {}

    def prepare_custom(self):
        pass

    def prepare_merits(self):
        pass

    def prepare_pools(self):
        self.pools = [pool() for pool in self.load_pools]
        self.pools_dict = {pool.id: pool for pool in self.pools}

    def prepare_templates(self):
        self.templates = [tem(self) for tem in self.load_templates]
        self.templates_dict = {tem.id: tem for tem in self.templates}