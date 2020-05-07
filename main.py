import pygame
import mido
import time

from pygame.locals import *
from classes import *
from random import randint, uniform
from math import cos, sin, pi

WIDTH = 1920
HEIGHT = 1080

def findNoteIdx(note, notes):
	i = 0
	for n in notes:
		if n.note == note:
			if n.time_off == -1:
				return i
		i += 1

def clean(notes, now):
	for n in notes:
		if n.time_off != -1:
			if now - n.time_off > 2:
				notes.remove(n)

	return notes

def createParticles(note, r=-1, g=-1, b=-1):
	particles = []
	newParticlesCount = randint(5,10)

	if r == -1:
		r = randint(0,255)
	if g == -1:
		g = randint(0,255)
	if b == -1:
		b = randint(0,255)

	for i in range(newParticlesCount):
		rad = uniform(0,2*pi)

		pos = [int(time.perf_counter()*150) % WIDTH, HEIGHT - int(((note.note - 21) * (HEIGHT/87)))]

		acceleration = uniform(note.velocity/64, note.velocity/6)
		if acceleration < 1:
			acceleration = 1
		accelerationDecay = acceleration/100

		color = pygame.Color(r, g, b)

		particles.append(Particle(acceleration, accelerationDecay, color, rad, pos))

	return particles

def moveParticles(particles):

	for p in particles:
		if int(p.acceleration) <= 0:
			p.active = False
			particles.remove(p)
			continue

		coeffAccelerationX = cos(p.rad)
		coeffAccelerationY = sin(p.rad)

		x = p.pos[0] + p.acceleration * coeffAccelerationX
		y = p.pos[1] + p.acceleration * coeffAccelerationY

		p.pos = [int(x), int(y)]

		p.acceleration -= p.accelerationDecay

	return particles

def main():
	pygame.init()
	window = pygame.display.set_mode((WIDTH,HEIGHT), RESIZABLE)

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
			elif msg.type == "note_off":
				idx = findNoteIdx(msg.note, notes)
				notes[idx].setOff(time.perf_counter())

		if tick > 1/60:
			for n in notes:
				if n.time_off == -1:
					r = 0
					g = -1
					b = 150
					particles += createParticles(n, r, g, b)

		notes = clean(notes, time.perf_counter())
		# print(len(notes))

		window.fill((0,0,0))

		for p in particles:
			if p.active:
				pygame.draw.circle(window, p.color, p.pos, 3)
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