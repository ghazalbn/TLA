# from graphviz import Digraph
class Edge:
    def __init__(self, d, w):
        self.dest = d
        self.weight = w
class Node:
    def __init__(self, i):
        self.symbol = f'q{i}'
        self.neighbors = []

class FA:
    def __init__(self, states, terminals, init_state, final_states, adj, transition_matrix):
        self.states = states
        self.terminals = terminals
        self.init_state = init_state
        self.final_states = final_states
        self.transition_matrix = transition_matrix
        self.regex = ''
        self.adj = adj

    def is_accept_by_FA(self, node, string):

        if not len(string) and self.adj[node].symbol in self.final_states:
            return True
        if not len(string):
            return False
        for edge in self.adj[node].neighbors:
            n, w = edge.dest, edge.weight
            if (w == '\\' and self.is_accept_by_FA(n, string)) or (w == string[0] and self.is_accept_by_FA(n, string[1: ])):
                    return True
        if not len(string):
            return False
        return False

    def show_schematic_FA(self, label, name):
        gr = Digraph(format='svg')
        gr.attr('node', shape='point')
        gr.node('qi')
        for i in self.states:
            if i in self.final_states:
                gr.attr('node', shape='doublecircle', color='green', style='')
            elif i in self.init_state:
                gr.attr('node', shape='circle', color='black', style='')
            else:
                gr.attr('node', shape='circle', color='white', style='')
            gr.node(str(' '.join(i)))
            if i in self.init_state:
                gr.edge('qi', str(' '.join(i)), 'start')
        for i, node in enumerate(self.states):
            for edge in adj[i].neighbors:
                n, w = edge.dest, edge.weight
                gr.edge(str(' '.join(node)), str(' '.self.adj[n]), w)
        gr.body.append(r'label = "\n\n{0}"'.format(label))
        gr.render('{0}'.format(name), view=True)


    def set_transition_dict(self):
        dict_states = {r: {c: 'ϕ' for c in self.states} for r in self.states}
        for i in self.states:
            for j in self.states:
                indices = [ii for ii, v in enumerate(self.transition_funct[i]) if v == j]  # get indices of states
                if len(indices) != 0:
                    dict_states[i][j] = '+'.join([str(self.terminals[v]) for v in indices])
        self.ds = dict_states
        self.transition_dict = copy.deepcopy(dict_states)

    def get_intermediate_states(self):
        return [state for state in self.states if state not in ([self.init_state] + self.final_states)]

    def get_predecessors(self, state):
        return [key for key, value in self.ds.items() if state in value.keys() and value[state] != 'ϕ' and key != state]

    def get_successors(self, state):
        return [key for key, value in self.ds[state].items() if value != 'ϕ' and key != state]

    def get_if_loop(self, state):
        if self.ds[state][state] != 'ϕ':
            return self.ds[state][state]
        else:
            return ''
