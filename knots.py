import functools, itertools

class Crossing:
	def __init__(self,pdinfo,arcs):
		self.i,self.j,self.k,self.l = pdinfo[:]
		if (self.j%arcs)+1 == self.l:
			self.rhr = -1
		else:
			self.rhr = 1
	def cc(self):
		if self.rhr > 0:
			self.i,self.j,self.k,self.l = self.l,self.i,self.j,self.k
		else:
			self.i,self.j,self.k,self.l = self.j,self.k,self.l,self.i
		self.rhr *= -1
	def __str__(self):
		return '{self.i},{self.j},{self.k},{self.l}'

class T:
	def __init__(self,c,e,i,n):
		self.t = [0]*n
		self.t[0] += i
		self.t[e] += c
	def __add__(self,other):
		new = T(0,0,0,max(len(self.t),len(other.t)))
		for i in range(len(self.t)):
			new.t[i] += self.t[i]
		for i in range(len(other.t)):
			new.t[i] += other.t[i]
		while len(new.t) > 1 and new.t[-1] == 0:
			del new.t[-1]
		return new
	def __sub__(self,other):
		new = T(0,0,0,max(len(self.t),len(other.t)))
		for i in range(len(self.t)):
			new.t[i] += self.t[i]
		for i in range(len(other.t)):
			new.t[i] -= other.t[i]
		while len(new.t) > 1 and new.t[-1] == 0:
			del new.t[-1]
		return new
	def __mul__(self,other):
		new = T(0,0,0,len(self.t)+len(other.t)-1)
		for i in range(len(self.t)):
			for j in range(len(other.t)):
				new.t[i+j] += self.t[i]*other.t[j]
		while len(new.t) > 1 and new.t[-1] == 0:
			del new.t[-1]
		return new
	def __str__(self):
		s = ""
		s += str(self.t[0])
		for i in range(1,len(self.t)):
			s += " + " + str(self.t[i]) + "t^" + str(i)
		return s

class GCode:
	def __init__(self,gaussCode):
		d = {}
		self.maxi = 1
		self.code = []
		for n in gaussCode:
			if abs(n) in d:
				self.code += [(-1 if n < 0 else 1)*d[abs(n)]]
			else:
				d[abs(n)] = self.maxi
				self.code += [(-1 if n < 0 else 1)*self.maxi]
				self.maxi += 1
		self.maxi -= 1
	def rmoves(self): # simplifying moves only for now
		moves = []
		d1 = [1,len(self.code)-1]
		for i in range(1,self.maxi+1):
			pos1 = self.code.index(i)
			pos2 = self.code.index(-i)
			if (pos1-pos2)%len(self.code) in d1:
				newcode = []
				for j in range(len(self.code)):
					if j not in [pos1,pos2]:
						newcode += [self.code[j]]
				moves += [GCode(newcode)]
		for i in range(1,self.maxi+1):
			pos1 = self.code.index(i-1 if i > 1 else self.maxi)
			pos2 = self.code.index(-(i-1 if i > 1 else self.maxi))
			pos3 = self.code.index(i)
			pos4 = self.code.index(-i)
			if (pos1-pos3)%len(self.code) in d1 and (pos2-pos4)%len(self.code) in d1:
				newcode = []
				for j in range(len(self.code)):
					if j not in [pos1,pos2,pos3,pos4]:
						newcode += [self.code[j]]
				moves += [GCode(newcode)]
		for combo in itertools.permutations(range(1,self.maxi+1),3):
			pos1 = self.code.index(combo[0])
			pos2 = self.code.index(-combo[0])
			pos3 = self.code.index(combo[1])
			pos4 = self.code.index(-combo[1])
			pos5 = self.code.index(combo[2])
			pos6 = self.code.index(-combo[2])
			if (pos1-pos3)%len(self.code) in d1 and (pos2-pos6)%len(self.code) in d1 and (pos4-pos5)%len(self.code) in d1:
				newcode = []
				for j in range(len(self.code)):
					if j == pos1:
						newcode += [combo[1]]
					elif j == pos2:
						newcode += [-combo[2]]
					elif j == pos3:
						newcode += [combo[0]]
					elif j == pos4:
						newcode += [combo[2]]
					elif j == pos5:
						newcode += [-combo[1]]
					elif j == pos6:
						newcode += [-combo[0]]
					else:
						newcode += [self.code[j]]
				moves += [GCode(newcode)]
		return moves
	def simplify(self,verbose=False):
		simp = GCode(self.code.copy())
		rlist = self.rmoves()
		tries = 0
		while rlist and tries < 100:
			simp = rlist[0]
			if verbose:
				print(simp.code)
			rlist = simp.rmoves()
			tries += 1
		return simp
	def is_alternating(self):
		for i in range(len(self.code)):
			if self.code[i-1]*self.code[i] > 0:
				return False
		return True
	def is_reduced(self):
		for i in range(1,self.maxi+1):
			pos1 = self.code.index(i)
			pos2 = self.code.index(-i)
			l = self.code[min(pos1,pos2)+1:max(pos1,pos2)]
			p = [(a,b) for a,b in itertools.permutations(l,2) if abs(a) == abs(b)]
			if len(l) == len(p):
				return False
		return True
	def is_unknot(self):
		simp = self.simplify()
		if (not simp.code):
			return 1
		elif simp.is_reduced() and simp.is_alternating():
			return -1
		return 0
	def __str__(self):
		return str(self.code)
		
