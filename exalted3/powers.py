

class ExPower(object):

    def __init__(self, powerset, model):
        self.owner = powerset
        self.model = model
        self.name = model.key

    def __str__(self):
        return self.name

class PowerSet(object):
    use = ExPower

    def __init__(self, owner, id, name):
        self.owner = owner
        self.id = id
        self.name = name
        self.model, created = CharmSet.objects.get_or_create(category_id=owner.category_id, sub_id=id)

        self.charms = [self.use(self, mod) for mod in self.model.charms.all()]

    def add(self, creator, name=None):
        if not name:
            raise ValueError("What should it be called?")

    def __repr__(self):
        return '<%s PowerSet: %s>' % (self.owner, self.name)


class CharmManager(object):
    category_id = 0
    use = PowerSet
    choice_init = {}

    def __init__(self, data):
        self.data = data
        self.choices = list()
        self.choices_dict = dict()
        for k, v in self.choice_init.iteritems():
            p = self.use(self, k, v)
            self.choices.append(p)
            self.choices_dict[p.id] = p

    def __str__(self):
        return self.name


class SolarCharm(CharmManager):
    category_id = 1
    name = 'Solar'
    choice_init = {1: 'Archery', 2: 'Athletics', 3: 'Awareness', 4: 'Brawl', 5: 'Bureaucracy', 6: 'Craft', 7: 'Dodge',
                   8: 'Integrity', 9: 'Investigation', 10: 'Larceny', 11: 'Linguistics', 12: 'Lore', 13: 'Medicine',
                   14: 'Melee', 15: 'Occult', 16: 'Performance', 17: 'Presence', 18: 'Resistance', 19: 'Ride',
                   20: 'Sail', 21: 'Socialize', 22: 'Stealth', 23: 'Survival', 24: 'Thrown', 25: 'War'}


class Sorcery(CharmManager):
    category_id = 100
    name = 'Sorcery'
    choice_init = {1: 'Terrestrial', 2: 'Celestial', 3: 'Solar'}


ALL_POWERSETS = (SolarCharm, Sorcery)