# from deep_translator import (GoogleTranslator,
#                              MicrosoftTranslator,
#                              PonsTranslator,
#                              LingueeTranslator,
#                              MyMemoryTranslator,
#                              YandexTranslator,
#                              PapagoTranslator,
#                              DeeplTranslator,
#                              QcriTranslator,
#                              LibreTranslator,
#                              single_detection,
#                              batch_detection)

from enum import Enum
from deep_translator import MyMemoryTranslator
from deep_translator import LibreTranslator
from deep_translator import GoogleTranslator
import sys
import time
import argparse
import json
import traceback
import ParseOxford

from openpyxl import Workbook


def ReadDict(filename: str) -> list:
    with open(filename) as file:
        return json.loads(file.read())


def WriteDict(filename: str, dict: list):
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(dict, outfile, indent=4, ensure_ascii=False)


def ExportDictToTxt(filename: str, dict: list):
    with open(filename, "w", encoding="utf-8") as outfile:
        outfile.writelines(
            map(lambda rec: f"{rec['en']}\t{rec['ru']}\n", dict))


def ExportDictToExcel(filename: str, dict: list):
    wb = Workbook()
    ws = wb.active
    for rec in dict:
        ws.append([rec['ru'], rec['en']])
    wb.save(filename)


def FilterDict(dict: list, level: str = None, part: str = None, status: str = None) -> list:
    iterator = dict
    if level is not None:
        iterator = filter(lambda rec: rec["level"] == level, iterator)
    if part is not None:
        iterator = filter(lambda rec: part in rec["parts"], iterator)
    if status is not None:
        iterator = filter(lambda rec: rec["status"] == status, iterator)
    return list(iterator)


def ListWords(dict: list):
    for item in dict:
        print(item)

    print(len(dict))


def TranslateWords(dict: list):
    # translator = MyMemoryTranslator(source='en', target='ru')
    # translator = LibreTranslator(source='en', target='ru')
    translator = GoogleTranslator(source='en', target='ru')
    i = 1
    for rec in dict:
        rec['ru'] = translator.translate(rec['en'])
        print(f"{i}: {rec['en']} -> {rec['ru']}")
        i += 1
        if i % 11 == 0:
            time.sleep(0.7)


# langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
# print(langs_dict)

# OK translated = GoogleTranslator(source='en', target='ru').translate("fifty")
# print(translated)

# OK translated = MyMemoryTranslator(source='en', target='ru').translate("fifty")
# print(translated)

# KEY? translated = DeeplTranslator(source='en', target='ru', use_free_api=True).translate("fifty")
# print(translated)

# FAIL print("language pairs: ", QcriTranslator("your_api_key").languages)

# FAIL translated = LingueeTranslator(source='english', target='russian').translate("fifty")
# print(translated)

# ???? translated = PonsTranslator(source='english', target='russian').translate("fifty", return_all=True)
# print(translated)

# KEY? translated = YandexTranslator('').translate(source="en", target="ru", text='fifty')
# print(translated)

# KEY? translated = MicrosoftTranslator(api_key='', source='en', target='ru',).translate("fifty")
# print(translated)

# OK translated = LibreTranslator(source='en', target='ru').translate("fifty")
# print(translated)


class Cmd(Enum):
    List = 'list'
    Translate = 'translate'
    Export = 'export'


COMMANDS = [Cmd.List.value, Cmd.Translate.value, Cmd.Export.value]


def main() -> int:

    print(sys.argv)

    parser = argparse.ArgumentParser(description="Parse American Oxford 3000 dictionary from TEXT (.txt) to JSON (.json)")
    parser.add_argument('infile', help="Input file(.json)")
    parser.add_argument('cmd', choices=COMMANDS, help="Command")
    parser.add_argument('-L', '--Level', choices=ParseOxford.LEVELS, help="Level")
    parser.add_argument('-P', '--Part', choices=ParseOxford.PARTS, help="Speech part")
    parser.add_argument('-S', '--Status', help="Status")
    parser.add_argument('outfile', nargs='?', help="Output file")

    args = parser.parse_args()

    try:
        print(args)

        dict = ReadDict(args.infile)
        filtered = FilterDict(dict, args.Level, args.Part, args.Status)

        match args.cmd:
            case Cmd.List.value:
                # ListWords(filtered)
                print(Cmd.List)
            case Cmd.Translate.value:
                TranslateWords(filtered)
                WriteDict(args.outfile, dict)
                print(Cmd.Translate)
            case Cmd.Export.value:
                ExportDictToExcel(args.outfile, filtered)
                print(Cmd.Export)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())
