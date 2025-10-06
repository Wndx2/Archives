"""
making this to practice my python because im getting sodium next year in dtsd 😭
this is still work in progress so stfu
"""

# --- --- --- imports --- --- --- #

import os
import sys
import random
import time
import termios


# --- --- --- classes --- --- --- #
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
	GREY = '\033[90m'


# --- --- --- variables --- --- --- #

# reading files from words.txt
with open('words.txt', 'r') as file:
	content = file.read()

full_list = content.split()
full_list_word_count = int(len(full_list)) - 1
completecount = []
times = []

# --- --- --- functions --- --- --- #


# terminal clearing function for cleaner output
def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


def flush():
	termios.tcflush(sys.stdin, termios.TCIFLUSH)


# generating word (does not print)
def generate():
	global randletter

	for i in range(1):
		randnum = random.randint(0, full_list_word_count)
		# picks random word from full_list list
		randletter = (full_list[randnum]).lower()

	# Use this to print:
	# print(f'\n\n {randletter} \n\n')


def countdown():
	for i in range(3, 0, -1):
		print(f'\r{i}', end='', flush=True)
		time.sleep(1)
	print(f'\r{Colors.YELLOW}GO!{Colors.DEFAULT}\n\n')
	flush()


# --- --- --- main function --- --- --- #

while True:
	play = input('Start? (y) ')
	try:
		if play.lower() == 'y':
			howmany = int(input('How many words? '))
			while len(completecount) < howmany:
				generate()
				clear()
				print('\n\nWORD:')
				print(f'>>> {Colors.BLUE}{randletter}{Colors.DEFAULT}')

				countdown()

				start_time = time.time()
				# time.time() is the initial time when the timer starts
				userinput = input('>>> ')
				elapsed = time.time() - start_time

				if userinput == randletter:
					print(f'{Colors.GREEN}\n\nCorrect!{Colors.DEFAULT}')
					print(f'Time taken: {elapsed:.2f} seconds\n\n')
					completecount.append(userinput)
					times.append(elapsed)

					# debugging purposes
					# print(completecount)
					# print(times)

					boboyuan = 0
					print('====================')
					for thing in completecount:
						print(f'{thing} : {round(times[boboyuan], 2)}')
						boboyuan += 1
					print('====================')

					time.sleep(2)
				else:
					print(f'{Colors.RED}\n\nFailed!{Colors.DEFAULT}')
					time.sleep(2)

			totaltime = 0
			for j in times:
				totaltime += j
			avgtime = totaltime / howmany

			wpm = 60 / avgtime

			print(f'\n\naverage time: {round(avgtime, 2)}')
			print(f'wpm: {round(wpm, 2)}\n\n')

			completecount = []
			times = []

		elif play == 'n':
			print('bye')
			break
		else:
			print('ni meiyou baba')
	except ValueError:
		print('Valueerrro')

		# 1 : 0.72
		# 1 x Y : 0.72 x Y = 60


# --- --- --- summary --- --- --- #

# append the correctly typed words into a list

# add summary screen:
# avg time taken, wpm, words that were used (in list)

# put it in a while loop (until 5 correctly typed) so that the user can continue with this unless program quits
