import functools, itertools, copy

class Crossing: # Crossing for pdcode, holds i,j,k,l and sign (right hand rule)
	def __init__(self,pdinfo,arcs):
		self.i,self.j,self.k,self.l = pdinfo[:]
		if (self.j%arcs)+1 == self.l:
			self.rhr = -1
		else:
			self.rhr = 1

# k = Torus( ( (i,j,k,l),(i,j,k,l)... ) )
class Torus:
	def __init__(self,pdcode):
		self.d = {} # maps crossing number to crossing
		i = 1
		for n in pdcode:
			c = Crossing(n,len(pdcode)*2)
			self.d[i] = c
			i += 1
	def __str__(self): # returns the PD Code of the Diagram in string form
		s = "["
		for key in self.d:
			if key != 1:
				s += ","
			s += str(self.d[key])
		s += ']'
		return s
	def code(self):
		code = []
		for i in range(1,len(self.d)+1):
			code += [self.d[i].i] + [self.d[i].j] + [self.d[i].k] + [self.d[i].l]
		return code
	def numComponents(self):
		maxi,components,code = 1,0,self.code()
		while maxi <= 2*len(self.d):
			components += 1
			i1 = code.index(maxi)
			code[i1] = 0
			i2 = code.index(maxi)
			code[i1] = maxi
			if i1%4 < 2:
				j1 = i1+2
			else:
				j1 = i1-2
			if i2%4 < 2:
				j2 = i2+2
			else:
				j2 = i2-2
			maxi = max(code[j1],code[j2])+1
		return components	
	def region_vectors(self): # returns set of integers corresponding to region vectors of diagram
		regions,code,numc = set(),self.code(),len(self.d)
		for idx in range(len(code)):
			reg,a,n = [0]*numc,idx,0
			temp,code[a] = code[a],0
			b = code.index(temp)
			code[a] = temp
			reg[b//4] = (reg[b//4]+1)%2
			if b%4 == 0:
				a = b+3
			else:
				a = b-1
			while a != idx:
				temp,code[a] = code[a],0
				b = code.index(temp)
				code[a] = temp
				reg[b//4] = (reg[b//4]+1)%2
				if b%4 == 0:
					a = b+3
				else:
					a = b-1
			for y in range(numc):
				if reg[y] == 1:
					n += 2**(numc-y-1)
			regions.add(n)
		return regions
	def diameter(self): # computes max number of RCCs to realize all sets of crossing changes
		regions,real,numc = self.region_vectors(),{0},len(self.d)
		mod = 2**(numc)
		real.update(regions)
		level = 1
		while level < numc+2:
			level += 1
			buff = set()
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(numc))
					b = list(bin(j)[2:].zfill(numc))
					for k in range(numc):
						if a[k] != b[k]:				
							x += 2**(numc-k-1)
					buff.add(x)
			real.update(buff)
		print(str(len(real)) + '/' + str(mod) + ' diagrams realized')
		return level
	def shimizu_region_vectors(self):
		regions,code,numc = set(),self.code(),len(self.d)
		for idx in range(len(code)):
			reg,a,n = [0]*numc,idx,0
			temp,code[a] = code[a],0
			b = code.index(temp)
			code[a] = temp
			reg[b//4] = 1
			if b%4 == 0:
				a = b+3
			else:
				a = b-1
			while a != idx:
				temp,code[a] = code[a],0
				b = code.index(temp)
				code[a] = temp
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
	def shimizu_diameter(self):
		regions,real,numc = self.shimizu_region_vectors(),{0},len(self.d)
		mod = 2**(numc)
		real.update(regions)
		level = 1
		while level < numc+2:
			level += 1
			buff = set()
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(numc))
					b = list(bin(j)[2:].zfill(numc))
					for k in range(numc):
						if a[k] != b[k]:				
							x += 2**(numc-k-1)
					buff.add(x)
			real.update(buff)
		print(str(len(real)) + '/' + str(mod) + ' diagrams realized')
		return level
	def ediameter(self): # prints each set of crossing changes as sum of fewest number of region vectors
		regions,real,numc = self.region_vectors(),{0},len(self.d)
		mod = 2**(numc)
		print('level 0:\n[' + bin(0)[2:].zfill(numc) + ']\n\n' + 'level 1:')
		for i in regions:
			real.add(i) 
			print('[' + bin(i)[2:].zfill(numc) + '] ')
		level = 1
		while level < numc+2:
			level += 1
			print('\nlevel ' + str(level) + ': ')
			for combo in itertools.combinations(regions,level):
				x,y,s = [0]*numc,0,""
				for i in range(level):
					if i > 0:
						s += " + "
					a = list(bin(combo[i])[2:].zfill(numc))
					for j in range(numc):
						x[j] += int(a[j])
						s += a[j]
				for i in range(numc):
					if x[i]%2 == 1:
						y += 2**(numc-i-1)
				if y not in real:
					print('[' + bin((y))[2:].zfill(numc) + '] = ' + s)
					real.add(y)
		print(str(len(real)) + '/' + str(mod) + ' diagrams realized')
		return level
	def distance(self,d): # computes minimum number of RCCs to effect set of crossing changes d
		regions = self.region_vectors()
		real,level,numc = {0},0,len(self.d)
		while d not in real:
			level += 1
			buff = set()
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(numc))
					b = list(bin(j)[2:].zfill(numc))
					for k in range(numc):
						if a[k] != b[k]:				
							x += 2**(numc-k-1)
					if x == d:
						return level
					buff.add(x)
			real.update(buff)
		print('Error: diagram not found')
		return level
	def mirror_distance(self): # computes minimum number of RCCs to change all crossings
		mod = 2**(len(self.d))-1
		return self.distance(mod)
	def black_white(self):
		vectors,code,numc,b,w = [],self.code(),len(self.d),0,0
		black,white,usedb,usedw = {0,2},{1,3},set(),set()
		while black or white:
			s,reg = "",[0]*numc
			if black:
				b += 1
				idx = i = black.pop()
				usedb.add(idx)
				temp,code[i] = code[i],0
				j = code.index(temp)
				code[i] = temp
				reg[j//4] = (reg[j//4]+1)%2
				#reg[j//4] = 1
				white.add(j)
				if j%4 == 0:
					i = j+3
				else:
					i = j-1
				usedb.add(i)
				while i != idx:
					temp,code[i] = code[i],0
					j = code.index(temp)
					code[i] = temp
					reg[j//4] = (reg[j//4]+1)%2
					#reg[j//4] = 1
					white.add(j)
					if j%4 == 0:
						i = j+3
					else:
						i = j-1
					usedb.add(i)
			else:
				w += 1
				idx = i = white.pop()
				usedw.add(idx)
				temp,code[i] = code[i],0
				j = code.index(temp)
				code[i] = temp
				reg[j//4] = (reg[j//4]+1)%2
				#reg[j//4] = 1
				black.add(j)
				if j%4 == 0:
					i = j+3
				else:
					i = j-1
				usedw.add(i)
				while i != idx:
					temp,code[i] = code[i],0
					j = code.index(temp)
					code[i] = temp
					reg[j//4] = (reg[j//4]+1)%2
					#reg[j//4] = 1
					black.add(j)
					if j%4 == 0:
						i = j+3
					else:
						i = j-1
					usedw.add(i)
			for r in reg:
				s += str(r)
			vectors.append(s)
			if black&usedw or white&usedb:
				return set()
			white = white-usedw
			black = black-usedb
		print('Diagram contains ' + str(b) + ' black regions and ' + str(w) + ' white regions')
		for v in vectors:
			print(v)
		return vectors

t = {}
t[1] = Torus(((1,5,2,4),(2,6,3,5),(3,6,4,1)))
t[2] = Torus(((1,5,2,4),(2,8,3,7),(3,8,4,9),(5,1,6,10),(6,9,7,10)))
t[3] = Torus(((1,14,2,15),(2,10,3,9),(3,17,4,16),(4,12,5,11),(5,12,6,13),(6,17,7,18),(7,10,8,11),(8,15,9,16),(13,18,14,1)))
t[4] = Torus(((1,8,2,9),(2,5,3,6),(3,1,4,10),(4,8,5,7),(6,10,7,9)))
t[5] = Torus(((1,13,2,12),(2,12,3,11),(3,7,4,6),(4,9,5,10),(5,11,6,10),(7,1,8,14),(8,13,9,14)))		
t[6] = Torus(((1,5,2,4),(2,7,3,8),(3,7,4,6),(5,1,6,8)))
t[7] = Torus(((1,7,2,6),(2,8,3,7),(3,5,4,8),(4,6,1,5)))
