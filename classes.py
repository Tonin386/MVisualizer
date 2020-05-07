class GNote:
	time_off = -1
	def __init__(self, msg, time_on):
		self.note = msg.note
		self.velocity = msg.velocity
		self.time_on = time_on

	def setOff(self, time_off):
		self.time_off = time_off

	def __str__(self):
		return "Note %d played from %f to %f at %d velocity." % (self.note, self.time_on, self.time_off, self.velocity)

class Particle:
	def __init__(self, acceleration=10, accelerationDecay=0.001, color=(255,255,255), rad=0, pos=(0,0)):
		self.acceleration = acceleration
		self.accelerationDecay = accelerationDecay
		self.color = color
		self.rad = rad
		self.pos = pos
		self.active = True

	def setOff(self):
		self.active = False

	def __str__(self):
		return "Particle at (%d;%d)" % (self.pos[0], self.pos[1])
