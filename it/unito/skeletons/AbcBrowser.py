from it.unito.skeletons import *


class AbcBrowser(metaclass=ABCMeta):

    def __init__(self, settings, logger, log_folder, maxsize=False, ghost=False):

        self._setting = settings
        self._maxsize = maxsize
        self._ghost = ghost
        self._driver = None

        self._define_browser()

        self._driver.implicitly_wait(3)

    def get_driver(self):
        return self._driver

    def get_settings(self):
        return self._setting

    def _define_browser(self):
        raise NotImplementedError("Function that Browser type has to implement")

    def quit(self):
        self._driver.close()

    def get_page(self, url):
        try:
            self._driver.get(url)
            time.sleep(0.5)
            self._current_url = url
            return True
        except Exception:
            return False

    def refresh(self):
        raise NotImplementedError('TO DO')

    def find_element(self, xpath):
        return self._driver.find_element_by_xpath(xpath)

    def find_elements(self, xpath):
        return self._driver.find_elements_by_xpath(xpath)

    def execute_script(self, item):
        self._driver.execute_script("arguments[0].scrollIntoView(true);", item)

    def wait_element(self, f):
        WebDriverWait(self._driver, 30).until(f)

    def get_current_url(self):
        return self._current_url

    def get_page_source(self):
        return self._driver.page_source
