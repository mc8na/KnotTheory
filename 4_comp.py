import itertools
subsets = {"P","B","G","R","PB","PG","PR","BG","BR","GR","PBG","PBR","PGR","BGR","PBGR","W"}

ineff = [set()]
ineff.append({"P","PB","PG","PR","PBG","PBR","PGR","PBGR"})
ineff.append({"B","G","R","BG","BR","GR","BGR","W"})
ineff.append({"B","PB","BG","BR","PBG","PBR","BGR","PBGR"})
ineff.append({"P","G","R","PG","PR","GR","PGR","W"})
ineff.append({"G","PG","BG","GR","PBG","PGR","BGR","PBGR"})
ineff.append({"P","B","R","PB","PR","BR","PBR","W"})
ineff.append({"R","PR","BR","GR","PBR","PGR","BGR","PBGR"})
ineff.append({"P","B","G","PB","PG","BG","PBG","W"})
ineff.append({"P","B","PG","BG","PR","BR","PGR","BGR"})
ineff.append({"G","R","PB","GR","PBG","PBR","PBGR","W"})
ineff.append({"P","G","PB","BG","PR","GR","PBR","BGR"})
ineff.append({"B","R","PG","BR","PBG","PGR","PBGR","W"})
ineff.append({"P","R","PB","PG","BR","GR","PBG","BGR"})
ineff.append({"B","G","PR","BG","PBR","PGR","PBGR","W"})
ineff.append({"B","G","PB","PG","BR","GR","PBR","PGR"})
ineff.append({"P","R","PR","BG","PBG","BGR","PBGR","W"})
ineff.append({"B","R","PB","PR","BG","GR","PBG","PGR"})
ineff.append({"P","G","PG","BR","PBR","BGR","PBGR","W"})
ineff.append({"G","R","PG","PR","BG","BR","PBG","PBR"})
ineff.append({"P","B","PB","GR","PGR","BGR","PBGR","W"})
ineff.append({"P","B","G","PR","BR","GR","PBG","PBGR"})
ineff.append({"R","PB","PG","BG","PBR","PGR","BGR","W"})
ineff.append({"P","B","R","PG","BG","GR","PBR","PBGR"})
ineff.append({"G","PB","PR","BR","PBG","PGR","BGR","W"})
ineff.append({"P","G","R","PB","BG","BR","PGR","PBGR"})
ineff.append({"B","PG","PR","GR","PBG","PBR","BGR","W"})
ineff.append({"B","G","R","PB","PG","PR","BGR","PBGR"})
ineff.append({"P","BG","BR","GR","PBG","PBR","PGR","W"})
ineff.append({"P","B","G","R","PBG","PBR","PGR","BGR"})
ineff.append({"PB","PG","PR","BG","BR","GR","PBGR","W"})

def nCk(n, k): # returns value of n choose k
	if k == 0 or k == n:
		return 1
	r,c = min(k,n-k),1
	for i in range(r):
		c *= ((n-i)/(i+1))
	return int(c)

def tuples(num): # prints how many possible tuples appear in a given number of ineffective sets
	dict = {}
	for combo in itertools.combinations(subsets,num):
		count,tuple = 0,set()
		for c in combo:
			tuple.add(c)
		for i in range(len(ineff)):
			if tuple <= ineff[i]:
				count += 1
		if count in dict:
			dict[count] += 1
		else:
			dict[count] = 1
	for key in sorted(dict.keys()):
		print(str(dict[key]) + '/' + str(nCk(16,num)) + ' ' + str(num) + '-tuples appear ' + str(key) + ' times')
	print('')

def print_tuples():
	for i in range(1,9):
		tuples(i)
		
def quads(): # determines whether all quads that appear in three ineffective sets have an
			 # even number of P's, B's, G's, and R's and whether all quads that appear in
			 # one ineffective set have an odd number of P's, B's, G's, or R's
	for combo in itertools.combinations(subsets,4):
		count,tuple = 0,set()
		for c in combo:
			tuple.add(c)
		for i in range(len(ineff)):
			if tuple < ineff[i]:
				count += 1
		s,p,b,g,r = "",0,0,0,0
		for c in tuple:
			for l in c:
				if l == 'P':
					p += 1
				elif l == 'B':
					b += 1
				elif l == 'G':
					g += 1
				elif l == 'R':
					r += 1
		if (p%2)+(b%2)+(g%2)+(r%2) == 0:
			if count == 1:
				print('boo')
		elif count == 3:
			print('boo')

def same_set(): # for any set of size 5-8, determines max number that appear in an ineffective set
	for i in range(5,9):
		count = []
		for combo1 in itertools.combinations(subsets,i):
			max = 4
			for j in range(5,i+1):
				for combo2 in itertools.combinations(combo1,j):
					tuple = set()
					for c in combo2:
						tuple.add(c)
					for k in range(len(ineff)):
						if tuple <= ineff[k]:
							max = j
			count += [max]
		print(str(min(count)) + ' out of ' + str(i) + ' appear in a set')

def combo(): # for any set of 7 or 8, determines whether any 5 or 6, resp., appear in an ineffective set
	for i in range(7,9):
		count = []
		bool = True
		for combo1 in itertools.combinations(subsets,i):
			m = max(i-2,4)
			for combo2 in itertools.combinations(combo1,m):
				b = False
				tuple = set()
				for c in combo2:
					tuple.add(c)
				for k in range(len(ineff)):
					if tuple <= ineff[k]:
						b = True
				if not b:
					bool = False
		print(str(i) + ' = ' + str(bool) + ' for a set of ' + str(i))
		