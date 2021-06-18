import glob
import json

from it.unito.log import *
from it.unito.log.ClassLogger import ClassLog


class UrlsLog(object):
    instance = None

    def __init__(self, facet_name, mainfolder, delete):

        if UrlsLog.instance is None:
            UrlsLog.instance = UrlsLog.__Log(facet_name, mainfolder, delete)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Log(object):

        def __init__(self, facet_name, mainfolder, delete):

            self.name = facet_name

            self.dir = os.path.join(mainfolder, 'logs')
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)

            self.file_name = f'urls_log.json'
            self.file_path = os.path.join(self.dir, self.file_name)

            self.writer = WriterFactory.get_writer("JSON", self.dir, {'append': False})
            self.logger = ClassLog(mainfolder)

            self.flag, self.level, self.urls = self._search_urls_log(delete)

        def _search_urls_log(self, delete):
            self.logger.write_entering(str(__name__) + "/search_urls_log")

            level = 0
            urls = []
            flag = False

            if not delete:

                query = os.path.join(self.dir, '*.json')
                for filename in glob.glob(query, recursive=True):
                    name, level, urls = self.read_urls(os.path.join(self.dir, filename))
                    if name == self.name:
                        flag = True
                        self.logger.write_message(str(__name__) + "/search_urls_log", f"file with name {name} found")
                        break

            self.logger.write_exiting(str(__name__) + "/search_urls_log")

            return flag, level, urls

        def read_urls(self, filename):
            self.logger.write_entering(str(__name__) + "/read_urls")

            with open(filename, 'r') as reader:
                data = json.load(reader)
                self.logger.write_message(str(__name__) + "/read_urls", f"loaded json file")

            self.logger.write_exiting(str(__name__) + "/read_urls")

            return data['name'], data['level'], data['urls']

    def _delete_file(self):
        self.logger.write_entering(str(__name__) + "/delete_file")
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            self.logger.write_message(str(__name__) + "/delete_file", f"urls_log with name {self.name} deleted")
        self.logger.write_exiting(str(__name__) + "/delete_file")

    def write_urls(self, level, urls_list):

        self.logger.write_entering(str(__name__) + "/write_urls")

        self._delete_file()

        data_to_write = {
            'name': self.name,
            'level': level,
            'urls': urls_list
        }

        self.logger.write_message(str(__name__) + "/write_urls",
                                  f"writing file with name {self.name} and level {level}. "
                                  f"It contains {len(urls_list)} urls")
        self.writer.write(self.file_name, data_to_write)
        self.logger.write_exiting(str(__name__) + "/write_urls")

    def get_flag(self):
        return self.flag

    def get_urls(self):
        return self.urls

    def get_level(self):
        return self.level
