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
	def black_white(self):
		vectors,code,numc,b,w = [],[],len(self.d),0,0
		for i in range(1,numc+1):
			code += [self.d[i].i] + [self.d[i].j] + [self.d[i].k] + [self.d[i].l]
		black,white,used = {0,2},{1,3},set()
		while black or white:
			s,reg = "",[0]*numc
			if black:
				b += 1
				idx = i = black.pop()
				used.add(idx)
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
				used.add(i)
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
					used.add(i)
			else:
				w += 1
				idx = i = white.pop()
				used.add(idx)
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
				used.add(i)
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
					used.add(i)
			for r in reg:
				s += str(r)
			vectors.append(s)
			white = white-used
			black = black-used
		print('Diagram contains ' + str(b) + ' black regions and ' + str(w) + ' white regions')
		for v in vectors:
			print(v)
		return vectors
	def region_vectors(self): # returns set of integers corresponding to region vectors of diagram
		regions,code,numc = set(),[],len(self.d)
		for i in range(1,numc+1):
			code += [self.d[i].i] + [self.d[i].j] + [self.d[i].k] + [self.d[i].l]
		for idx in range(len(code)):
			reg,a,n = [0]*numc,idx,0
			temp,code[a] = code[a],0
			b = code.index(temp)
			code[a] = temp
			reg[b//4] = (reg[b//4]+1)%2
			#reg[b//4] = 1
			if b%4 == 0:
				a = b+3
			else:
				a = b-1
			while a != idx:
				temp,code[a] = code[a],0
				b = code.index(temp)
				code[a] = temp
				reg[b//4] = (reg[b//4]+1)%2
				#reg[b//4] = 1
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
		crossings = len(self.d)
		regions = self.region_vectors()
		mod = 2**(crossings)
		real = {0}
		real.update(regions)
		level = 1
		while level < crossings+2:
			level += 1
			buff = set()
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(crossings))
					b = list(bin(j)[2:].zfill(crossings))
					for k in range(crossings):
						if a[k] != b[k]:				
							x += 2**(crossings-k-1)
					buff.add(x)
			real.update(buff)
		#print(str(len(real)) + '/' + str(mod) + ' diagrams realized')
		return level
	def ediameter(self): # prints each set of crossing changes as sum of fewest number of region vectors
		crossings = len(self.d)
		regions = self.region_vectors()
		mod = 2**(crossings)
		real = {0}
		print('level 0:\n[' + bin(0)[2:].zfill(crossings) + ']\n\n' + 'level 1:')
		for i in regions:
			real.add(i) 
			print('[' + bin(i)[2:].zfill(crossings) + '] ')
		level = 1
		while level < crossings+2:
			level += 1
			print('\nlevel ' + str(level) + ': ')
			for combo in itertools.combinations(regions,level):
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
		print(str(len(real)) + '/' + str(mod) + ' diagrams realized')
		return level
	def distance(self,d): # computes minimum number of RCCs to effect set of crossing changes d
		regions = self.region_vectors()
		real,level,crossings = {0},0,len(self.d)
		while d not in real:
			level += 1
			buff = set()
			for i in regions:
				for j in real:
					x = 0
					a = list(bin(i)[2:].zfill(crossings))
					b = list(bin(j)[2:].zfill(crossings))
					for k in range(crossings):
						if a[k] != b[k]:				
							x += 2**(crossings-k-1)
					if x == d:
						return level
					buff.add(x)
			real.update(buff)
		print('Error: diagram not found')
		return level
	def mirror_distance(self): # computes minimum number of RCCs to change all crossings
		mod = 2**(len(self.d))-1
		return self.distance(mod)
