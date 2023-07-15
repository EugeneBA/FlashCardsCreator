import sys
import argparse
import json
import traceback
import pathlib

def ReadLines(filename: str) -> list[str]:
    with open(filename, encoding="utf-8") as file:
        return file.readlines()


def ParseLines(lines: list[str]) -> list:
    dict = []
    invalidLines = []

    for line in lines:
        if not line.strip():            
            continue

        words = line.split('-')
        if len(words)<2:
            invalidLines.append(line)
            continue

        record = {
            "de": words[0].strip(),
            "ru": words[1].strip(),            
        }
        dict.append(record)      

    return (dict, invalidLines)

def main() -> int:

    parser = argparse.ArgumentParser(description="Parse American Oxford 3000 dictionary from TEXT (.txt) to JSON (.json)")

    parser.add_argument('infile', help="input file(.txt)")
    parser.add_argument('outfile', nargs='?', help="output file(.json) (default: [infile].json)")

    args = parser.parse_args()

    try:
        lines = ReadLines(args.infile)
        dict, invalidLines = ParseLines(lines)

        print(f"{len(dict)} words were parsed successfully")
        if len(invalidLines) > 0:
            print()
            print(f"Next {len(invalidLines)} lines were invalid:")
            for line in invalidLines:
                print(line)

        if len(dict) > 0:
            outfileName = args.outfile
            if outfileName is None:
                p = pathlib.Path(args.infile)
                outfileName = p.with_suffix(".json")
            with open(outfileName, "w", encoding="utf-8") as outfile:
                json.dump(dict, outfile, indent=4, ensure_ascii=False)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())
