import os
import random


class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


########################################################

# reading files from words.txt
with open('words.txt', 'r') as file:
	content = file.read()

# setting variables
words = content.split()
lim = int(len(words)) - 1
length = int(input('Enter sentence length: '))


# terminal clearing function for cleaner output
def clear():
	if os.name == 'nt':
		os.system('CLS')
	else:
		os.system('CLEAR')


# generating groups of words
def generate():
	for i in range(length):
		randnum = random.randint(0, lim)
		randletter = words[randnum]
		print(randletter)


generate()
