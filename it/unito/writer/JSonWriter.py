import json

from it.unito.skeletons.AbcWriter import AbcWriter
from it.unito.writer import *


class JSonWriter(AbcWriter):

    def __init__(self, mainfolder=None, setting=None):
        super().__init__(mainfolder, setting)

    def write(self, name, data_to_write, **kwargs):
        name = os.path.join(self._mainfolder, name)

        with open(name, 'w') as writer:
            json.dump(data_to_write, writer, indent=2)
