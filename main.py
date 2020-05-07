import pygame
import mido
import time

from pygame.locals import *
from classes import *
from random import randint

HEIGHT = 1920
WIDTH = 1080

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

	return notes

def createParticles(note):
	particles = []
	newParticlesCount = randint(10,20)

	for i in range(newParticlesCount):
		deg = randint(0,359)

		pos = [int(note.time_on)*100 % WIDTH, HEIGHT - (int((note.note - 21) * (HEIGHT/87) + randint(int(-HEIGHT/87), int(HEIGHT/87))))]

		acceleration = note.velocity/4
		accelerationDecay = acceleration/50

		color = pygame.Color(255, randint(0,255), 255)

		particles.append(Particle(acceleration, accelerationDecay, color, deg, pos))

	return particles

def moveParticles(particles):

	for p in particles:
		if p.acceleration <= 0:
			p.active = False
			particles.remove(p)

		coeffAccelerationY = (p.deg % 90) / 90
		coeffAccelerationX = 1 - coeffAccelerationY

		x = p.pos[0]
		y = p.pos[1]

		if p.deg < 90:
			x += p.acceleration * coeffAccelerationX
			y += p.acceleration * coeffAccelerationY
		if 90 <= p.deg < 180:
			x -= p.acceleration * coeffAccelerationX
			y += p.acceleration * coeffAccelerationY
		if 180 <= p.deg < 270:
			x -= p.acceleration * coeffAccelerationX
			y -= p.acceleration * coeffAccelerationY
		if 270 <= p.deg < 360:
			x += p.acceleration * coeffAccelerationX
			y -= p.acceleration * coeffAccelerationY

		p.pos = [int(x), int(y)]

		p.acceleration -= p.accelerationDecay

	return particles

def main():
	pygame.init()
	window = pygame.display.set_mode((HEIGHT,WIDTH), RESIZABLE)

	stop = False
	inport = None
	tick = time.perf_counter()

	notes = []
	particles = []

	try:
		inport = mido.open_input(mido.get_input_names()[0])
		print("Port opened: %s" % inport)
	except Exception as e:
		print("Error: %s" % e)
		stop = True
		return 2

	while not stop:
		tick = time.perf_counter() - tick
		pygame.time.Clock().tick(60)
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

		if tick > 0.01:
			for n in notes:
				if n.time_off == -1:
					particles += createParticles(n)
					
		notes = clean(notes, time.perf_counter())
		# print(len(notes))

		window.fill((0,0,0))

		for p in particles:
			if p.active:
				pygame.draw.circle(window, p.color, p.pos, 1)
		pygame.display.flip()

		particles = moveParticles(particles)

	# debug
	# for n in notes:
	# 	print(n)

	print("Program ended after %fs" % time.perf_counter())
	return 0

if __name__ == "__main__":
    # execute only if run as a script
    main()