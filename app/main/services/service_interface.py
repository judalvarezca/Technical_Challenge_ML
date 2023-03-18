import abc


class Service(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_map_url') and 
                callable(subclass.load_map_url) and 
                hasattr(subclass, 'run') and 
                callable(subclass.run) or 
                NotImplemented)

    @abc.abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def load_map_url(self, **kwargs):
        raise NotImplementedError