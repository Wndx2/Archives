"""
making this to practice my python because im getting sodium next year in dtsd 😭
this is still work in progress so stfu
"""

import os
import random
# import readchar as rc
# import time

# reading files from words.txt
with open('words.txt', 'r') as file:
	content = file.read()

# setting variables
full_list = content.split()
full_list_word_count = int(len(full_list)) - 1
sentence_length = int(input('Enter sentence length: '))
words = []
yourwords = []


class Colors:
	# could print using colors like this:
	# print(f'{Colors.BLUE}Enter text here{Colors.DEFAULT}')

	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	DEFAULT = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


# terminal clearing function for cleaner output
def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


# generating groups of words
def generate():
	for i in range(sentence_length):
		randnum = random.randint(0, full_list_word_count)
		# picks random word from full_list list
		randletter = full_list[randnum]

		# 'word' list contains the randomized words
		words.append(randletter)

	# use following format to print it with spaces in between

	print('\n\n ', ' '.join(words), '\n\n')


generate()

# while True:
# break
