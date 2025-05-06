import collections
from collections import defaultdict
import json
def infix_to_postfix(infix_expr):
    
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3} 
    rez = []
    operators = []

    def add_concat_operator(expr):
        res = []
        for i, caracter in enumerate(expr):
            res.append(caracter)
            if i < len(expr) - 1:
                current = caracter
                next = expr[i+1]

                if (current.isalnum() or current in ['*', '?', '+', ')']) and \
                   (next.isalnum() or next == '('):
                    res.append('.')
        return "".join(res)

    infix_expr = add_concat_operator(infix_expr)

    for caracter in infix_expr:
        if caracter.isalnum(): 
            rez.append(caracter)
        elif caracter == '(':
            operators.append(caracter)
        elif caracter == ')':
            while operators and operators[-1] != '(':
                rez.append(operators.pop())
            if operators and operators[-1] == '(':
                operators.pop()  #
            
        else:  
            while (operators and operators[-1] != '(' and precedence.get(operators[-1], 0) >= precedence.get(caracter, 0)):
                rez.append(operators.pop())
            operators.append(caracter)

    while operators:
        rez.append(operators.pop())

    return "".join(rez)

stare_curenta_id = 0

def stare_noua():
    global stare_curenta_id
    stare_curenta_id += 1
    return stare_curenta_id - 1

class NFAFragment:
    def __init__(self, start_stare, accept_stare, tranzitii):
        self.start_stare = start_stare
        self.accept_stare = accept_stare
        self.tranzitii = tranzitii

def caracter(char):
    s0 = stare_noua()
    s1 = stare_noua()
    return NFAFragment(s0, s1, [(s0, char, s1)])

def concatenare(nfa1, nfa2):
    tranzitii = nfa1.tranzitii + nfa2.tranzitii
    tranzitii.append((nfa1.accept_stare, 'λ', nfa2.start_stare))
    return NFAFragment(nfa1.start_stare, nfa2.accept_stare, tranzitii)

def alternare(nfa1, nfa2):
    s_nou = stare_noua()
    accept_nou = stare_noua()
    
    tranzitii = nfa1.tranzitii + nfa2.tranzitii
    tranzitii.append((s_nou, 'λ', nfa1.start_stare))
    tranzitii.append((s_nou, 'λ', nfa2.start_stare))
    tranzitii.append((nfa1.accept_stare, 'λ', accept_nou))
    tranzitii.append((nfa2.accept_stare, 'λ', accept_nou))
    
    return NFAFragment(s_nou, accept_nou, tranzitii)

def star(nfa1):
    s_nou = stare_noua()
    accept_nou = stare_noua()
    
    tranzitii = nfa1.tranzitii
    tranzitii.append((s_nou, 'λ', nfa1.start_stare))    
    tranzitii.append((s_nou, 'λ', accept_nou))          
    tranzitii.append((nfa1.accept_stare, 'λ', nfa1.start_stare)) 
    tranzitii.append((nfa1.accept_stare, 'λ', accept_nou))       
    
    return NFAFragment(s_nou, accept_nou, tranzitii)

def plus(nfa1):
   
    s_nou = stare_noua() 
    accept_nou = stare_noua() 
    
    tranzitii = list(nfa1.tranzitii) 
    
    tranzitii.append((s_nou, 'λ', nfa1.start_stare))
    
    tranzitii.append((nfa1.accept_stare, 'λ', nfa1.start_stare))
    
    tranzitii.append((nfa1.accept_stare, 'λ', accept_nou))
    
    return NFAFragment(s_nou, accept_nou, tranzitii)
def optional(nfa1):
    s_nou = stare_noua()
    accept_nou = stare_noua()

    tranzitii = list(nfa1.tranzitii)

    tranzitii.append((s_nou, 'λ', nfa1.start_stare))
    tranzitii.append((s_nou, 'λ', accept_nou))
    tranzitii.append((nfa1.accept_stare, 'λ', accept_nou))

    return NFAFragment(s_nou, accept_nou, tranzitii)