# k = Diagram( ( (i,j,k,l),(i,j,k,l)... ) )
class Diagram:
	def __init__(self,pdcode):
		self.d = {} # maps crossing number to crossing
		i = 1
		for n in pdcode:
			c = Crossing(n,len(pdcode)*2)
			self.d[i] = c
			i += 1
	#def rcc(self,i): # RCC move on region i
		#for n in self.r[i]:
			#self.d[n].cc()
	def dtCode(self):
		pairs = {}
		for a in self.d:
			if self.d[a].i%2 == 1:
				if self.d[a].rhr > 0:
					pairs[self.d[a].i] = -(self.d[a].l)
				else:
					pairs[self.d[a].i] = -(self.d[a].j)
			elif self.d[a].rhr > 0:
				pairs[self.d[a].l] = self.d[a].i
			else:
				pairs[self.d[a].j] = self.d[a].i
		dtcode = []
		for a in sorted(pairs):
			dtcode += [pairs[a]]
		return dtcode
	def gaussCode(self):
		gcode = [0] * (2*len(self.d))
		for a in self.d:
			gcode[self.d[a].i-1] = -a
			if self.d[a].rhr < 0:
				gcode[self.d[a].j-1] = a
			else:
				gcode[self.d[a].l-1] = a
		return GCode(gcode)
	def isAlternating(self):
		dt = self.dtCode()
		for n in range(len(dt)):
			if dt[n-1]*dt[n] < 0:
			 return False
		return True
	def copy(self):
		return Knot(self.d.copy())
	def __str__(self):
		return str(self.d)
	def aPoly(self):
		if len(self.d) < 3:
			return T(0,0,1,1)
		gcode = self.gaussCode()
		m = [[T(0,0,0,1) for x in range(len(self.d))] for y in range(len(self.d))]
		a = 1
		for n in gcode.code:
			if n > 0:
				m[n-1][a-1] += T(-1,1,1,2)
			elif self.d[abs(n)].rhr > 0:
				m[abs(n)-1][a-1] += T(0,0,-1,1)
				a = (a%len(self.d)) + 1
				m[abs(n)-1][a-1] += T(1,1,0,2)
			else:
				m[abs(n)-1][a-1] += T(1,1,0,2)
				a = (a%len(self.d)) + 1
				m[abs(n)-1][a-1] += T(0,0,-1,1)
		del m[len(m)-1]
		for n in range(len(m)):
			del m[n][len(m)]
		apoly = self.det(m)
		#apoly = self.solve(m,T(0,0,1,1))
		i = 0
		while i < len(apoly.t) and apoly.t[i] == 0:
			i += 1
		if i > 0:
			for j in range(i,len(apoly.t)):
				apoly.t[j-i],apoly.t[j] = apoly.t[j],0
		while len(apoly.t) > 1 and apoly.t[-1] == 0:
			del apoly.t[-1]
		if apoly.t[0] < 0:
			for j in range(len(apoly.t)):
				apoly.t[j] *= -1
		return apoly
	def det(self,l):
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
			return(l[0][0]*l[1][1]-l[0][1]*l[1][0])
	def solve(self,matrix,mul):
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
				total += mul * self.solve(m, sign * matrix[0][i])
			return total
	def isUnknot(self):
		u = self.gaussCode().is_unknot()
		if u > 0:
			return 'Diagram is the unknot'
		elif u > 0:
			return 'Diagram is not the unknot'
		return 'Unable to determine'
	def isReduced(self):
		return self.gaussCode().is_reduced()
	def isAlternating(self):
		return self.gaussCode().is_alternating()
	def region_vectors(self):
		regions,d2,numc = set(),[],len(self.d)
		for a in range(1,numc+1):
			d2 += [self.d[a].i] + [self.d[a].j] + [self.d[a].k] + [self.d[a].l]
		for idx in range(len(d2)):
			reg,a,n = [0]*numc,idx,0
			reg[idx//4] = 1
			temp,d2[a] = d2[a],0
			b = d2.index(temp)
			d2[a] = temp
			reg[b//4] = 1
			if b%4 == 0:
				a = b+3
			else:
				a = b-1
			while a != idx:
				temp,d2[a] = d2[a],0
				b = d2.index(temp)
				d2[a] = temp
				reg[b//4] = 1
				if b%4 == 0:
					a = b+3
				else:
					a = b-1
			for y in range(numc):
				if reg[y] == 1:
					n += 2**(numc-y-1)
			regions.add(n)
		return regions
	def diameter(self):
		crossings = len(self.d)
		regions = self.region_vectors()	
		mod = 2**crossings
		real = {0}
		print('level 0:\n[' + bin(0)[2:].zfill(crossings) + ']\n\n' + 'level 1:')
		for i in regions:
			real.add(i) 
			print('[' + bin(i)[2:].zfill(crossings) + '] ')
		level = 1
		while len(real) < mod:
			level += 1
			print('\nlevel ' + str(level) + ': ')
			for combo in itertools.permutations(regions,level):
				x,y,s = [0]*crossings,0,""
				for i in range(level):
					if i > 0:
						s += " + "
					a = list(bin(combo[i])[2:].zfill(crossings))
					for j in range(crossings):
						x[j] += int(a[j])
						s += a[j]
				for i in range(crossings):
					if x[i]%2 == 1:
						y += 2**(crossings-i-1)
				if y not in real:
					print('[' + bin((y))[2:].zfill(crossings) + '] = ' + s)
					real.add(y)
		return level
	
		while len(list) < mod:
			level += 1
			buff = set()
			print('level ' + str(level) + ': ')
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(crossings))
					b = list(bin(j)[2:].zfill(crossings))
					for k in range(crossings):
						if a[k] != b[k]:				
							x += 2**(crossings-k-1)
					buff.add(x)
			for p in buff-real:
				print('[' + bin((p))[2:].zfill(crossings) + '] ')
			real.update(buff)
		return level

# call: i = diam( #crossings , (int1,int2,int3,...) )
# where ints are equal to int cast of region vectors (e.g. [1011] = 11)
def diam(crossings,regions):
		
	mod = 2**crossings
	real = {0}
	print('level 0:\n[' + bin(0)[2:].zfill(crossings) + ']\n\n' + 'level 1:')
	for i in regions:
		real.add(i) 
		print('[' + bin(i)[2:].zfill(crossings) + '] ')
	level = 1
	while len(real) < mod:
		level += 1
		print('\nlevel ' + str(level) + ': ')
		for combo in itertools.permutations(regions,level):
			x,y,s = [0]*crossings,0,""
			for i in range(level):
				if i > 0:
					s += " + "
				a = list(bin(combo[i])[2:].zfill(crossings))
				for j in range(crossings):
					x[j] += int(a[j])
					s += a[j]
			for i in range(crossings):
				if x[i]%2 == 1:
					y += 2**(crossings-i-1)
			if y not in real:
				print('[' + bin((y))[2:].zfill(crossings) + '] = ' + s)
				real.add(y)
	return level
	
	while len(list) < mod:
		level += 1
		buff = set()
		print('level ' + str(level) + ': ')
		for i in regions:
			for j in real:
				x = 0
				a = list(bin(i)[2:].zfill(crossings))
				b = list(bin(j)[2:].zfill(crossings))
				for k in range(crossings):
					if a[k] != b[k]:				
						x += 2**(crossings-k-1)
				buff.add(x)
		for p in buff-real:
			print('[' + bin((p))[2:].zfill(crossings) + '] ')
		real.update(buff)
	return level

								