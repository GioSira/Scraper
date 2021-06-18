from it.unito.skeletons.AbcWriter import AbcWriter
from it.unito.writer import *


class XLSWriter(AbcWriter):

    def __init__(self, mainfolder=None, setting=None):
        super().__init__(mainfolder, setting)

    def __inner_write(self, data, df, cols):
        single_entry = pd.DataFrame([data], columns=cols)
        df = df.append(single_entry, ignore_index=True)
        return df

    def write(self, name, data_to_write, **kwargs):

        assert len(data_to_write) > 1, 'No data to write'

        name = self._get_name(name)
        name = os.path.join(self._mainfolder, f'{name}.xlsx')

        writer = pd.ExcelWriter(name, engine='openpyxl', mode='w')

        cols = data_to_write[0]
        df = pd.DataFrame(columns=cols)

        if isinstance(data_to_write, list) and \
                isinstance(data_to_write[0], list) or isinstance(data_to_write[0], tuple):
            for data in data_to_write[1:]:
                df = self.__inner_write(data, df, cols)
        elif isinstance(data_to_write, list) or isinstance(data_to_write, tuple):
            df = self.__inner_write(data_to_write[1], df, cols)

        df.to_excel(writer, index=False)
        writer.save()

        writer.close()
