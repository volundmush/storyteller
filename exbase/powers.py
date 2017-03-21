

class Charm(object):
    id = 0
    name = 'None'
    cost = '--'
    mins = ''
    type = ''
    keywords = ('None',)
    duration = ''
    req_charms = 'None'
    req__ids = ()
    req_stats = {}
    tags = ()
    max_purchases = '1'

    def __init__(self, data):
        self.data = data
        for tag in self.tags:
            data.charm_tags[tag].register(self)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def purchase_check(self, buyer):
        pass
