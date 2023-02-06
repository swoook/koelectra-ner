import json

from example import Example


class Dataset:
    def __init__(self, source_path=None):
        self.__example = Example()
        self.__result = list()
        if source_path is not None: 
            self.__source_data = json.load(open(source_path, 'r'))['data']
        
    # @property
    # def source_data(self):
    #     return self.__source_data
    
    # @source_data.setter
    # def source_data(self, source_path):
    #     self.__source_data = json.load(open(source_path, 'r'))['data']
        
    def convert(self, source_path=None):
        if source_path is not None: 
            self.__source_data = json.load(open(source_path, 'r'))['data']
        
        for _, source_example in enumerate(self.__source_data):
            self.__result.append(
                self.__example.convert(source_example)
            )

        return self.__result