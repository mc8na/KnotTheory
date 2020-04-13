# Filename: threecomp.py
# Author: Miles Clikeman
#
# Attempts to identify patterns in the shading subsets of three-component reduced link diagrams.

import itertools

subsets = {"P","B","G","PB","PG","BG","PBG","W"}

ineff = [{"P","PB","PG","PBG"}] + [{"B","G","BG","W"}]
ineff += [{"B","PB","BG","PBG"}] + [{"P","G","PG","W"}]
ineff += [{"G","PG","BG","PBG"}] + [{"P","B","PB","W"}]
ineff += [{"P","B","PG","BG"}] + [{"G","PB","PBG","W"}]
ineff += [{"P","G","PB","BG"}] + [{"B","PG","PBG","W"}]
ineff += [{"B","G","PB","PG"}] + [{"P","BG","PBG","W"}]
ineff += [{"P","B","G","PBG"}] + [{"PB","PG","BG","W"}]

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
		print(str(dict[key]) + '/' + str(nCk(8,num)) + ' ' + str(num) + '-tuples appear ' + str(key) + ' times')
	print('')

def print_tuples(): # prints the tuples found in tuples()
	for i in range(1,4):
		tuples(i)

def two_two():
	for i in range(0,7):
		for j in range(0,14):
			if j != 2*i and j != 2*i+1:
				if len(ineff[j]&ineff[2*i]) != 2 or len(ineff[j]&ineff[2*i+1]) != 2:
					print('False')
