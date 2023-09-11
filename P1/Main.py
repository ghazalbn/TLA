import FA, NFA

def show_menu(nfa):
    print('\n\n********Menu********\n')
    print('Available Functions:\n\n')
    print('**DFA**\nisAcceptByDFA\nmakeSimpleDFA\nshowSchematicDFA\n')
    print('**NFA**\nisAcceptByNFA\ncreateEquivalentDFA\nfindRegExp\nshowSchematicNFA\n\n')
    while True:

        query = input('Enter the function you want to call, or Exit: ').lower()
        if query == 'exit' :
            exit()
        elif query == 'isacceptbydfa' or query == 'isacceptbynfa' :
            string = input('Enter a string: ')
            print(nfa.is_accept_by_FA(0, string))
            print()

        elif query == 'showschematicdfa' or query == 'showschematicnfa' :
            nfa.show_schematic_FA()
            print()

        elif query == 'makesimpledfa' :
            dfa = nfa.create_equivalent_DFA()
            dfa.make_simple_DFA()
            print()

        elif query == 'createequivalentdfa' :
            dfa = nfa.create_equivalent_DFA()
            print_dfa(dfa)
            print()

        elif query == 'findregexp' :
            print(nfa.find_regexp())
            print()
        
        
def print_dfa(dfa):
    print('states:\n' + f'[{ "], [".join(map(", ".join, dfa.states))}]')
    print('\nInitial State: ' + str(dfa.init_state[0]))
    print('\nFinal States:\n' + f'[{ "], [".join(map(", ".join, dfa.final_states))}]')
    print('\nTransitions:\n')
    for i in range(len(dfa.states)):
        for e in dfa.adj[i].neighbors:
            n, w = e.dest, e.weight
            print(f'[{ ", ".join(dfa.states[i])}]', f'[{ ", ".join(n)}]', w)


if __name__ == '__main__':
    states = input('Enter the states in your FA : ')
    states = states.replace('{', '').replace('}','').split(',')
    alphabets = input('Enter the terminals : ')
    alphabets = alphabets.replace('{', '').replace('}','').split(',')
    init_state = states[0]
    adj = [FA.Node(_) for _ in range(len(states))]
    transition_matrix = [['ϕ' for __ in range(len(states))] for _ in range(len(states))]
    final_states = input('Enter the final states : ')
    final_states = final_states.replace('{', '').replace('}','').split(',')
    transition_count = int(input('Enter the number of transitions: '))
    print('Enter transitions:')

    for i in range(transition_count):
        s = list(map(str, input().replace('q', '').split(',')))
        q, n, w = int(s[0]), int(s[1]), s[2] if len(s)>0 and s[2] else '\\'
        adj[q].neighbors.append(FA.Edge(n, w))
        transition_matrix[q][n] = w
    nfa = NFA.NFA(states, alphabets, init_state, final_states, adj, transition_matrix)

    show_menu(nfa)

    # print(nfa.DFA_to_regex())
