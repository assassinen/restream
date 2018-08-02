import time
from model.product import Product

class ProductHelper:


    def __init__(self, app):
        self.app = app


    def get_product_list(self, pattert=''):
        wd = self.app.wd
        self.find_products(pattert)

        product_list = wd.find_element_by_css_selector("[class='table table-striped table-bordered table-condensed']").text.split('\n')
        product_count = len(product_list) // 3
        list = []
        for i in range(product_count):
            product_kwargs = dict(zip(['name', 'description', 'price'], product_list[3*i+1:3*i+4]))
            list.append(Product(**product_kwargs))
        return list


    def find_products(self, pattert=''):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_xpath("//html//body//nav//div//ul//li[4]//form//input").click()
        wd.find_element_by_xpath("//html//body//nav//div//ul//li[4]//form//input").clear()
        wd.find_element_by_xpath("//html//body//nav//div//ul//li[4]//form//input").send_keys(pattert)
        time.sleep(1)
        wd.find_element_by_id("searchButton").click()
        time.sleep(2)

