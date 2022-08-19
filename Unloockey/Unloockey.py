#!/usr/bin/python3
import argparse
import sys
from itertools import permutations
import configparser
import argparse


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = MyParser()
args = parser.parse_args()


def print_help():
    with open("help.txt") as f:
        print(f.read())


cfg = configparser.ConfigParser()
cfg.read("Unloockey.cfg")

CONFIG = {"global": {
    "years": cfg.get("years", "years").split(","),
    "chars": cfg.get("chars", "chars").split(","),
    "numeros": cfg.get("nums", "numeros").split(",")

}}

birthdate = ""
address = ""
addressup = ""
words = []
numbers = []
numeros = CONFIG["global"]["numeros"]
years = CONFIG["global"]["years"]
chars = CONFIG["global"]["chars"]

# Almacena los años especificados en el archivo de configuración
for y in years:
    numbers.append(y)

# Almacena numeros del 0 al 100
for i in range(101):
    numbers.append(i)

# Almacena los números de la dirección en la lista de numeros,
# Pone la primera letra de cada palabra de la dirección en mayuscula los espacios y remueve los espacios .
for i in address.split():
    if i.isnumeric():
        numbers.append(i)
    addressup += str(i.title())
address = address.replace(" ", "")

# Separar fecha de nacimiento y agregarla a la lista
numbers.append(birthdate)
numbers.append(birthdate[-2:])
numbers.append(birthdate[-3:])
numbers.append(birthdate[-4:])
numbers.append(birthdate[1:2])
numbers.append(birthdate[3:4])
numbers.append(birthdate[:2])
numbers.append(birthdate[2:4])

# Agrega la direccion sin numeros a la lista de palabras.
words.append(''.join([i for i in address if not i.isdigit()]))
words.append(''.join([i for i in addressup if not i.isdigit()]))

# Agregar perfil
with open("profile.txt") as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith("birthdate:"):
            none, line = line.split(':')
            if len(line) != 0 and len(line) != 8:
                print("ERROR: INCORRECT SYNTAX Birthdate (DDMMYYYY)")
                exit()
            else:
                birthdate = line
        elif line.startswith("address:"):
            none, line = line.split(':')
            address = line

        elif isinstance(line, str):
            words.append(line)
            print(words[0])
        else:
            numbers.append(line)
            print(numbers[0])

# //WORDLIST//


wordlist = open("wordlist", "a+")

# Agrega las listas sin combinar y las combinadas a la wordlist
for num in numbers:
    wordlist.writelines(str(num) + "\n")
    for word in words:
        for i in list(permutations([num, word], 2)):
            wordlist.writelines("".join(map(str, i)) + "\n")
        for char in chars:
            for i in list(permutations([num, word, char], 3)):
                wordlist.writelines("".join(map(str, i)) + "\n")

for word in words:
    wordlist.writelines(word + "\n")
    for otherwords in words:
        if word != otherwords:
            word2 = word + otherwords
            wordlist.writelines(word2 + "\n")
            for num in numbers:
                for i in list(permutations([word2, num], 2)):
                    wordlist.writelines("".join(map(str, i)) + "\n")
                    for char in chars:
                        for i in list(permutations([num, word2, char], 3)):
                            wordlist.writelines("".join(map(str, i)) + "\n")

wordlist.close()