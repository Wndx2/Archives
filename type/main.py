import os
import random

########################################################

# reading files from words.txt
with open('words.txt', 'r') as file:
	content = file.read()

# setting variables
words = content.split()
lim = int(len(words)) - 1
randnum = random.randint(0, lim)


# terminal clearing function for cleaner output
def clear():
	if os.name == 'nt':
		os.system('CLS')
	else:
		os.system('CLEAR')


# generating groups of words (placeholder for now)
def generate():
	print()


########################################################

print(lim)
print(randnum)
print(words[randnum])
