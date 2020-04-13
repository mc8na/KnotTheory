# Filename: DavidClayton-PythonProgram.py
# Author: David Clayton
#
# Defines Knot class and methods to determine whether a diagram
# is equivalent to the unknot using Reidemeister moves
#
# Used as a Python coding example

import functools, itertools
class Knot:
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
	def ecodes(self):
		codes = []
		tcode = self.code.copy()
		for i in range(len(self.code)):
			reduced = Knot(tcode).code
			if reduced not in codes:
				codes += [Knot(tcode).code]
			tcode.reverse()
			reduced = Knot(tcode).code
			if reduced not in codes:
				codes += [Knot(tcode).code]
			tcode.reverse()
			tcode = tcode[1:]+tcode[:1]
		return codes
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
				moves += [Knot(newcode)]
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
				moves += [Knot(newcode)]
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
				moves += [Knot(newcode)]
		return moves
	def simplify(self,verbose=False):
		simp = self.copy()
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
		sign = 1
		for i in range(len(self.code)):
			if self.code[i-1]*self.code[i] > 0:
				return False
		return True
	def is_unknot(self,loose=False):
		simp = self.simplify()
		return (not simp.code) or loose and (not simp.is_alternating())
	def copy(self):
		return Knot(self.code.copy())
	def __str__(self):
		return str(self.code)

def pos_val(pattern,fixed,kmove,loose=False):
	possible_moves = []
	for i in range(len(fixed)):
		if not fixed[i]:
			if pattern[i] in pattern[:i]:
				pos = pattern[:i].index(pattern[i])
				possible_moves += [fixed[:pos]+[-1]+fixed[pos+1:i]+[1]+fixed[i+1:]]
			else:
				pos = pattern[i+1:].index(pattern[i])+i+1
				possible_moves += [fixed[:i]+[1]+fixed[i+1:pos]+[-1]+fixed[pos+1:]]
	if not possible_moves:
		code = list(map(lambda x: pattern[x]*fixed[x], range(len(pattern))))
		return Knot(code).is_unknot(loose)^kmove
	for newfix in possible_moves:
		if not pos_val(pattern, newfix, not kmove, loose):
			return True
	return False

def game_tree(pattern,fixed,verbose=True):
	possible_moves = []
	for i in range(len(fixed)):
		if not fixed[i]:
			if pattern[i] in pattern[:i]:
				pos = pattern[:i].index(pattern[i])
				possible_moves += [fixed[:pos]+[-1]+fixed[pos+1:i]+[1]+fixed[i+1:]]
			else:
				pos = pattern[i+1:].index(pattern[i])+i+1
				possible_moves += [fixed[:i]+[1]+fixed[i+1:pos]+[-1]+fixed[pos+1:]]
	if not possible_moves:
		code = list(map(lambda x: pattern[x]*fixed[x], range(len(pattern))))
		if Knot(code).is_unknot():
			return 'U'
		return 'K'
	current_tree = []
	for newfix in possible_moves:
		new_result = game_tree(pattern, newfix, verbose=False)
		if type(new_result) == list:
			new_result.sort()
		if new_result not in current_tree:
			current_tree += [new_result]
	if verbose:
		print(current_tree)
		print()
		while type(current_tree) == list:
			current_tree = simplify_tree(current_tree)
			print(current_tree)
			print()
	else:
		return current_tree

def simplify_tree(game_tree):
	if type(game_tree[0]) == list:
		return list(map(simplify_tree,game_tree))
	elif '0' not in game_tree and 'U' not in game_tree and 'K' not in game_tree:
		return '0'
	elif 'U' in game_tree and '0' not in game_tree and 'K' not in game_tree:
		return 'U'
	elif 'K' in game_tree and '0' not in game_tree and 'U' not in game_tree:
		return 'K'
	return '*'

def winner(pattern,loose=False):
	kwin = pos_val(pattern,[0]*len(pattern),True)
	uwin = pos_val(pattern,[0]*len(pattern),False)
	if kwin and uwin:
		print('The first player to move wins.')
	elif kwin:
		print('K always wins.')
	elif uwin:
		print('U always wins.')
	else:
		print('The second player to move wins.')