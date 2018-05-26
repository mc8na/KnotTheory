import functools, itertools

class Crossing:
	def __init__(self,pdinfo,arcs):
		self.index,self.i,self.j,self.k,self.l = pdinfo[:]
		if (self.j%arcs)+1 == self.l:
			self.rhr = -1
		else:
			self.rhr = 1
	def __str__(self):
		return '{self.index},{self.i},{self.j},{self.k},{self.i}'

class Knot:
	def __init__(self,pdcode):
		self.d = {}
		for n in pdcode:
			c = Crossing(n,len(pdcode)*2)
			self.d[c.i] = c
	def dtCode(self):
		pairs = {}
		for a in self.d:
			if a%2 == 1:
				if self.d[a].rhr > 0:
					pairs[a] = -(self.d[a].l)
				else:
					pairs[a] = -(self.d[a].j)
			elif self.d[a].rhr > 0:
				pairs[self.d[a].l] = a
			else:
				pairs[self.d[a].j] = a
		dtcode = []
		for a in sorted(pairs):
			dtcode += pairs[a]
		return dtcode
	def gaussCode(self):
		list = dtCode(self)
		t = []
		for n in range(1,len(list)+1):
			t += 2*n-1
			t += list[n-1]
		gcode = [0] * len(t)
		#for n in range(len(t)):
		#	gcode += 0
		for n in t:
			if n%2 == 1: # n is odd
				if n <= len(t)//2: # first time through a crossing
					if t[n+1] > 0: # over crossing
						gcode[n] = n
					else:		   # under crossing
						gcode[n] = -n
				elif t[n+1] > 0:   # second time through a crossing
					gcode[n] = t[n+1] # over the pair
				else:				# under the pair
					gcode[n] = -t[n+1]
			else: #n is even
				if n > 0 and n <= len(t)//2: # first time under
					gcode[n] = -n
				elif n > 0: # under crossing second time through
					gcode[n] = -t[n-1]
				elif abs(n) <= len(t)//2: # first time over
					gcode[abs(n)] = abs(n)
				else: # over crossing second time through
					gcode[abs(n)] = t[n-1]
		return gcode
	def isAlternating(self):
		dt = dtCode(self)
		for n in range(len(dt)):
			if dt[n-1]*dt[i] > 0:
			 return False
		return True
	def copy(self):
		return Knot(self.d.copy())
	def __str__(self):
		return str(self.d)
		