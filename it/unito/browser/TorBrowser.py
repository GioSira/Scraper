from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from it.unito.browser import *
from it.unito.skeletons.AbcBrowser import AbcBrowser


class TorBrowser(AbcBrowser):

    def __init__(self, settings, maxsize=False, ghost=False):

        super().__init__(settings, maxsize, ghost)

    def _define_browser(self):

        self._capabilities = DesiredCapabilities.FIREFOX
        self._capabilities['marionette'] = True
        self._profile = webdriver.FirefoxOptions()

        # if self._ghost:
        #    self._profile.headless = True

        try:

            if self._setting["header"] and self._setting["header"] != "":
                self._profile.add_argument(f'--user-agent={self._setting["header"]}')

            if self._setting["firefox_binary"] and self._setting["firefox_binary"] != "":
                self._firefox_binary = FirefoxBinary(self._setting["firefox_binary"])

            self._driver = webdriver.Firefox(capabilities=self._capabilities, options=self._profile,
                                             executable_path=self._setting['geckodriver'],
                                             firefox_binary=self._firefox_binary,
                                             service_log_path=self._setting['log_dir'])

        except Exception as e:

            self._driver = webdriver.Firefox(firefox_profile=self._profile,
                                             executable_path=self._setting['geckodriver'])

        if self._maxsize:
            self._driver.maximize_window()
