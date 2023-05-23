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
import pathlib
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
    with open(filename, encoding='utf-8') as file:
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
        if status == "none":
            iterator = filter(lambda rec: (not("status" in rec)) or (not(rec["status"].strip()) or rec["status"] == "none"), iterator)
        else:
            iterator = filter(lambda rec: ("status" in rec) and (rec["status"] == status), iterator)
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
        if i % 51 == 0:
            time.sleep(1.2)
        elif i%11 == 0:
            time.sleep(0.7)

def SetNewStatus(status:str, dict: list):
    for rec in dict:
        rec['status'] = status

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
    SetStatus = 'set_status'

class Status(Enum):
    Known = 'known'
    Study = 'study'
    NoSet = None

COMMANDS = [Cmd.List.value, Cmd.Translate.value, Cmd.Export.value, Cmd.SetStatus.value]

def main() -> int:

    print(sys.argv)

    parser = argparse.ArgumentParser(description="Parse American Oxford 3000 dictionary from TEXT (.txt) to JSON (.json)")
    parser.add_argument('infile', help="Input file(.json)")
    parser.add_argument('cmd', choices=COMMANDS, help="Command")
    parser.add_argument('-L', '--Level', choices=ParseOxford.LEVELS, help="Level")
    parser.add_argument('-P', '--Part', choices=ParseOxford.PARTS, help="Speech part")
    parser.add_argument('-S', '--Status', help="Status")
    parser.add_argument('-NS', '--NewStatus', help="New status")
    parser.add_argument('outfile', nargs='?', help="Output file")

    args = parser.parse_args()

    try:
        print(args)

        dict = ReadDict(args.infile)
        filtered = FilterDict(dict, args.Level, args.Part, args.Status)

        outfile = args.outfile
        if outfile is None:
            dict_outfile = args.infile

        match args.cmd:
            case Cmd.List.value:
                ListWords(filtered)
                print(Cmd.List)
            case Cmd.Translate.value:
                TranslateWords(filtered)
                WriteDict(dict_outfile, dict)
                print(Cmd.Translate)
            case Cmd.Export.value:
                p = pathlib.Path(args.outfile)
                if p.suffix == '.xlsx':
                    ExportDictToExcel(args.outfile, filtered)
                else:
                    ExportDictToTxt(args.outfile, filtered)
                print(Cmd.Export)
            case Cmd.SetStatus.value:
                SetNewStatus(args.NewStatus, filtered)
                WriteDict(dict_outfile, dict)
                print(Cmd.SetStatus)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())
