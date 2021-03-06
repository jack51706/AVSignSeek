#!/usr/bin/python3
import sys
import argparse
from zipfile import ZipFile
from utils import *
from raw_analysis import raw_analysis
from result import print_results

def main(args):

    print("=== AVSignSeek ===")

    with ZipFile(args.zip_file) as myzip:
        with myzip.open(args.filename, pwd=args.zip_password.encode()) as myfile:
            file_bin = myfile.read()

    try:
        analysed_parts = get_ranges_from_str(args.ranges_str, len(file_bin))
    except Exception as e:
        parser.print_help()
        print("\n%s" % str(e))
        sys.exit(1)

    signature_range_list = raw_analysis(file_bin, analysed_parts, args.limit_sign, args.subdiv, args.sleep)
    signature_range_list = union(signature_range_list)

    print_results(file_bin, signature_range_list, args.output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically detects AV Signatures")
    parser.add_argument("zip_file")
    parser.add_argument('-s', help='waiting time between 2 tests (default: 20)', dest='sleep', default=20, type=int)
    parser.add_argument('-p', help='zip password (default: infected)', dest='zip_password', default="infected")
    parser.add_argument('-f', help='file name contained in the zip (default: infected.bin)', dest='filename', default="infected.bin")
    parser.add_argument('-l', help='signature limit (default: 64)', dest='limit_sign', default=64, type=int)
    parser.add_argument('-d', help='subdiv per step (default: 4)', dest='subdiv', default=4, type=int)
    parser.add_argument('-o', help='output_file (default: output.txt)', dest='output_file', default="output.txt")
    parser.add_argument('-r', help='range (default: ":")', dest='ranges_str', default=":", type=str)

    args = parser.parse_args()

    main(args)
