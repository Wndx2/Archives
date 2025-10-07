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
	# print(f'{Colors.BLUE}Enter text here{Colors.DEFAULT}')
	# https://gist.github.com/iamnewton/8754917 -- for a list of full color codes
	# all ansi colors are in colored bold text

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
with open('words25k.txt', 'r') as file:
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
	clear()
	print(f"You type the word that's printed in {Colors.BLUE}blue{Colors.DEFAULT}.")
	print(
		f'Press {Colors.GREY}"enter"{Colors.DEFAULT} once you are done typing to submit your input.\n'
	)
	print('Your score will be calculated based on your WPM and average speed.\n\n')
	start_game = input(f'Start? ({Colors.GREEN}y{Colors.DEFAULT}/{Colors.RED}n{Colors.DEFAULT}) ')
	try:
		clear()
		if start_game.strip().lower() == 'y':
			num_words = int(input('How many words? '))

			if num_words <= 0:
				clear()
				print('ni meiyou baba')
				break
			else:
				# loops function until gets {num_words} appended into the {word_times} list
				while len(completed_words) < num_words:
					generate()
					clear()
					print('\nWORD:')
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
						break

				# wpm calculation
				total_time = sum(word_times)
				average_time = total_time / num_words
				all_typed_entries = 0
				for word in completed_words:
					all_typed_entries += len(word)
				wpm = (all_typed_entries / 5) / (total_time / 60)

				# summary screen
				clear()
				print(f'{Colors.GREY}--- --- typed words --- ---\n')

				index = 0
				for j in completed_words:
					print(f'{j} : {round(word_times[index], 2)}')
					index += 1

				print(f'\n--- --- --- --- --- --- ---{Colors.DEFAULT}\n\n')

				print(f'Average Time: {Colors.YELLOW}{round(average_time, 2)}{Colors.DEFAULT}')

				# prints wpm output based on wpm
				if wpm < 30:
					print(f'WPM: {Colors.RED}{round(wpm, 2)}{Colors.DEFAULT}')
					print(f'{Colors.GREY}* ni shi stoobid{Colors.DEFAULT}\n')
				elif wpm > 30 and wpm < 40:
					print(f'WPM: {Colors.RED}{round(wpm, 2)}{Colors.DEFAULT}')
					print(f"{Colors.GREY}* you're slow asf{Colors.DEFAULT}\n")
				elif wpm > 40 and wpm < 100:
					print(f'WPM: {Colors.YELLOW}{round(wpm, 2)}{Colors.DEFAULT}')
					print(f'{Colors.GREY}* average{Colors.DEFAULT}\n')
				elif wpm > 100 and wpm < 120:
					print(f'WPM: {Colors.GREEN}{round(wpm, 2)}{Colors.DEFAULT}')
					print(f'{Colors.GREY}* good{Colors.DEFAULT}\n')
				else:
					print(f'WPM: {Colors.PURPLE}{round(wpm, 2)}{Colors.DEFAULT}')
					print(f'{Colors.GREY}* touch grass{Colors.DEFAULT}\n')

				# calculates score based on WPM
				score = round((wpm * 100) - (average_time * 10))
				print(f'Your score is: {Colors.PURPLE}{score}{Colors.DEFAULT}\n\n')

				print(f'{Colors.GREY}--- --- --- --- --- --- ---{Colors.DEFAULT}\n')

				# enter clears the screen, and reloops the while loop at the top
				input('Press enter to continue')

				# initializes the lists (fresh state)
				completed_words = []
				word_times = []

		elif start_game == 'n':
			print('bye')
			break
		else:
			print('ni meiyou fangzi')
	except ValueError:
		continue
