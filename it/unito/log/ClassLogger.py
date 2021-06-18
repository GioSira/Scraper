from it.unito.log import *


class ClassLog(object):
    instance = None

    def __init__(self, mainfolder):

        if ClassLog.instance is None:
            ClassLog.instance = ClassLog.__Log(mainfolder)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Log(object):

        def __init__(self, mainfolder):
            self.dir = os.path.join(mainfolder, 'logs')
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)

            self.file_name = f'class_log'

            self.writer = WriterFactory.get_writer("LOG", self.dir, {'append': True, 'style': 'date'})

    def write_entering(self, name):
        with lock:
            msg = f'[{str((datetime.now()).strftime("%H:%M:%S"))}] - +++++++++++++++++++++++++++++ Entering {name} +++++++++++++++++++++++++++++\n'
            self.writer.write(self.file_name, msg)

    def write_exiting(self, name):
        with lock:
            msg = f'[{str((datetime.now()).strftime("%H:%M:%S"))}] - +++++++++++++++++++++++++++++ Exiting {name} ++++++++++++++++++++++++++++++\n'
            self.writer.write(self.file_name, msg)

    def write_message(self, class_name, message):
        with lock:
            msg = f'[{str((datetime.now()).strftime("%H:%M:%S"))}] - {class_name}: {message}\n'
            self.writer.write(self.file_name, msg)
