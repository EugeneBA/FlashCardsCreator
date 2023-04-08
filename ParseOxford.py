import sys
import argparse
import json
import re
import traceback
import pathlib


def ReadLines(filename: str) -> list[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]


LEVELS = ["A1", "A2", "B1", "B2"]
PARTS = [
    "det./pron./adv.",
    "adj./pron.",
    "adj./adv.",
    "adv./prep.",
    "exclam./n.",
    "conj./adv.",
    "conj./prep.",        
    "det./adj.",
    "det./number",
    "det./pron.",    
    "number/det.",
    "pron./det.",
    "prep./adv.",
    "n.",
    "adj.",
    "auxiliary v.",
    "modal v.",
    "adv.",
    "v.",
    "pron.",
    "prep.",
    "conj.",
    "det.",
    "exclam.",
    "indefinite article",
    "definite article",
    "infinitive marker",
    "number"
]

# REG = "(?P<partlist>((?P<part>conj\.\/adv\.|number\/det\.|adj\.\/adv\.|n\.|adj\.|modal v\.|adv\.|v\.|pron\.|prep\.|conj\.|det\.|exclam\.|indefinite article|definite article|infinitive marker|auxiliary v\.|det\.\/pron\.|number),?\s?)+)\s(?P<level>(A|B)(1|2))"
PARTS_REG = "|".join(PARTS).replace(".", "\.")
REG = f"(?P<partlist>(\s(?P<part>{PARTS_REG}),?\s?)+)\s(?P<level>(A|B)(1|2))"


def ParseLines(lines: list[str]) -> list:
    regex = re.compile(REG)

    dict = []
    invalidLines = []

    for line in lines:
        text = line
        res = regex.search(text)
        if res is None:
            invalidLines.append(line)
            continue

        [beg, end] = res.span()
        word = text[:beg].strip()
        parts = res.group("partlist").strip()
        level = res.group("level")
        record = {
            "en": word,
            "parts": parts,
            "level": level
        }
        dict.append(record)

        while end < len(text):
            text = text[end:]
            res = regex.search(text)
            if res is None:
                invalidLines.append(line)
                continue
            [beg, end] = res.span()
            parts = res.group("partlist").strip()
            level = res.group("level")
            record = {
                "en": word,
                "parts": parts,
                "level": level
            }
            dict.append(record)

    return (dict, invalidLines)


# from PyMultiDictionary import MultiDictionary
# dictionary = MultiDictionary()

# print(dictionary.translate('en', 'Environment'))


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
            with open(outfileName, "w") as outfile:
                json.dump(dict, outfile, indent=4)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())
