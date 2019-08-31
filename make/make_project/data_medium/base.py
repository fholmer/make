class DataMediumBase():
    @staticmethod
    def mkdir(target):
        raise NotImplementedError

    @staticmethod
    def write_text(target, content):
        raise NotImplementedError

    @staticmethod
    def read_text(source):
        raise NotImplementedError

    @staticmethod
    def copy(source, target):
        raise NotImplementedError
