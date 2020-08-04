import pytest
from fixture.application import Application

fixture = None


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default="firefox", help="Choose browser: chrome or firefox")


@pytest.fixture(scope="function")
def app(request):
    global fixture
    browser = request.config.getoption("browser")
    fixture = Application(browser=browser, url="https://privnote.com/")
    return fixture


@pytest.fixture(scope="function", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


