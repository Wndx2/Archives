import time

print('Stopwatch started. Press Ctrl+C to stop.')

start_time = time.time()  # record the start time

try:
	while True:
		elapsed = time.time() - start_time  # elapsed time in seconds (float)
		minutes = int(elapsed // 60)
		seconds = int(elapsed % 60)
		milliseconds = int((elapsed - int(elapsed)) * 1000)  # get milliseconds
		print(f'\r{minutes:02d}:{seconds:02d}:{milliseconds:03d}', end='')
		time.sleep(0.01)  # update every 10ms for smoother display
except KeyboardInterrupt:
	print('\nStopwatch stopped.')
