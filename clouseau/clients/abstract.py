
from abc import ABCMeta, abstractmethod



class AbstractClient:
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self,data):
        """
        Each instance of an AbstractClient must implement a render method, 
        which is called by Clouseau
        """
        raise Exception


