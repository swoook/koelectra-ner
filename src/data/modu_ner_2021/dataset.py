import json
import csv

from tqdm.contrib.concurrent import process_map

from example import Example


class Dataset:
    def __init__(self, source_path=None):
        self.__example = Example()
        self.__result = list()
        if source_path is not None: 
            self.__source_data = json.load(open(source_path, 'r'))['document']
        
    def convert(self, source_path=None, dst_path=None):
        if source_path is not None: 
            self.__source_data = json.load(open(source_path, 'r'))['document']
        
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
            

def parse_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--src_directory", type=str, required=True)
    arg_parser.add_argument("--dst_directory", type=str, required=True)
    arg_parser.add_argument("--num_cpus", type=int, required=True)

    args = arg_parser.parse_args()
    
    return args
    
    
def main(args):
    entries = os.listdir(args.src_directory)
    entries = [entry for entry in entries if os.path.splitext(entry)[1] == '.json']

    def process_map_fn(entry):
        src_path = os.path.join(src_directory, entry)
        src_name = os.path.splitext(entry)[0]
        dataset = Dataset(os.path.join(src_directory, entry))
        dataset.convert(dst_path=os.path.join(
            args.dst_directory, 
            ''.join([src_name, '.tsv'])
        ))

    process_map(process_map_fn, entries, max_workers=args.num_cpus)
    
    
if __name__ == '__main__':
    args = parse_args()
    main(args)
    
    