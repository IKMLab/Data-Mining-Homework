import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    def add_args(*args, **kwargs):
        parser.add_argument(*args, **kwargs)

    add_args('--min_sup', type=float, default=0.1, help='Minimum support')
    add_args('--min_conf', type=float, default=0.1, help='Minimum confidence')

    # TODO: You should add the dataset argument here
    add_args('--dataset', type=str, default='your-raw-inputs.txt', help='Dataset to use, please include the extension')

    return parser.parse_args()
