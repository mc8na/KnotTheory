# Filename: torus.py
# Author: Miles Clikeman
#
# Contains code to find the number of components, checkerboard shading, region vectors, and diameter of knot diagrams embedded on a torus.

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
	def numComponents(self): # returns the number of components of the link diagram
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
					n += 1<<(numc-y-1)
			regions.add(n)
		return regions
	def diameter(self): # computes max number of RCCs to realize all sets of crossing changes
		numc,regions,power = len(self.d),self.region_vectors(),1<<(numc-self.components+1)
		new = list(regions)
		real = [False]*power
		real[0] = True
		for r in regions:
			real[r] = True
		level,numreal = 1,len(regions)+1
		while numreal < power and level < numc+3:
			level += 1
			buff = []
			for i in regions:
				for j in new:
					x = i^j
					if not real[x]:
						real[x] = True
						numreal += 1
						buff = buff+[x]
			new = buff
		print(str(numreal) + '/' + str(power) + ' diagrams realized')
		return level
	def shimizu_region_vectors(self): # computes region vectors where reducible region counts twice
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
					n += 1<<(numc-y-1)
			regions.add(n)
		return regions
	def shimizu_diameter(self): # diameter of the diagram for Shimizu RCC
		numc,regions,power = len(self.d),self.shimizu_region_vectors(),1<<(numc-self.components+1)
		new = list(regions)
		real = [False]*power
		real[0] = True
		for r in regions:
			real[r] = True
		level,numreal = 1,len(regions)+1
		while numreal < power and level < numc+3:
			level += 1
			buff = []
			for i in regions:
				for j in new:
					x = i^j
					if not real[x]:
						real[x] = True
						numreal += 1
						buff = buff+[x]
			new = buff
		print(str(numreal) + '/' + str(power) + ' diagrams realized')
		return level
	def ediameter(self): # prints each set of crossing changes as sum of fewest number of region vectors
		numc = len(self.d)
		regions = self.region_vectors()
		power = 1<<(numc-self.components+1)
		real = [False]*power
		real[0] = True
		print('level 0:\n[' + bin(0)[2:].zfill(numc) + ']\n\n' + 'level 1:')
		for i in regions:
			real[i] = True 
			print('[' + bin(i)[2:].zfill(numc) + '] ')
		numreal = len(regions)+1
		level = 1
		while numreal < power and level < numc+2:
			level += 1
			print('\nlevel ' + str(level) + ': ')
			for combo in itertools.combinations(regions,level): # try adding all combinations of a certain number of region vectors
				x = 0
				for i in range(level): # symmetric difference of all rcc vectors
					x = x^combo[i]
				if not real[x]: # realized new diagram
					real[x] = True
					numreal += 1
					s = ""
					for i in range(level):
						if i > 0:
							s += " + "
						s += bin((combo[i]))[2:].zfill(numc)
					print('[' + bin((x))[2:].zfill(numc) + "] = " + s) # print out diagram vector and rcc vectors
		print(str(numreal) + '/' + str(power) + ' diagrams realized')
		return level
	def distance(self,d): # computes minimum number of RCCs to effect set of crossing changes d
		regions = self.region_vectors()
		numc = len(self.d)
		for level in range(numc+2):
			for combo in itertools.combinations(regions,level):
				x = 0
				for i in range(level):
					x = x^combo[i]
				if x == d:
					return level
		print('Error: diagram not found')
		return level
	def mirror_distance(self): # computes minimum number of RCCs to change all crossings
		mod = 1<<(len(self.d))-1
		return self.distance(mod)
	def black_white(self): # returns black and white regions from checkerboard shading of the diagram
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
				#reg[j//4] = 1 # for shimizu's rcc definition
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
t[8] = Torus(((1,4,2,3),(2,3,1,4)))
t[9] = Torus(((1,9,2,8),(2,14,3,13),(3,6,4,7),(4,16,5,15),(5,11,6,10),(7,12,8,13),(9,15,10,14),(11,1,12,16)))
