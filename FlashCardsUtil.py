import sys
import argparse
import json
import traceback

def main() -> int:
    
    parser = argparse.ArgumentParser(description="Parse American Oxford 3000 dictionary from TEXT (.txt) to JSON (.json)")

    parser.add_argument('infile', help="input file(.txt)")
    parser.add_argument('outfile', nargs='?', help="output file(.json) (default: [infile].json)")

    args = parser.parse_args()

    try:
        print("test")
    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())