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

	PURPLE = '\033[1;35m'
	BLUE = '\033[1;34m'
	CYAN = '\033[1;36m'
	GREEN = '\033[1;32m'
	YELLOW = '\033[1;33m'
	RED = '\033[1;31m'
	DEFAULT = '\033[0m'
	GREY = '\033[90m'


# --- --- --- variables --- --- --- #

# reading files from words.txt
with open('words.txt', 'r') as file:
	content = file.read()

word_list = content.split()
word_list_length = int(len(word_list)) - 1
completed_words = []
word_times = []

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
	global current_word

	for i in range(1):
		random_index = random.randint(0, word_list_length)
		# picks random word from word_list list
		current_word = (word_list[random_index]).lower()

	# Use this to print:
	# print(f'\n\n {current_word} \n\n')


def countdown():
	for i in range(3, 0, -1):
		print(f'\r{i}', end='', flush=True)
		time.sleep(1)
	print(f'\r{Colors.YELLOW}GO!{Colors.DEFAULT}\n\n')
	flush()


# --- --- --- main code --- --- --- #

while True:
	start_game = input('Start? (y) ')
	try:
		clear()
		if start_game.lower() == 'y':
			num_words = int(input('How many words? '))
			while len(completed_words) < num_words:
				generate()
				clear()
				print('\n\nWORD:')
				print(f'>>> {Colors.BLUE}{current_word}{Colors.DEFAULT}')

				countdown()

				start_time = time.time()
				# time.time() is the initial time when the timer starts
				user_input = input('>>> ')
				elapsed_time = time.time() - start_time

				if user_input == current_word:
					print(f'{Colors.GREEN}\n\nCorrect!{Colors.DEFAULT}')
					print(f'Time taken: {elapsed_time:.2f} seconds\n\n')
					completed_words.append(user_input)
					word_times.append(elapsed_time)

					time.sleep(2)

				else:
					print(f'{Colors.RED}\n\nFailed!{Colors.DEFAULT}')
					time.sleep(2)

			total_time = 0
			for i in word_times:
				total_time += i
			average_time = total_time / num_words

			wpm = 60 / average_time

			clear()
			print(f'{Colors.GREY}--- --- --- --- ---\n')

			index = 0
			for j in completed_words:
				print(f'{j} : {round(word_times[index], 2)}')
				index += 1

			print(f'\n--- --- --- --- ---{Colors.DEFAULT}')

			print(f'\n\nAverage Time: {round(average_time, 2)}')
			print(f'WPM: {round(wpm, 2)}\n\n')

			completed_words = []
			word_times = []

		elif start_game == 'n':
			print('bye')
			break
		else:
			print('ni meiyou baba')
	except ValueError:
		print('ni meiyou mama')
