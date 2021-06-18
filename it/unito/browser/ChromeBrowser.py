from it.unito.browser import *
from it.unito.skeletons.AbcBrowser import AbcBrowser


class ChromeBrowser(AbcBrowser):

    def __init__(self, settings, maxsize=False, ghost=False):

        super().__init__(settings, maxsize, ghost)

    def _define_browser(self):

        self._capabilities = dict(DesiredCapabilities.CHROME)
        self._profile = webdriver.ChromeOptions()
        self._profile.add_argument('--no-sandbox')

        if self._ghost:
            self._profile.headless = True

        try:

            if self._setting["header"] and self._setting["header"] != "":
                self._profile.add_argument(f'--user-agent={self._setting["header"]}')

            self._driver = webdriver.Chrome(desired_capabilities=self._capabilities, chrome_options=self._profile,
                                            executable_path=self._setting['driver'],
                                            service_log_path=self._setting['log_dir'])

        except:

            self._driver = webdriver.Chrome(executable_path=self._setting['driver'],
                                            chrome_options=self._profile)

        if self._maxsize:
            self._driver.maximize_window()
