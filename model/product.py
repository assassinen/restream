from sys import maxsize

class Product:

    # paramentr = {'id': None, 'name': None, 'description': None, 'price': None, 'image': None}
    # @classmethod
    # def get_price(cls):
    #     return float(cls.paramentr['price'])

    def __init__(self, **kwargs):
        self.paramentr = {'id': None, 'name': None, 'description': None, 'price': None, 'image': None}
        for key, item in kwargs.items():
            self.paramentr[key] = str(item)


    def __eq__(self, other):
        return (self.paramentr['id'] is None or other.paramentr['id'] is None or self.paramentr['id'] == other.paramentr['id']) \
               and self.paramentr['name'] == other.paramentr['name'] \
               and self.paramentr['description'] == other.paramentr['description'] \
               and self.paramentr['price'] == other.paramentr['price']


    def __repr__(self):
        return '{} - price: ${}'.format(self.paramentr['name'], self.paramentr['price'])


    def id_or_max(self):
        if self.paramentr['id']:
            return int(self.paramentr['id'])
        else:
            return maxsize

    def get_name(self):
        return self.paramentr['name']

    def get_price(self):
        return self.paramentr['price']


    def price_or_max(self):
        if self.paramentr['price']:
            return self.paramentr['price']
        else:
            return maxsize

    # def __init__(self, id: None, name: None, description: None, price: None, image: None):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.image = image
    #
    #
    # def __repr__(self):
    #     return '{} - price: ${}'.format(self.name, self.price)
    #
    #
    # def __eq__(self, other):
    #     return (self.id is None or other.id is None or self.id == other.id) \
    #            and self.name == other.name \
    #            and self.description == other.description \
    #            and self.price == other.price \
    #            and self.image == other.image




