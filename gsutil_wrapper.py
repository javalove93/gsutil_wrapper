import argparse

parser = argparse.ArgumentParser(prog='gsutil_wrapper', description='gsutil wrapper')
parser.add_argument('source_file')
parser.add_argument('dest_file')

args = parser.parse_args()

