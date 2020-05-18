from modules.scanner import Scanner
from modules.parser import Parser
from sys import argv, exit

if len(argv)==1:
    exit('No arguments provided. Need to provide text file as argument.')
elif len(argv) > 2:
    exit('Too many arguments.')
if str(argv[1]).split('.')[-1] != 'txt':
    exit('Wrong file format. File must be a TXT file')

file = open(argv[1])

with file as input_file:
    file_content = input_file.read()
scanner = Scanner(file_content)
parser = Parser(scanner)
parser.start()