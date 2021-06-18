from it.unito.skeletons import *


class AbcWriter(metaclass=ABCMeta):

    def __init__(self, mainfolder=None, setting=None):
        if mainfolder is None:
            self._mainfolder = '.'
        else:
            self._mainfolder = mainfolder
            if not os.path.exists(self._mainfolder):
                os.makedirs(self._mainfolder)

        if setting:
            assert (setting in ['plain', 'date'], f'setting {setting} not into [\'plain\', \'date\'] list')

        self._setting = setting

    def _get_name(self, name):

        if self._setting and self._setting == 'date':
            return f'{name}_{datetime.now().strftime("%Y_%m_%d")}'

        return f'{name}'

    @abstractmethod
    def write(self, name, data_to_write, **kwargs):
        pass
