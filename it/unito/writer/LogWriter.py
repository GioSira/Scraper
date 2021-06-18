from it.unito.skeletons.AbcWriter import AbcWriter
from it.unito.writer import *


class LogWriter(AbcWriter):

    def __init__(self, mainfolder=None, setting=None):

        super().__init__(mainfolder, setting)
        self._append_flag = (setting is not None) and setting['append']

    def write(self, name, data_to_write, **kwargs):

        if 'style' in self._setting and self._setting['style'] == 'date':
            name = f'{name}_{(datetime.now()).strftime("%Y%m%d")}.log'
        name = os.path.join(self._mainfolder, name)

        writer_flag = 'w'
        if os.path.exists(name) and self._append_flag:
            writer_flag = 'a'

        with open(name, writer_flag) as writer:

            if isinstance(data_to_write, str):
                writer.write(data_to_write + '\n')
                writer.flush()

            elif isinstance(data_to_write, list):

                for data in data_to_write:
                    writer.write(data + '\n')
                writer.flush()

            else:
                raise Exception(f'datatype {type(data_to_write)} not supported')
