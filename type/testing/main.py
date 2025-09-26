import readchar as rc
import sys

print('Type something. Press SPACE to submit. Press ESC to quit.')

buffer = ''

while True:
	key = rc.readkey()

	if key == ' ':  # SPACE submits
		print(f'\nSubmitted: {buffer}')
		buffer = ''
		print('\nType something. Press SPACE to submit. Press ESC to quit.')
	elif key == '\x1b':  # ESC quits
		print('\nExiting...')
		break
	elif key == '\x7f':  # Backspace
		if buffer:
			buffer = buffer[:-1]
			sys.stdout.write('\b \b')  # erase last char
			sys.stdout.flush()
	else:
		buffer += key
		sys.stdout.write(key)  # echo typed character
		sys.stdout.flush()
