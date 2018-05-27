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

class T:
	def __init__(self,c,e,i,n):
		self.t = [0]*n
		self.t[0] += i
		self.t[e] += c
	def __add__(self,other):
		new = T(0,0,0,max(len(self.t),len(other.t)))
		for i in range(len(self.t)):
			new[i] += self.t[i]
		for i in range(len(other.t)):
			new[i] += other.t[i]
		return new
	def __sub__(self,other):
		new = T(0,0,0,max(len(self.t),len(other.t)))
		for i in range(len(self.t)):
			new[i] += self.t[i]
		for i in range(len(other.t)):
			new[i] -= other.t[i]
		return new
	def __mul__(self,other):
		new = T(0,0,0,len(self.t)+len(other.t)-1)
		for i in range(len(self.t)):
			for j in range(len(other.t)):
				new[i+j] += self.t[i]*other.t[j]
		return new
	def __str__(self):
		s = ""
		for i in range(len(self.t)):
			s += str(i) + "t^" + str(self.t[i]) + " "
		return s

class Knot:
	def __init__(self,pdcode):
		self.d = {}
		i = 1
		for n in pdcode:
			c = Crossing(n,len(pdcode)*2)
			self.d[i] = c
			i += 1
	def dtCode(self):
		pairs = {}
		for a in self.d:
			if self.d[a].i%2 == 1:
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
	def aPoly(self):
		gcode = gaussCode(self)
		m = [[T(0,0,0,1) for x in range(len(self.d))] for y in range(len(self.d))]
		a = 1
		for n in gcode:
			if n > 0:
				m[n][a] += T(-1,1,1,2)
			elif self.d[n].rhr > 0:
				m[n][a] += T(0,0,-1,2)
				a += a%len(self.d) + 1
				m[n][a] += T(1,1,0,2)
			else:
				m[n][a] += T(1,1,0)
				a += a%len(self.d) + 1
				m[n][a] += T(0,0,-1,1)
		del m[len(m)-1]
		for n in range(len(m)):
			del m[n][len(m)]
		return det(m)
		#return solve(m,1)
	def det(l):
		n = len(l)
		if (n>2):
			i,t,sum = T(0,0,1,1),0,T(0,0,0,1)
			while t <= n-1:
				d = {}
				t1 = 1
				while t1 <= n-1:
					m = 0
					d[t1] = []
					while m <= n-1:
						if (m == t):
							u = 0
						else:
							d[t1].append(m[t1][m])
						m += 1
					t1 += 1
				l1 = [d[x] for x in d]
				sum = sum + i*(l[0][t])*(det(l1))
				i = i*T(0,0,-1,1)
				t += 1
			return sum
		else:
			return(m[0][0]*m[1][1]-m[0][1]*m[1][0])
	def solve(matrix,mul):
		width = len(matrix)
		if width == 1:
			return mul * matrix[0][0]
		else:
			sign = T(0,0,-1,1)
			total = T(0,0,0,1)
			for i in range(width):
				m = []
				for j in range(1,width):
					buff = []
					for k in range(width):
						if k != i:
							buff.append(matrix[j][k])
					m.append(buff)
				sign *= T(0,0,-1,1)
				total += mul * solve(m, sign * matrix[0][i])
			return total
					
		