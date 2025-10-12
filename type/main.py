"""
bobotype - v1

created by wndx2 (sleepywndud) and caibirana2-eng

"""

# imports
import os
import sys
import random
import time
import termios


class Colors:
	# print(f'{Colors.BLUE}Enter text here{Colors.DEFAULT}')
	# https://gist.github.com/iamnewton/8754917 <-- for a list of full color codes
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
	'ni meiyou baba',
	'ni shi gae',
]


# terminal clearing function for cleaner output
def clear():
	# windows
	if os.name == 'nt':
		os.system('cls')
	# mac/linux
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


# introduction
def introduction():
	print(f'{Colors.CYAN}Welcome to BOBOTYPE!{Colors.DEFAULT}\n')
	print(f"You type the word/sentence that's printed in {Colors.BLUE}blue{Colors.DEFAULT}.")
	print(f'Press {Colors.GREY}"enter"{Colors.DEFAULT} once you are done typing to submit your input.\n')
	print('Your score will be calculated based on your WPM and average speed.')
	print('Please note that your WPM may not be accurate when typing singular words!\n\n')


# prints the difficulty selecting screen
def select_difficulty():
	global difficulty, content

	clear()

	print(
		f'Select Difficulty:\n{Colors.GREEN}1. Easy\n{Colors.RED}2. Hard\n{Colors.PURPLE}3. Custom{Colors.DEFAULT}'
	)
	print(
		f"{Colors.GREY}Or, click '{Colors.CYAN}0{Colors.GREY}' to return to the main menu{Colors.DEFAULT}\n"
	)
	difficulty = input('>>> ')

	if difficulty.strip().lower() not in ['0', '1', '2', '3']:
		clear()

		print('invalid difficulty(1)\n')
		select_difficulty()

	# reads the corresponding txt file depending on input
	elif difficulty.strip().lower() == '0':  # return to main menu
		clear()
		print('main menu')
		main()

	elif difficulty.strip().lower() == '1':
		with open('words.txt', 'r') as file:
			content = file.read()
		select_mode()

	elif difficulty.strip().lower() == '2':
		with open('words25k.txt', 'r') as file:
			content = file.read()
		select_mode()

	elif difficulty.strip().lower() == '3':
		with open('wordscustom.txt', 'r') as file:
			content = file.read()
		select_mode()

	else:
		clear()
		print('invalid difficulty\n')
		select_difficulty()


# prints the mode selecting screen (mode refers to word/sentence--more to be added in the future)
def select_mode():
	global mode, word_list_length, completed_words, word_times, num_words, word_list, word_times

	clear()

	# makes the .txt file into a variable
	word_list = content.split()
	# counts how many words are in the .txt file
	word_list_length = int(len(word_list)) - 1
	# initializes the two lists used for counting how many words are accurately typed
	completed_words = []
	word_times = []
	print('Select Mode:\n')
	print(f'{Colors.GREEN}1. Word(s)')
	print(f'{Colors.BLUE}2. Sentence')
	print(f'{Colors.YELLOW}3. Endurance\n')
	mode = input(f'{Colors.DEFAULT}\n>>> ')

	if mode.strip() == '1':  # words
		clear()
		num_words = int(input('How many words? \n\n>>> '))
		# invalidates negative, or 0 word counts (zero div error)
		if num_words <= 0:
			clear()

			print('ni meiyou baba\n')
			# returns the user back to mode-selecting menu
			select_mode()

		else:
			run_words()

	elif mode.strip() == '2':  # sentences
		run_sentences()

	elif mode.strip() == '3':  # endurance
		run_endurance()


# prints the words and checks if it's correct--repeats until the two lists are equal
def run_words():
	global word_list, word_times, completed_words

	if len(completed_words) < num_words:
		generate()

		clear()

		print('\nWORD:')
		print(f'>>> {Colors.BLUE}{current_word}{Colors.DEFAULT}')
		countdown()

		start_time = time.time()
		user_input = input('>>> ')
		# calculates the elapsed time
		elapsed_time = time.time() - start_time

		if user_input == current_word:  # correct
			print(f'{Colors.GREEN}\n\nCorrect!{Colors.DEFAULT}')
			# prints the time, and appends the typed word into the completed_words list
			# the completed_words list is later used for len-ing later
			print(f'Time taken: {elapsed_time:.2f} seconds\n\n')
			completed_words.append(user_input)
			word_times.append(elapsed_time)
			time.sleep(2)
		else:  # incorrect
			print(f'{Colors.RED}\n\nFailed!{Colors.DEFAULT}')
			# prints a heartwarmimg message when wrong
			print(
				f'{Colors.GREY}{heartwarming_messages[int(random.randint(0, len(heartwarming_messages) - 1))]}{Colors.DEFAULT}'
			)
			time.sleep(2)
		run_words()  # repeats until len of both lists are equal

	else:
		# prints the summary when the len of both lists are equal
		# time calculation
		total_time = sum(word_times)
		average_time = total_time / num_words
		all_typed_entries = 0

		for word in completed_words:
			all_typed_entries += len(word)

		# calculating wpm
		wpm = (all_typed_entries / 5) / (total_time / 60)

		# prints the words that are typed
		clear()

		print(f'{Colors.GREY}--- --- typed words --- ---\n')

		index = 0
		for j in completed_words:
			print(f'{j} : {round(word_times[index], 2)}')
			index += 1

		print(f'\n--- --- --- --- --- --- ---{Colors.DEFAULT}\n\n')
		print(f'Average Time: {Colors.YELLOW}{round(average_time, 2)}{Colors.DEFAULT}')

		# output comments depending on wpm
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

		# calculates score
		score = round((wpm * 100) - (average_time * 10))
		print(f'Your score is: {Colors.PURPLE}{score}{Colors.DEFAULT}\n\n')
		print(f'{Colors.GREY}--- --- --- --- --- --- ---{Colors.DEFAULT}\n')
		input('Press enter to continue')
		completed_words = []
		word_times = []

		# restarts--sends the user back to the start where they select the difficulty
		select_difficulty()


