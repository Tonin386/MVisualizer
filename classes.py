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

