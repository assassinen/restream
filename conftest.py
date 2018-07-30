import pytest
from fixture.application import Application
from fixture.rest import Rest
import json
import os.path


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file:
            target = json.load(file)
    return target



@pytest.fixture(scope="session", autouse=True)
def rest(request):
    rest_config = load_config(request.config.getoption("--target"))['rest']
    rest_fixture = Rest(base_url=rest_config['baseUrl'], username=rest_config['user'], password=rest_config['pass'])
    return rest_fixture


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.login(username=web_config['user'], password=web_config['pass'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        if fixture is not None:
            fixture.session.logout()
            fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")