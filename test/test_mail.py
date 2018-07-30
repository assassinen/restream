import time

#
def test_web_login(app):
    time.sleep(3)
    assert True

def test_rest_login(rest):
    time.sleep(3)
    assert (rest.token != 0)

# def test_search(rest):
#     for i in rest.search()['data']:
#         print(i)
#     assert (rest.token != 0)


