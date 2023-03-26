import json
import re


def ReadLines(filename: str) -> list[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]

REG = "(?P<partlist>((?P<part>conj\.\/adv\.|number\/det\.|adj\.\/adv\.|n\.|adj\.|modal v\.|adv\.|v\.|pron\.|prep\.|conj\.|det\.|exclam\.|indefinite article|definite article|infinitive marker|auxiliary v\.|det\.\/pron\.|number),?\s?)+)\s(?P<level>(A|B)(1|2))"

dict = []
invalidLines = []

lines = ReadLines("En\American_Oxford_3000.txt")

regex = re.compile(REG)

for line in lines:
    text = line
    res = regex.search(text)
    if res is None:
        invalidLines.append(line)
        continue
    [beg, end] = res.span();
    word = text[:beg].rstrip()
    parts = res.group("partlist")
    level = res.group("level")
    record = {
        "en": word,
        "parts": parts,
        "level": level,
        "ru": None
         }
    
    dict.append(record)

    while end<len(text):
        text = text[end:]
        res = regex.search(text)
        if res is None:
            invalidLines.append(line)
            continue
        [beg, end] = res.span();
        parts = res.group("partlist")
        level = res.group("level")
        record = {
             "en": word,
             "parts": parts,
             "level": level,
             "ru": None
             }
    
        dict.append(record)


# print(dict)
print(len(dict))
print(len(invalidLines))

for line in invalidLines:
    print(line)


with open("En\American_Oxford_3000.json", "w") as outfile:
    json.dump(dict, outfile, indent = 4)

# from PyMultiDictionary import MultiDictionary
# dictionary = MultiDictionary()

# print(dictionary.translate('en', 'Environment'))
