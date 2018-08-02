from model.product import Product
import jsonpickle
import os.path


class JsonFixtures:
    def __init__(self, file):
        self.file = file


    def load_from_json(self):
        testdata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file)
        with open(testdata_file) as f:
            return jsonpickle.decode(f.read())


    def get_product_list(self, pattert = ''):
        list=[]
        products = self.load_from_json()

        for product in products:
            if pattert.lower() not in product['name'].lower() and pattert.lower() not in product['description'].lower():
                continue
            id, name, description, price, image = (product['id'], product['name'], product['description'], product['price'], product['image'])
            product_kwargs = dict(zip(['id', 'name', 'description', 'price', 'image'], [id, name, description, price, image]))
            list.append(Product(**product_kwargs))
        return list