def postfix_la_nfa(expresie_postfix):
    global _stare_curenta_id
    _stare_curenta_id = 0 
    
    stiva = []
    alfabet = set()

    for token in expresie_postfix:
        if token.isalnum() and len(token) == 1: 
            alfabet.add(token)
            stiva.append(caracter(token))
        elif token == '.': 
           
            nfa2 = stiva.pop()
            nfa1 = stiva.pop()
            stiva.append(concatenare(nfa1, nfa2))
        elif token == '|': 
            
            nfa2 = stiva.pop()
            nfa1 = stiva.pop()
            stiva.append(alternare(nfa1, nfa2))
        elif token == '*': 
           
            nfa1 = stiva.pop()
            stiva.append(star(nfa1))
        elif token == '+':
            nfa1 = stiva.pop()
            stiva.append(plus(nfa1))
        elif token=='?':
            nfa1 = stiva.pop()
            stiva.append(optional(nfa1))
       
            
        
    nfa_final_fragment = stiva[0]
    
    
    
    return {
        "states": set(range(_stare_curenta_id)),
        "alfabet": alfabet,
        "tranzitii": nfa_final_fragment.tranzitii,
        "start": nfa_final_fragment.start_stare,
        "accept": {nfa_final_fragment.accept_stare}
    }

def compute_lamd_closure(state, transitions):
    closure = {state}
    stack = [state]
    while stack:
        current_state = stack.pop()
        for start_state, symbol, end_state in transitions:
            if start_state == current_state and symbol == 'λ' and end_state not in closure:
                closure.add(end_state)
                stack.append(end_state)
    return frozenset(closure)

def get_transitions_for_state_symbol(state, symbol, transitions):
    next_states = set()
    for start_state, sym, end_state in transitions:
        if start_state == state and sym == symbol:
            next_states.add(end_state)
    return next_states

def convert_nfa_to_dfa(nfa_config):
    alfabet = nfa_config["alfabet"]
    transitions_list = nfa_config["tranzitii"] 
    start = nfa_config["start"]
    accept = nfa_config["accept"]
    states = nfa_config["states"] 

    dfa_start = compute_lamd_closure(start, transitions_list)
    dfa_states = []
    dfa_transitions = {}
    dfa_accept = set()
    unprocessed = [dfa_start]

    while unprocessed:
        current_dfa_state = unprocessed.pop(0)
        if current_dfa_state not in dfa_states:
            dfa_states.append(current_dfa_state)
            if any(state in accept for state in current_dfa_state):
                dfa_accept.add(current_dfa_state)

            for symbol in alfabet:
                next_nfa_states = set()
                for nfa_state in current_dfa_state:
                    next_nfa_states.update(get_transitions_for_state_symbol(nfa_state, symbol, transitions_list))

                next_dfa_state = frozenset()
                for state in next_nfa_states:
                    next_dfa_state = next_dfa_state.union(compute_lamd_closure(state, transitions_list))

                if next_dfa_state:
                    dfa_transitions.setdefault(current_dfa_state, {})[symbol] = next_dfa_state
                    if next_dfa_state not in dfa_states and next_dfa_state not in unprocessed:
                        unprocessed.append(next_dfa_state)

    dfa = {
        "states": dfa_states,
        "alfabet": alfabet,
        "transitions": dfa_transitions,
        "start": dfa_start,
        "accept": dfa_accept
    }
    return dfa

def check(dfa, word):

    current_state=dfa['start']

    for char in word:
        transitions = dfa["transitions"].get(current_state, {})
        if char not in transitions:
            return False
        current_state = transitions[char]

    return current_state in dfa["accept"]



file="LFA-Assignment2_Regex_DFA_v2.json"
with open(file, 'r') as f:
    data = json.load(f)


for case in data:
    name = case['name']
    regex = case['regex']
    print(name)
    regex=infix_to_postfix(regex)
    nfa=postfix_la_nfa(regex)
    dfa=convert_nfa_to_dfa(nfa)
    # if name=="R7":
    #     print(dfa)
    pairs=case['test_strings']
    for pair in pairs:
        word=pair['input']
        rez=pair['expected']
        if rez==check(dfa,word):
            print(word,' Corect')
        else:
            print(word,' Incorect')

    print()