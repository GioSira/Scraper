from it.unito.writer.JSonWriter import JSonWriter
from it.unito.writer.LogWriter import LogWriter
from it.unito.writer.SimpleWriter import SimpleWriter
from it.unito.writer.WriterType import WriterType
from it.unito.writer.XLSWriter import XLSWriter


class WriterFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def get_writer(writerType, mainfolder, setting):

        if WriterType.SIMPLE.equals(writerType):
            return SimpleWriter(mainfolder, setting)
        elif WriterType.XLS.equals(writerType):
            return XLSWriter(mainfolder, setting)
        elif WriterType.LOG.equals(writerType):
            return LogWriter(mainfolder, setting)
        elif WriterType.JSON.equals(writerType):
            return JSonWriter(mainfolder, setting)
        else:
            raise ValueError('writer type %s not present in class WriterType' % writerType)
