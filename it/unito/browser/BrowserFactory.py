from it.unito.browser.BrowserType import BrowserType
from it.unito.browser.ChromeBrowser import ChromeBrowser
from it.unito.browser.FirefoxBrowser import FirefoxBrowser
from it.unito.browser.TorBrowser import TorBrowser


class BrowserFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get_browser(browserType, setting, maxsize, ghost):

        if BrowserType.CHROME.equals(browserType):
            return ChromeBrowser(settings=setting, maxsize=maxsize, ghost=ghost)
        elif BrowserType.FIREFOX.equals(browserType):
            return FirefoxBrowser(settings=setting, maxsize=maxsize, ghost=ghost)
        elif BrowserType.TOR.equals(browserType):
            return TorBrowser(settings=setting, maxsize=maxsize, ghost=ghost)
        else:
            raise ValueError('browser type %s not present in class BrowserType' % browserType)
