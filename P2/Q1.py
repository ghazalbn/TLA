# python3

import sys
import threading

sys.setrecursionlimit(10**6)
threading.stack_size(2**26) 

class Grammer:

	def __init__(self):
		# self.start = 'S'
		self.terminals = {}
		self.rules = {}

	# read grammer
	def read(self):
		n = int(input())
		for _ in range(n):
			rule = input().split("->")
			lhs = rule[0].strip().replace('<', '').replace('>', '')

			if _ == 0: self.start = lhs
			
			rhs = rule[1].strip().split("|")
			# print(parts)
			if not lhs in self.rules:
				self.rules[lhs]=[]
			for var in rhs:
				var = var.strip().replace('<', '').replace('>', '')
				# print(part)
				if not var in self.rules[lhs]:
					self.rules[lhs].append(var)

	def set_start(self):
		for key, value in self.rules.items():
			for vars in value:
				if 'S' in vars:
					self.rules['S0'] = ['S']
					self.start = 'S0'
					return


	def update_rules(self, variable):
		for key in list(self.rules):
			# if key != variable:
			for i in range(len(self.rules[key])):
				if variable in self.rules[key][i]:
					if len(self.rules[key][i]) == 1:
						self.rules[key].append(self.rules[key][i].replace(variable, "#"))
					elif self.rules[key][i] == f'{variable}{variable}' and variable not in self.rules[key]:
						self.rules[key].append(self.rules[key][i].replace(variable, "#"))
						self.rules[key].append(variable)
					else:
						self.rules[key].append(self.rules[key][i].replace(variable, ""))


	# hazfe lambda
	def eliminate_lambda(self):
			new_vars = list(self.rules)
		# while(len(new_vars)):
			# flag = False
			for key in new_vars:
				# new_vars.remove(key)
				value = self.rules[key]
				if key != self.start:
					for i in range(len(value)):
						if '#' in value[i]:
							# flag = True
							self.rules[key].remove('#')
							self.update_rules(key)
							# new_vars.append(key)
							break

			# if not flag:
			# 	return

	def is_terminal(self, var: str):
		return not var.isalpha() or var.islower()

	def eliminate_unit(self):
			new_vars = list(self.rules)
		# while(len(new_vars)):
			# flag = False
			for _ in range(2):
				for key in new_vars:
					# new_vars.remove(key)
					value = self.rules[key]
					for i in range(len(value)):
						if len(value[i]) == 1 and not self.is_terminal(value[i]) and value[i] != '#':
							# flag = True
							var = value[i]
							if (key != var):
								# self.rules[key] += self.rules[value[i]]
								if(value[i] in self.rules):
								# 	self.rules[key].remove(value[i])
								# else:
									for v in self.rules[var]:
										if v not in self.rules[key]:
											self.rules[key].append(v)
							# if i < len(value) and value[i] in self.rules[key]:
							self.rules[key].remove(var)
							# self.update_rules(key)
							# if(key not in new_variable): new_vars.append(key)
				# if not flag:
				# 	return

	def delete(self, variable):
		self.rules.pop(variable)
		for key, value in self.rules.items():
			for vars in value:
				if variable in vars:
					self.rules[key].remove(vars)

	
	def reach_terminal(self, key):
		for vars in self.rules[key]:
			flag = True
			# if vars.islower():
			# 	return True
			for var in vars:
				if var == key or (not self.is_terminal(var) and not self.reach_terminal(var)):
					flag = False
					break
			if flag:
				return True
		return False
			
					


	def reachable(self, v, key):
		queue = [v]
		while len(queue):
			variable = queue.pop()
			for vars in self.rules[variable]:

				# if key in vars:
				# 	return True
				for var in vars:
					if var == key:
						return True
					# or khatarnake!!!
					if var.isupper() and (var != variable and (var != 'S' or variable != 'S0')):
						queue.append(var)
				
		return False
				


	def eliminate_useless(self):
		for key in list(self.rules):
			# not self.reach_terminal(key) or
			if  (key != self.start and not self.reachable(self.start, key)):
				self.delete(key)


	def eliminate(self):
		self.eliminate_lambda()
		self.eliminate_unit()
		# threading.Thread(target=self.eliminate_useless).start()
		# self.eliminate_useless()


	def new_variable(self):
		alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		for alpha in alphabet:
			if alpha not in self.rules:
				return alpha
		sys.exit(0)


	def convert_terminals(self):
		for key in list(self.rules):
			for j in range(len(self.rules[key])):
				value = self.rules[key][j]
				for i in range(len(value)):
					if self.is_terminal(value[i]) and len(value) != 1:
						if value[i] not in self.terminals:
							var = self.new_variable()
							self.terminals[value[i]] = var
							self.rules[var] = [value[i]]
							# self.rules[var].append(value[i])
						else:
							var = self.terminals[value[i]]
						self.rules[key][j] = self.rules[key][j].replace(value[i], var)


		
	def convert_twovariables(self):
		new_vars = list(self.rules)
		while len(new_vars):
			for key in new_vars:
				for j in range(len(self.rules[key])):
					length = len(self.rules[key][j])
					if length > 2:
						values = self.rules[key][j][1:]
						name = self.new_variable()
						new_vars.append(name)
						self.rules[name] = []
						self.rules[name].append(values)
						self.rules[key][j] = self.rules[key][j].replace(values, name)
				new_vars.remove(key)


	def cgf_to_cnf(self):
		self.read()
		self.set_start()
		self.eliminate()
		self.convert_terminals()
		self.convert_twovariables()


	def cyk(self, w):
		n = len(w)
		table = [[set([]) for j in range(n)] for i in range(n)]
	
		for j in range(n):
			for variable, rule in self.rules.items():
				for rhs in rule:
					if len(rhs) == 1 and rhs[0] == w[j]:
						table[j][j].add(variable)
			for i in range(j, -1, -1):   
				for k in range(i, j):     
					for variable, rule in self.rules.items():
						for rhs in rule:
							if len(rhs) == 2 and rhs[0] in table[i][k] and rhs[1] in table[k + 1][j]:
								table[i][j].add(variable)
		return "Rejected" if len(table[0][n-1]) == 0 else "Accepted"
					

grammer = Grammer()
grammer.cgf_to_cnf()
w = input()
print(grammer.cyk(w))

