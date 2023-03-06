def ReadLines(filename:str)->list[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file]

print(ReadLines("En\American_Oxford_3000.txt"))