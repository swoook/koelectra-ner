import csv
import json

from example import Example


class Dataset:
    def __init__(self, source_path=None):
        self.__example = Example()
        self.__result = list()
        if source_path is not None: 
            self.__source_data = json.load(open(source_path, 'r'))['document']

    def __initialize(self):
        self.__result = list()
        self.__source_data = None
        
    def convert(self, src_path=None, dst_path=None):
        if src_path is not None:
            self.__initialize()
            self.__source_data = json.load(open(src_path, 'r'))['document']
        
        for _, document in enumerate(self.__source_data):
            examples = document['sentence']
            for example in examples:
                sequences = self.__example.convert(example)
                if sequences is None: continue
                self.__result.append(sequences)
            
        if dst_path is None: dst_path = './results.tsv'
            
        with open(dst_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(self.__result)