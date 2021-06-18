import time
from queue import Queue
from threading import Thread

from it.unito import *
from it.unito.scraper import *


class Scraper(object):

    def __init__(self, facet, threads, delete):

        self._facet = Facet(facet)

        self._main_folder = self._facet.get_folder()

        self._writer_data = self._facet.get_writer()
        writer_type = self._writer_data['type']
        writer_style = self._writer_data['style']
        self._writer = WriterFactory.get_writer(writer_type, self._main_folder, writer_style)

        self._logger = ClassLog(self._main_folder)
        self._url_saver = UrlsLog(self._facet.get_name(), self._main_folder, delete)

        self._item_queue = Queue()
        self._current_index = 0

        self._n_thread = threads
        self._extract_fields_queue = []

        self._fields = self._facet.get_fields_name()
        self._extracted_data = [[] for _ in range(len(self._fields))]

    def _watch_threads(self):

        self._logger.write_message(str(__name__) + "/watch_threads", "starting watch_threads")

        while True:
            time.sleep(60)

            for idx, t in enumerate(self._extract_fields_queue):
                if not t.is_alive():
                    self._logger.write_message(str(__name__) + "/watch_threads", f"thread {idx} dead. Restarting")
                    new_t = Thread(target=self._extract_fields)
                    self._extract_fields_queue[idx] = new_t
                    new_t.daemon = True
                    new_t.start()

    def extract_items(self):

        self._logger.write_entering(str(__name__) + "/extract_items")

        if not self._url_saver.get_flag():
            url = self._facet.get_url()
            self._item_queue.put(url)
        else:
            for url in self._url_saver.get_urls():
                self._item_queue.put(url)
            self._current_index = self._url_saver.get_level()

        items = self._facet.get_items()
        num_levels = len(items)

        for current_item_index in range(self._current_index, num_levels):
            self._logger.write_message(str(__name__) + "/extract_items", f"current level {current_item_index}")
            self._logger.write_message(str(__name__) + "/extract_items", "finding items")
            # estraggo le url dell'item corrente
            self._internal_extract_item(current_item_index)
            self._logger.write_message(str(__name__) + "/extract_items", "items found")

        # una volta uscito dal ciclo for, ho le url delle pagine da cui estrarre i campi
        self._logger.write_message(str(__name__) + "/extract_items", "extracting item fields")
        for _ in range(self._n_thread):
            self._logger.write_message(str(__name__) + "/extract_items", "starting new extract_fields thread")
            self._extract_fields_queue.append(Thread(target=self._extract_fields))
            self._extract_fields_queue[-1].daemon = True
            self._extract_fields_queue[-1].start()

        for idx in range(len(self._extract_fields_queue)):
            self._logger.write_message(str(__name__) + "/extract_items", f"wait thread {idx} to finish")
            self._extract_fields_queue[idx].join()  # aspetta che il thread sia terminato

        # self._watch_threads()

        self._logger.write_message(str(__name__) + "/extract_items", "item fields extracted")

        self._logger.write_message(str(__name__) + "/extract_items", "writing data")
        self._write_fields(self._extracted_data)
        self._logger.write_message(str(__name__) + "/extract_items", "data wrote")

        self._logger.write_exiting(str(__name__) + "/extract_items")

    def _internal_extract_item(self, index):

        # pre condizione: item_queue contiene la lista delle url
        # da cui estrarre l'item

        self._logger.write_entering(str(__name__) + "/_internal_extract_item")

        new_url_set = set()

        operator = Operator(self._facet)

        self._logger.write_message(str(__name__) + "/_internal_extract_item", "finding items")
        while not self._item_queue.empty():

            page = self._item_queue.get()

            try:

                # connettiti alla pagina corrente
                if not operator.connect_to_web_page(page):
                    raise Exception("cannot connect to %s" % page)
                self._logger.write_message(str(__name__) + "/_internal_extract_item", f"connected to page {str(page)}")

                next_page_flag = True
                while next_page_flag:
                    self._logger.write_message(str(__name__) + "/extract_items", "extracting items url")
                    urls = operator.acquire_urls(index)
                    self._logger.write_message(str(__name__) + "/extract_items", "items ur extracted")
                    # estrai le url dalla pagina corrente e mettile nel set
                    list(map(new_url_set.add, urls))
                    # vai alla prossima pagina
                    next_page_flag = operator.next_page(index)
                    if next_page_flag:
                        self._logger.write_message(str(__name__) + "/extract_items", "going to next page")

            except Exception as e:
                self._logger.write_message(str(__name__) + "/_internal_extract_item", str(e))

        # aggiungi le url estratte alla coda per il prossimo livello
        self._logger.write_message(str(__name__) + "/extract_items", "inserting urls into queue")
        new_url_set = list(new_url_set)
        self._url_saver.write_urls(index + 1, new_url_set)
        list(map(self._item_queue.put, new_url_set))
        self._logger.write_message(str(__name__) + "/extract_items", "urls inserted")

        # post condizione: item_queue contiene la lista delle url
        # per il prossimo item o per estrarre i campi
        self._logger.write_exiting(str(__name__) + "/_internal_extract_item")

        self._logger.write_message(str(__name__) + "/_internal_extract_item", "closing browser")
        # chiudi browser in quanto hai finito
        operator.quit()
        self._logger.write_message(str(__name__) + "/_internal_extract_item", "browser closed")

    def _extract_fields(self):

        self._logger.write_entering(str(__name__) + "/_extract_fields")

        # pre condizione: item_queue contiene la lista delle url
        # da cui estrarre i campi

        operator = Operator(self._facet)

        self._logger.write_message(str(__name__) + "/_extract_fields", "starting fields extraction")
        while not self._item_queue.empty():

            try:

                page = self._item_queue.get()
                if not operator.connect_to_web_page(page):
                    raise Exception("cannot connect to %s" % page)
                self._logger.write_message(str(__name__) + "/_extract_fields", f"accessed to page {str(page)}")

                for idx, field_name in enumerate(self._fields):
                    self._logger.write_message(str(__name__) + "/_extract_fields", f"extracting field {field_name}")
                    field = self._facet.get_field_parameters(field_name)
                    elements = operator.extract_from_current_page(field['path'], field['attribute'])
                    with lock:
                        self._extracted_data[idx] += elements
                    self._logger.write_message(str(__name__) + "/_extract_fields", f"field {field_name} extracted")

            except Exception as e:
                self._logger.write_message(str(__name__) + "/_extract_fields", str(e))

        self._logger.write_message(str(__name__) + "/_extract_fields", "fields extracted")

        self._logger.write_message(str(__name__) + "/_extract_fields", "closing browser")
        # chiudi browser in quanto hai finito
        operator.quit()
        self._logger.write_message(str(__name__) + "/_extract_fields", "browser closed")

        self._logger.write_exiting(str(__name__) + "/_extract_fields")

    def _write_fields(self, extracted_data):

        fields_name = self._facet.get_fields_name()
        if len(extracted_data) > 1:  # se contiene piu' di una matrice interna
            extracted_data = list(zip(*extracted_data))  # combino i dati per la scrittura
            extracted_data = [fields_name] + extracted_data
        else:
            extracted_data = [fields_name] + extracted_data[0]

        self._writer.write(self._writer_data['file_name'], extracted_data)
