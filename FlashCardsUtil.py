import sys
import argparse
import json
import traceback

def ReadDict(filename: str) -> list:
    with open(filename) as file:
        return json.loads(file.read())
    
def ListWords(dict:list, args)->int:
    for item in  dict:
        print(item)

    print(len(dict))
    return 0

def main() -> int:
    
    parser = argparse.ArgumentParser(description="Parse American Oxford 3000 dictionary from TEXT (.txt) to JSON (.json)")

    parser.add_argument('infile', help="input file(.json)")
    parser.add_argument('cmd', choices=["list", "auto_translate", "create_cards"], help="command")
    parser.add_argument('-L','--Level', action='append', choices=["A1", "A2", "B1", "B2"], help="level")
    parser.add_argument('-P','--Part', action='append',  help="speech part")    
    parser.add_argument('outfile', nargs='?', help="output file")

    args = parser.parse_args()

    try:
        print(args)

        dict = ReadDict(args.infile)
        
        #print(dict[1])

        match args.cmd:
            case "list":
                ListWords(dict, args)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0


if __name__ == '__main__':
    sys.exit(main())