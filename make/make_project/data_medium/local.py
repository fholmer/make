import shutil
from .base import DataMediumBase

class Local(DataMediumBase):
    @staticmethod
    def mkdir(target):
        target.mkdir(parents=True)
        #os.makedirs(str(target_path))

    @staticmethod
    def write_text(target, content):
        target.write_text(content)

    @staticmethod
    def read_text(source):
        return source.read_text()

    @staticmethod
    def copy(source, target):
        shutil.copy(source, target)
