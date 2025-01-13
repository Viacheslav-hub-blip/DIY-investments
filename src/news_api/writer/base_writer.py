import abc
class BaseWriter(abc.ABC):
    @abc.abstractmethod
    def write_to_file(self,file_path:str, data):pass
