import os
import time

from it.unito.browser.BrowserFactory import BrowserFactory
from it.unito.log.ClassLogger import ClassLog
from it.unito.operations import *


class Operator(object):

    def __init__(self, facet):

        self._facet = facet

        browser_facet = self._facet.get_browser()
        browser_facet['log_dir'] = os.path.join(facet.get_folder(), 'logs/browser_log.log')
        b_type = browser_facet['type']
        self._browser = BrowserFactory.get_browser(b_type, browser_facet, True, True)

        self._logger = ClassLog(self._facet.get_folder())

    def connect_to_web_page(self, url):
        self._logger.write_entering(str(__name__) + '/connect_to_web_page')
        out = self._browser.get_page(url)
        self._logger.write_exiting(str(__name__) + '/connect_to_web_page')
        return out

    def quit(self):
        self._logger.write_entering(str(__name__) + '/quit')
        self._browser.quit()
        self._logger.write_exiting(str(__name__) + '/quit')

    def get_page_content(self):
        return self._browser.get_page_source()

    def next_page(self, current_item_index):

        self._logger.write_entering(str(__name__) + '/next_page')

        current_item = self._facet.get_items()[current_item_index]

        if "next" in current_item and current_item['next'] != "":
            elem_obj = self._browser.find_element(current_item['next'])
            self._browser.execute_script(elem_obj)
            self._logger.write_message(str(__name__) + '/next_page', "next found")
            time.sleep(0.2)
            elem_obj.click()
            self._logger.write_exiting(str(__name__) + '/next_page')
            return True
        self._logger.write_message(str(__name__) + '/next_page', "next not present")

        self._logger.write_exiting(str(__name__) + '/next_page')

        return False

    def acquire_urls(self, current_item_index):

        self._logger.write_entering(str(__name__) + '/acquire_urls')

        current_item = self._facet.get_items()[current_item_index]
        xpath = current_item['path']
        url = current_item['url']
        type = current_item['type']

        page_list = set()

        try:
            self._browser.wait_element(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self._logger.write_message(str(__name__) + '/acquire_urls', str(e))

        try:
            items = self._browser.find_elements(xpath)
            if items:
                for item in items:
                    try:
                        self._browser.execute_script(item)
                        time.sleep(0.2)
                        elem_obj = item.find_element_by_xpath(url)
                        url_acquired = elem_obj.get_attribute(type)
                        page_list.add(url_acquired)
                    except Exception as e:
                        self._logger.write_message(str(__name__) + '/acquire_urls', str(e))
        except Exception as e:
            self._logger.write_message(str(__name__) + '/acquire_urls', str(e))

        page_list = list(page_list)
        if len(page_list) == 0:
            self._logger.write_message(str(__name__) + '/acquire_urls', "no url found")

        self._logger.write_exiting(str(__name__) + '/acquire_urls')
        return page_list

    def extract_from_current_page(self, xpath, type):

        self._logger.write_entering(str(__name__) + '/extract_from_current_page')

        try:
            self._browser.wait_element(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            self._logger.write_message(str(__name__) + '/extract_from_current_page', str(e))

        item_list = []
        items = self._browser.find_elements(xpath)
        if items:
            for item in items:
                try:
                    self._browser.execute_script(item)
                    time.sleep(0.2)

                    if type == 'text':
                        elem_value = item.text
                    elif type in ['href', 'src']:
                        elem_value = item.get_attribute(type)
                    else:
                        raise ValueError('type %s not in [\'text\', \'href\', \'src\']' % type)

                    item_list.append(elem_value)

                except Exception as e:
                    self._logger.write_message(str(__name__) + '/extract_from_current_page', str(e))

        self._logger.write_exiting(str(__name__) + '/extract_from_current_page')

        return item_list
