# from graphviz import Digraph
import FA, DFA
import copy
import math

class NFA(FA.FA):


    def create_equivalent_DFA(self):

        adj = [FA.Node(_) for _ in range(int(math.pow(len(self.states), 2)))]
        transition_matrix = [['ϕ' for __ in range(int(math.pow(len(self.states), 2)))] for _ in range(int(math.pow(len(self.states), 2)))]
        dfa_states = [[self.init_state]]

        for i, states in enumerate(dfa_states):
            for terminal in self.terminals + ['\\']:
                neigh = []
                for s in states:
                    state = int(s.replace('q', ''))
                    for edge in self.adj[state].neighbors:
                        n, w = edge.dest, edge.weight
                        if terminal == w:
                            if adj[n].symbol not in neigh:
                                neigh.append(adj[n].symbol)
                            for e in self.adj[n].neighbors:
                                nn, ww = e.dest, e.weight
                                if '\\' == ww:
                                    if adj[nn].symbol not in neigh:
                                        neigh.append(adj[nn].symbol)
                neigh.sort()
                if neigh:
                    if dfa_states.count(neigh) == 0:
                        dfa_states.append(neigh)
                    dest = dfa_states.index(neigh)
                    
                    adj[i].neighbors.append(FA.Edge(neigh, terminal))

                    transition_matrix[i][dest] = terminal
        fainal_states = []

        for i in range(len(dfa_states)):
            for state in dfa_states[i]:
                state = int(state.replace('q', ''))
                if adj[state].symbol in self.final_states and dfa_states[i] not in fainal_states:
                    fainal_states.append(dfa_states[i])

        adj = [adj[i] for i in range(len(dfa_states))]
        transition_matrix = [[transition_matrix[i][j] for j in range(len(dfa_states))] for i in range(len(dfa_states))]
        # dfa_states = [q.symbol for q in adj]
        return DFA.DFA(dfa_states, self.terminals, dfa_states[0], fainal_states, adj, transition_matrix)

    def get_input_symbol(self):
        input_symbols = {st: {to: '' for to in self.states} for st in self.states}
        for node in range(len(self.adj)):
            for edge in self.adj[node].neighbors:
                n, w = edge.dest, edge.weight
                if input_symbols[self.adj[node].symbol][self.adj[n].symbol] == '':
                    input_symbols[self.adj[node].symbol][self.adj[n].symbol] = w
                else:
                    input_symbols[self.adj[node].symbol][self.adj[n].symbol] += '+' + w
        return input_symbols

    def get_pred(self, state, input_symbols):
        return [f'q{i}' for i in range(-1, len(self.adj)) if list(input_symbols.keys()).count(f'q{i}') and input_symbols[f'q{i}'][state] != '' and f'q{i}' != state]
 
    def get_succ(self, state, input_symbols):
        return [f'q{i}' for i in range(len(self.adj) + 1) if list(input_symbols[state].keys()).count(f'q{i}') and input_symbols[state][f'q{i}'] != '' f'q{i}' != state]

    def check_self_loop(self, state, input_symbols):
        if input_symbols[state][state] == '':
            return False
        return True

    def build_one_final_nfa(self, input_symbols):
        self.states.append(f'q{len(self.adj)}')
        for final_state in self.final_states:
            input_symbols[final_state][f'q{len(self.adj)}'] = '\\'
        self.final_states = [f'q{len(self.adj)}']

        self.states = ['q-1'] + self.states
        input_symbols['q-1'] = {}
        for to in self.states:
            if to != self.init_state:
                input_symbols['q-1'][to] = ''
            else:
                input_symbols['q-1'][to] = '\\'
        
        self.init_state = 'q-1'

        


    def find_regexp(self):

        input_symbols = self.get_input_symbol()
        self.build_one_final_nfa(input_symbols)
        
        for state in self.states:
            if state == self.init_state or state in self.final_states:
                continue


            successors = self.get_succ(state, input_symbols)
            predecessors = self.get_pred(state, input_symbols)
            for predecessor in predecessors:
                if predecessor in input_symbols.keys():
                    for successor in successors:
                        if successor in input_symbols[predecessor].keys():

                            pred_suc = ''
                            self_loop = ''
                            from_pred = ''
                            to_suc = ''

                            if input_symbols[predecessor][successor] != '':
                                if not input_symbols[predecessor][successor].count('+'):
                                    to_suc = input_symbols[predecessor][successor]
                                else:
                                    pred_suc = '(' + input_symbols[predecessor][successor] + ')'
                            
                            if self.check_self_loop(state, input_symbols):
                                if not input_symbols[state][state].count('+'):
                                    self_loop = input_symbols[state][state] + '*'
                                else:
                                    self_loop = '(' + input_symbols[state][state] + ')' + '*'
                                    
                            if input_symbols[predecessor][state] != '':
                                if not input_symbols[predecessor][state].count('+'):
                                    from_pred = input_symbols[predecessor][state]
                                else:
                                    from_pred = '(' + input_symbols[predecessor][state] + ')'
                            
                            if input_symbols[state][successor] != '':
                                if not input_symbols[state][successor].count('+'):
                                    to_suc = input_symbols[state][successor]
                                else:
                                    to_suc = '(' + input_symbols[state][successor] + ')'

                            new_exp = from_pred + self_loop + to_suc

                            if pred_suc != '':
                                new_exp = '(' + new_exp + '+' + pred_suc + ')'

                            input_symbols[predecessor][successor] = new_exp
            
            input_symbols = {st: {to: v for to, v in inp.items() if to != state} for st, inp in input_symbols.items() if st != state}
        r = input_symbols[self.init_state][self.final_states[0]]
        return r