def run_sentences():
	global sentence, user_input, elapsed_time, num_words

	clear()
	num_words = int(input('How many words? \n\n>>> '))
	sentence = []

	for m in range(num_words):
		random_index = random.randint(0, word_list_length)
		sentence.append(word_list[random_index].lower())
	sentence = ' '.join(sentence)

	clear()

	print('\nSENTENCE:')
	print(f'>>> {Colors.BLUE}{sentence}{Colors.DEFAULT}')
	countdown()

	start_time = time.time()
	user_input = input('>>> ')
	elapsed_time = time.time() - start_time

	if user_input.lower() == sentence.lower():
		print(f'{Colors.GREEN}\n\nCorrect!{Colors.DEFAULT}')
		print(f'Time taken: {elapsed_time:.2f} seconds\n\n')
		time.sleep(2)

		# time calculation
		total_time = elapsed_time
		all_typed_entries = len(sentence)

		# calculating wpm
		wpm = (all_typed_entries / 5) / (total_time / 60)

		# prints the sentence that is typed
		clear()

		print(f'{Colors.GREY}--- --- --- --- --- --- ---\n')

		print(sentence)

		print(f'\n--- --- --- --- --- --- ---{Colors.DEFAULT}\n\n')
		print(f'Average Time: {Colors.YELLOW}{round(total_time, 2)}{Colors.DEFAULT}')

		# output comments depending on wpm
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

		# calculates score
		score = round((wpm * 100) - (total_time * 10))
		print(f'Your score is: {Colors.PURPLE}{score}{Colors.DEFAULT}\n\n')
		print(f'{Colors.GREY}--- --- --- --- --- --- ---{Colors.DEFAULT}\n')
		input('Press enter to continue')
		sentence = []

		# restarts--sends the user back to the start where they select the difficulty
		select_difficulty()

	else:
		print(f'{Colors.RED}\n\nFailed!{Colors.DEFAULT}')
		print(
			f'{Colors.GREY}{heartwarming_messages[int(random.randint(0, len(heartwarming_messages) - 1))]}{Colors.DEFAULT}'
		)
		time.sleep(2)
		select_difficulty()


def run_endurance():
	global current_sentence, next_sentence

	# plan is to generate two sentences at once; when current_sentence is complete
	# make next_sentence == current_sentence, then re-generate next_sentence, then repeat
	current_sentence = []
	next_sentence = []

	# change to user input later on
	time_limit = 30
	current_time = 30

	for m in range(10):
		random_index = random.randint(0, word_list_length)
		current_sentence.append(word_list[random_index].lower())

		random_index = random.randint(0, word_list_length)
		next_sentence.append(word_list[random_index].lower())

	current_sentence = ' '.join(current_sentence)
	next_sentence = ' '.join(next_sentence)

	# fuck this shit
	while current_time != time_limit:
		clear()
		print('ENDURANCE:')
		print(f'>>> {Colors.BLUE}{current_sentence}')
		print(f'{Colors.GREY}{next_sentence}{Colors.DEFAULT}')

		if user_input.lower() == current_sentence.lower():
			next_sentence == current_sentence

			for m in range(10):
				random_index = random.randint(0, word_list_length)
				next_sentence.append(word_list[random_index].lower())


# main function that starts--each function leads to another function
# so it works in harmony basically
def main():
	global start_game

	# clears the screen before starting
	clear()

	introduction()

	start_game = input(f'Start? ({Colors.GREEN}y{Colors.DEFAULT}/{Colors.RED}n{Colors.DEFAULT})\n\n>>> ')
	if start_game.strip().lower() == 'y':
		select_difficulty()

	elif start_game.strip().lower() == 'n':
		clear()
		print('you gotta play')
		time.sleep(1)
		clear()
		main()

	# easter eggs
	elif (
		start_game.strip().lower() == ''
		or start_game.strip().lower() == 'bobo'
		or start_game.strip().lower() == 'wenbo'
		or start_game.strip().lower() == 'no u'
	):
		# fat spammer
		while True:
			print(heartwarming_messages[int(random.randint(0, len(heartwarming_messages) - 1))])
			time.sleep(0.05)

	else:
		clear()
		print(f'{Colors.RED}Invalid option{Colors.DEFAULT}\n')
		main()


# starting function
main()
