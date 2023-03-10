import argparse
import os

from dataset import Dataset
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


def parse_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--src_directory", type=str, required=True)
    arg_parser.add_argument("--dst_directory", type=str, required=True)
    arg_parser.add_argument("--num_cpus", type=int, required=True)

    args = arg_parser.parse_args()
    
    return args
    

def main(args):
    entries = list()
    for base_dir, _, filenames in os.walk(args.src_directory):
        entries.extend([
            os.path.join(base_dir, filename) for filename in filenames if os.path.splitext(filename)[1] == '.json'
        ])

    if not os.path.exists(args.dst_directory): os.makedirs(args.dst_directory)

    if args.num_cpus == 1:
        dataset = Dataset()
        for entry in tqdm(entries):
            src_path = entry
            src_name = os.path.splitext(os.path.basename(entry))[0]
            dst_path = os.path.join(args.dst_directory, ''.join([src_name, '.tsv']))
            dataset.convert(
                    src_path=src_path, 
                    dst_path=dst_path
                    )

    elif args.num_cpus > 1:
        def process_map_fn(entry):
            src_path = entry
            src_name = os.path.splitext(os.path.basename(entry))[0]
            dst_path = os.path.join(args.dst_directory, ''.join([src_name, '.tsv']))
            dataset = Dataset(src_path)
            dataset.convert(dst_path=dst_path)

        process_map(process_map_fn, entries, max_workers=args.num_cpus)
    
    
if __name__ == '__main__':
    args = parse_args()
    main(args)