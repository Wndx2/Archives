"""
making this to practice my python because im getting sodium next year in dtsd 😭
this is still work in progress so stfu
"""

import os
import sys
import random
import time
import termios


# terminal clearing function for cleaner output
def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


# terminal input clearing function. (so that the users don't type during the countdown)
def flush():
	termios.tcflush(sys.stdin, termios.TCIFLUSH)


# generating word (does not print)
def generate():
	global current_word, word_list, word_list_length

	for i in range(1):
		random_index = random.randint(0, word_list_length)
		# picks random word from word_list list
		current_word = (word_list[random_index]).lower()

	# Use this to print:
	# print(f'\n\n {current_word} \n\n')


# countdown function
def countdown():
	for i in range(3, 0, -1):
		print(f'\r{i}', end='', flush=True)
		time.sleep(1)
	print(f'\r{Colors.YELLOW}GO!{Colors.DEFAULT}\n\n')
	flush()


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


# list of heartwarming messages you could get
heartwarming_messages = [
	'skill issues',
	'baha sucker sucker',
	'are you bobo?',
	'imagine failing',
	'all green',
	'not achieved in typing',
	'fatass',
	'ni shi stupid',
	'bobo has a higher accuracy than you',
	'om has a higher accuracy than you',
	'L',
	'cai jiu duo lian shu bu qi jiu bie wan yi qian shi yi qian xian zai shi xian zai',
	'cai',
	'you animal. no one care animal. so no one care you.',
]

# introduction
clear()


def introduction():
	print(f'{Colors.CYAN}Welcome to bobotype!{Colors.DEFAULT}\n')
	print(f"You type the word/sentence that's printed in {Colors.BLUE}blue{Colors.DEFAULT}.")
	print(f'Press {Colors.GREY}"enter"{Colors.DEFAULT} once you are done typing to submit your input.\n')
	print('Your score will be calculated based on your WPM and average speed.')
	print('Please note that your WPM may not be accurate when typing singular words!\n\n')


def generate():
	global current_word

	for i in range(1):
		random_index = random.randint(0, word_list_length)
		# picks random word from word_list list
		current_word = (word_list[random_index]).lower()


def countdown():
	for i in range(3, 0, -1):
		print(f'\r{i}', end='', flush=True)
		time.sleep(1)
	print(f'\r{Colors.YELLOW}GO!{Colors.DEFAULT}\n\n')
	flush()


def run_words():
	if len(completed_words) < num_words:
		generate()
		clear()
		print('\nWORD:')
		print(f'>>> {Colors.BLUE}{current_word}{Colors.DEFAULT}')
		countdown()
		start_time = time.time()
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
			print(
				f'{Colors.GREY}{heartwarming_messages[int(random.randint(0, len(heartwarming_messages) - 1))]}{Colors.DEFAULT}'
			)
			time.sleep(2)
		run_words()
	else:
		summary()


def select_mode():
	global mode, word_list_length, completed_words, word_times, num_words, word_list, word_times
	clear()
	word_list = content.split()
	word_list_length = int(len(word_list)) - 1
	completed_words = []
	word_times = []
	mode = input(f'Select Mode:\n{Colors.GREEN}1. Words\n{Colors.BLUE}2. Sentence\n\n{Colors.DEFAULT}>>> ')
	if mode.strip() == '1':
		num_words = int(input('How many words? '))
		if num_words <= 0:
			clear()
			print('ni meiyou baba\n')
			select_mode()
		else:
			run_words()


def select_difficulty():
	global difficulty, content
	clear()
	difficulty = input(
		f'Select Level:\n{Colors.GREEN}1. Easy\n{Colors.RED}2. Hard\n{Colors.PURPLE}3. Custom\n\n{Colors.DEFAULT}>>> '
	)
	if difficulty.strip().lower() not in ['1', '2', '3']:
		clear()
		print('invalid difficulty(1)\n')
		select_difficulty()
	elif difficulty.strip().lower() == '1':
		with open('../words.txt', 'r') as file:
			content = file.read()
		select_mode()
	elif difficulty.strip().lower() == '2':
		with open('../words25k.txt', 'r') as file:
			content = file.read()
		select_mode()
	elif difficulty.strip().lower() == '3':
		with open('../wordscustom.txt', 'r') as file:
			content = file.read()
		select_mode()
	else:
		clear()
		print('invalid difficulty\n')
		select_difficulty()


def summary():
	global word_times, completed_words
	total_time = sum(word_times)
	average_time = total_time / num_words
	all_typed_entries = 0
	for word in completed_words:
		all_typed_entries += len(word)

	wpm = (all_typed_entries / 5) / (total_time / 60)

	clear()
	print(f'{Colors.GREY}--- --- typed words --- ---\n')

	index = 0
	for j in completed_words:
		print(f'{j} : {round(word_times[index], 2)}')
		index += 1

	print(f'\n--- --- --- --- --- --- ---{Colors.DEFAULT}\n\n')
	print(f'Average Time: {Colors.YELLOW}{round(average_time, 2)}{Colors.DEFAULT}')

	if wpm == 0:
		print('gtfo')
	elif wpm < 30:
		print(f'WPM: {Colors.RED}{round(wpm, 2)}{Colors.DEFAULT}')
		print(f'{Colors.GREY}* ni shi stoobid{Colors.DEFAULT}\n')
	elif wpm > 30 and wpm < 50:
		print(f'WPM: {Colors.RED}{round(wpm, 2)}{Colors.DEFAULT}')
		print(f"{Colors.GREY}* you're slow asf{Colors.DEFAULT}\n")
	elif wpm > 50 and wpm < 100:
		print(f'WPM: {Colors.YELLOW}{round(wpm, 2)}{Colors.DEFAULT}')
		print(f'{Colors.GREY}* average{Colors.DEFAULT}\n')
	elif wpm > 100 and wpm < 120:
		print(f'WPM: {Colors.GREEN}{round(wpm, 2)}{Colors.DEFAULT}')
		print(f'{Colors.GREY}* good{Colors.DEFAULT}\n')
	else:
		print(f'WPM: {Colors.PURPLE}{round(wpm, 2)}{Colors.DEFAULT}')
		print(f'{Colors.GREY}* touch grass{Colors.DEFAULT}\n')

	score = round((wpm * 100) - (average_time * 10))
	print(f'Your score is: {Colors.PURPLE}{score}{Colors.DEFAULT}\n\n')
	print(f'{Colors.GREY}--- --- --- --- --- --- ---{Colors.DEFAULT}\n')
	input('Press enter to continue')
	completed_words = []
	word_times = []
	select_difficulty()


# main function
def main():
	global start_game
	introduction()
	start_game = input(
		f'Start? ({Colors.GREEN}y{Colors.DEFAULT}/{Colors.RED}n{Colors.DEFAULT}/{Colors.PURPLE}bobo{Colors.DEFAULT})\n>>> '
	)
	if start_game.strip().lower() == 'y':
		select_difficulty()
	elif start_game.strip().lower() == 'bobo':
		print('ni shi bobo')
	else:
		clear()
		print(f'{Colors.RED}Invalid option{Colors.DEFAULT}\n')
		main()


# starting function
main()
