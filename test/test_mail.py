import time
import pytest
from model.product import Product


# 1) --------------------------------------------------------------

# product search without search parameter returns all products
def test_returns_all_product(rest, data_from_json):
    pattert = ''
    rest_products = rest.get_product_list(pattert)
    json_products = data_from_json.get_product_list(pattert)
    assert len(rest_products) == len(json_products)
    assert sorted(rest_products, key=Product.id_or_max) == sorted(json_products, key=Product.id_or_max)


# product search with one match returns found product
def test_returns_one_product(rest, data_from_json):
    pattert = 'OWASP Juice Shop Hoodie'
    rest_products = rest.get_product_list(pattert)
    json_products = data_from_json.get_product_list(pattert)
    assert len(rest_products) == 1
    assert len(rest_products) == len(json_products)
    assert sorted(rest_products, key=Product.id_or_max) == sorted(json_products, key=Product.id_or_max)


# product search with no matches returns no products
def test_returns_no_products(rest, data_from_json):
    pattert = 'no matcher'
    rest_products = rest.get_product_list(pattert)
    json_products = data_from_json.get_product_list(pattert)
    assert len(rest_products) == len(json_products)
    assert sorted(rest_products, key=Product.id_or_max) == sorted(json_products, key=Product.id_or_max)


@pytest.mark.skipif(True, reason="bug for characters: #, %, &, _, +")
def test_search_with_special_characters(rest, data_from_json, json_special_characters):
    pattert = json_special_characters['_']
    rest_products = rest.get_product_list(pattert)
    json_products = data_from_json.get_product_list(pattert)
    assert len(rest_products) == len(json_products)
    assert sorted(rest_products, key=Product.id_or_max) == sorted(json_products, key=Product.id_or_max)


def test_XSS_attack(rest):
    pattert = '<script>alert("XSS")</script>'
    status_code = rest.get_status_code(pattert)
    assert status_code == 200


def test_SQL_Injection(rest):
    pattert = "';'"
    status_code = rest.get_status_code(pattert)
    assert status_code == 500



# 2) --------------------------------------------------------------

@pytest.mark.skipif(True, reason="bug description for product: "
                                 "Quince Juice (1000ml), "
                                 "WASP SSL Advanced Forensic Tool (O-Saft), "
                                 "OWASP Node.js Goat," 
                                 "OWASP Juice Shop Sticker" )
def test_web_find(app, rest, json_all_product):
    pattert = json_all_product['name']
    app_products = app.product.get_product_list(pattert)
    rest_products = rest.get_product_list(pattert)

    assert len(app_products) == len(rest_products)
    assert sorted(app_products, key=Product.get_name) == sorted(rest_products, key=Product.get_name)



def test_web_find_error(app, rest):
    pattert = 'OWASP Node.js Goat'
    app_products = app.product.get_product_list(pattert)
    rest_products = rest.get_product_list(pattert)

    assert len(app_products) == len(rest_products)
    assert app_products[0].paramentr['description'] != rest_products[0].paramentr['description']



# 3) --------------------------------------------------------------

def test_find_product(rest):
    rest_products = rest.get_product_list()
    products = [product for product in sorted(rest_products, key=Product.get_price, reverse=True)[0:2]]
    # реализовать метод добаления products в корзину
    for product in products:
        rest.add_product(product)

    basket_products = [basket_product for basket_product in rest.get_basket_products()]

    assert len(products) == len(basket_products)
    assert sorted(products, key=Product.id_or_max) == sorted(basket_products, key=Product.id_or_max)
    for i in range(len(products)):
        assert sorted(products, key=Product.id_or_max)[i] == sorted(basket_products, key=Product.id_or_max)[i]

    # реализовать метод офистки корзины



# N) --------------------------------------------------------------
#
# def test_web_login(app):
#     time.sleep(3)
#     assert True
#
# def test_rest_login(rest):
#     time.sleep(3)
#     assert (rest.token != 0)
#
# def test_search(rest):
#     for i in rest.search():
#         print(i.keys())
#     assert (rest.token != 0)






