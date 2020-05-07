import pygame
import mido
import time

from pygame.locals import *
from classes import GNote

def findNoteIdx(note, notes):
	i = 0
	for n in notes:
		if n.note == note:
			if not n.time_off == -1:
				return i
			else:
				i += 1
	return -1

def clean(notes, now):
	for n in notes:
		if n.time_off != -1:
			if now - n.time_off > 5:
				notes.remove(n)

def main():
	pygame.init()
	window = pygame.display.set_mode((640,480), RESIZABLE)

	stop = False
	inport = None

	notes = []

	try:
		inport = mido.open_input(mido.get_input_names()[0])
		print("Port opened: %s" % inport)
	except Exception as e:
		print("Error: %s" % e)
		stop = True
		return 2

	while not stop:
		for event in pygame.event.get():
			if event.type == QUIT:
				stop = True
				break
			# if event.type == KEYDOWN:
			# 	if event.key == K_KEY:
					#do something

		for msg in inport.iter_pending():
			if msg.type == "note_on":
				notes.append(GNote(msg, time.perf_counter()))
			else:
				idx = findNoteIdx(msg.note, notes)
				notes[idx].setOff(time.perf_counter())

		clean(notes, time.perf_counter())
		# print(len(notes))

		pygame.display.flip()

	# debug
	# for n in notes:
	# 	print(n)

	print("Program ended after %fs" % time.perf_counter())
	return 0

if __name__ == "__main__":
    # execute only if run as a script
    main()