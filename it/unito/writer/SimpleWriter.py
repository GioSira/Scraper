from it.unito.skeletons.AbcWriter import AbcWriter
from it.unito.writer import *


class SimpleWriter(AbcWriter):

    def __init__(self, mainfolder=None, setting=None):
        super().__init__(mainfolder, setting)

    def write(self, name, data_to_write, **kwargs):
        name = self._get_name(name)
        name = os.path.join(self._mainfolder, f'{name}.txt')

        with open(name, 'w') as writer:
            writer.write(data_to_write)
            writer.flush()
