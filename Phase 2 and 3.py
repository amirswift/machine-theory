from collections import deque

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts_input(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.accept_states

    def add_transition(self, state, symbol, next_state):
        if state in self.transitions:
            self.transitions[state][symbol] = next_state
        else:
            self.transitions[state] = {symbol: next_state}

    def count_members(self, max_length):
        count = 0
        members = []

        def generate_string_rec(length, current_string):
            nonlocal count
            if length == 0:
                if self.accepts_input(current_string):
                    count += 1
                    members.append(current_string)
            else:
                for char in self.alphabet:
                    generate_string_rec(length - 1, current_string + char)

        for length in range(1, max_length + 1):
            generate_string_rec(length, '')

        return count, members

    def generate_strings(self, length):
        if length == 0:
            yield ''
        else:
            for string in self.generate_strings(length - 1):
                for char in self.alphabet:
                    yield string + char

    def is_language_empty(self):
        for length in range(1, len(self.states) + 1):
            for string in self.generate_strings(length):
                if self.accepts_input(string):
                    return False
        return True

    def is_language_infinite(self):
        visited_states = set()
        stack = [self.start_state]

        while stack:
            current_state = stack.pop()
            visited_states.add(current_state)

            for symbol in self.alphabet:
                next_state = self.transitions[current_state][symbol]
                if next_state not in visited_states:
                    stack.append(next_state)

                if next_state in visited_states and self.accepts_input(symbol):
                    return True

        return False

    def shortestWord(self, lst):
        if not lst:
            return 0
        return len(min(lst, key=len))

    def longestWord(self, lst):
        if not lst:
            return 0
        return len(max(lst, key=len))

    def language_accepts_string(self, x):
        return self.accepts_input(x)

    def generate_language_examples(self):
        non_accepted_strings = []
        accepted_strings = []

        for length in range(1, len(self.states) + 2):
            for string in self.generate_strings(length):
                if self.accepts_input(string):
                    accepted_strings.append(string)
                else:
                    non_accepted_strings.append(string)

                if len(accepted_strings) >= 2 and len(non_accepted_strings) >= 2:
                                        return accepted_strings[:2], non_accepted_strings[:2]

    def generate_strings_of_length(self, length):
        strings = []

        def generate_strings_rec(current_state, current_string):
            if len(current_string) == length:
                if current_state in self.accept_states:
                    strings.append(current_string)
            else:
                for symbol in self.alphabet:
                    next_state = self.transitions[current_state][symbol]
                    generate_strings_rec(next_state, current_string + symbol)

        generate_strings_rec(self.start_state, '')

        return strings

    def count_strings_of_length(self, length):
        count = 0

        def count_strings_rec(current_state, current_length):
            nonlocal count
            if current_length == length:
                if current_state in self.accept_states:
                    count += 1
            else:
                for symbol in self.alphabet:
                    next_state = self.transitions[current_state][symbol]
                    count_strings_rec(next_state, current_length + 1)

        count_strings_rec(self.start_state, 0)

        return count
        
    def complement(self):
        complement_states = self.states - self.accept_states
        return DFA(self.states, self.alphabet, self.transitions, self.start_state, complement_states)
    def intersection(self, other_dfa):
        intersection_states = set()
        intersection_accept_states = set()
        intersection_transitions = {}

        for state1 in self.states:
            for state2 in other_dfa.states:
                new_state = f'({state1}, {state2})'
                intersection_states.add(new_state)

                if state1 in self.accept_states and state2 in other_dfa.accept_states:
                    intersection_accept_states.add(new_state)

                for symbol in self.alphabet:
                    next_state1 = self.transitions[state1][symbol]
                    next_state2 = other_dfa.transitions[state2][symbol]
                    new_next_state = f'({next_state1}, {next_state2})'
                    intersection_transitions.setdefault(new_state, {})[symbol] = new_next_state

        intersection_start_state = f'({self.start_state}, {other_dfa.start_state})'

        return DFA(intersection_states, self.alphabet, intersection_transitions, intersection_start_state, intersection_accept_states)
    def union(self, other_dfa):
        union_states = set()
        union_accept_states = set()
        union_transitions = {}

        for state1 in self.states:
            for state2 in other_dfa.states:
                new_state = f'({state1}, {state2})'
                union_states.add(new_state)

                if state1 in self.accept_states or state2 in other_dfa.accept_states:
                    union_accept_states.add(new_state)

                for symbol in self.alphabet:
                    next_state1 = self.transitions[state1].get(symbol, 'E')
                    next_state2 = other_dfa.transitions[state2].get(symbol, 'E')
                    new_next_state = f'({next_state1}, {next_state2})'
                    union_transitions.setdefault(new_state, {})[symbol] = new_next_state

        union_start_state = f'({self.start_state}, {other_dfa.start_state})'

        return DFA(union_states, self.alphabet, union_transitions, union_start_state, union_accept_states)
    # Union of the two DFAs


    
    def difference(self, other_dfa):
        difference_states = set()
        difference_accept_states = set()
        difference_transitions = {}

        for state1 in self.states:
            for state2 in other_dfa.states:
                new_state = f'({state1}, {state2})'
                difference_states.add(new_state)

                if state1 in self.accept_states and state2 not in other_dfa.accept_states:
                    difference_accept_states.add(new_state)

                for symbol in self.alphabet:
                    next_state1 = self.transitions[state1].get(symbol, 'E')
                    next_state2 = other_dfa.transitions[state2].get(symbol, 'E')
                    new_next_state = f'({next_state1}, {next_state2})'
                    difference_transitions.setdefault(new_state, {})[symbol] = new_next_state

        difference_start_state = f'({self.start_state}, {other_dfa.start_state})'

        return DFA(difference_states, self.alphabet, difference_transitions, difference_start_state, difference_accept_states)
    
    def is_disjoint(self, other_dfa):
        for length in range(1, len(self.states) + len(other_dfa.states) + 1):
            for string in self.generate_strings(length):
                if self.accepts_input(string) and other_dfa.accepts_input(string):
                    return False
        return True
    # Check if the two DFAs are disjoint
    
    # Difference of the two DFAs
    def is_equivalent(self, other_dfa):
    # Check if the sets of accepting states are different
        if self.accept_states != other_dfa.accept_states:
            return False

        # Check if all strings up to the length of the combined state space
        # are accepted by both DFAs
        for length in range(1, len(self.states) + len(other_dfa.states) + 1):
            for string in self.generate_strings(length):
                if self.accepts_input(string) != other_dfa.accepts_input(string):
                    return False

        return True
     
    def minimize_level1(self):
        not_visited = [(i , j) for i in self.states for j in self.states]

        for tup in not_visited:
            i, j = tup
            is_i_accepted = True if i in self.accept_states else False
            is_j_accepted = True if j in self.accept_states else False
           
            if (is_i_accepted == is_j_accepted):
                not_visited.remove((i, j))
                
           
       
        return not_visited

    def minimize(self):
        not_visited = self.minimize_level1()
        
        _break = False

        while(not _break):
            _break = True

            for pair in not_visited:
                state_i, state_j = pair

                for char in self.alphabet:
                    state_after_i = self.transitions[state_i][char]
                    state_after_j = self.transitions[state_j][char]
                    
                    is_state_after_i_accepted = True if state_after_i in self.accept_states else False
                    is_state_after_j_accepted = True if state_after_j in self.accept_states else False  
                    
                    if(is_state_after_i_accepted == is_state_after_j_accepted):
                        if (state_i, state_j) in not_visited:
                            not_visited.remove((state_i, state_j))
                            _break = False
                        if (state_j, state_i) in not_visited:
                            not_visited.remove((state_j, state_i))
                            _break = False
        
        return not_visited
    # Check if the transitions are disjoint 
     

states = {'A', 'B', 'C', 'E'}
alphabet = {'a', 'b'}
transitions = {
    'A': {'a': 'C', 'b': 'B'},
    'B': {'a': 'E', 'b': 'E'},
    'C': {'a': 'B', 'b': 'E'},
    ##'D': {'a': 'E', 'b': 'E'},
    'E': {'a': 'E', 'b': 'E'}
    
}
start_state = 'A'
accept_states = {'B','C'}

dfa = DFA(states, alphabet, transitions, start_state, accept_states)

count, members = dfa.count_members(5)
print("Members are:", count)
print("Members are:")
for member in members:
    print(member)

language_empty = dfa.is_language_empty()
print("Is the language empty?", language_empty)

language_infinite = dfa.is_language_infinite()
print("Is the language infinite?", language_infinite)

print('Length of the shortest string is:', dfa.shortestWord(members))
print('Length of the longest string is:', dfa.longestWord(members))

string_to_check = 'aa'
accepts_string = dfa.language_accepts_string(string_to_check)
print(f"Does the language accept '{string_to_check}'?", accepts_string)

accepted_examples, non_accepted_examples = dfa.generate_language_examples()
print("Accepted examples:")
for example in accepted_examples:
    print(example)

print("Non-accepted examples:")
for example in non_accepted_examples:
    print(example)

k = 1
strings_of_length_k = dfa.generate_strings_of_length(k)
print(f"Strings of length {k} in the language:")
for string in strings_of_length_k:
    print(string)

m = 2
count_strings_of_length_m = dfa.count_strings_of_length(m)
print(f"Number of strings with length {m} in the language:", count_strings_of_length_m)
complement_dfa = dfa.complement()

print("Original DFA:")
print("Accept states:", dfa.accept_states)

print("Complement DFA:")
print("Accept states:", complement_dfa.accept_states)

states1 = {'A', 'B', 'C', 'E'}
alphabet1 = {'a', 'b'}
transitions1 = {
    'A': {'a': 'C', 'b': 'B'},
    'B': {'a': 'E', 'b': 'E'},
    'C': {'a': 'B', 'b': 'E'},
    'E': {'a': 'E', 'b': 'E'}
}
start_state1 = 'A'
accept_states1 = {'B', 'C'}
dfa1 = DFA(states1, alphabet1, transitions1, start_state1, accept_states1)

# Second DFA
states2 = {'X', 'Y', 'Z'}
alphabet2 = {'a', 'b'}
transitions2 = {
    'X': {'a': 'Y', 'b': 'X'},
    'Y': {'a': 'Z', 'b': 'Y'},
    'Z': {'a': 'Y', 'b': 'X'}
}
start_state2 = 'X'
accept_states2 = {'X', 'Y'}
dfa2 = DFA(states2, alphabet2, transitions2, start_state2, accept_states2)

# Intersection of the two DFAs
intersection_dfa = dfa1.intersection(dfa2)

# Print the intersection DFA
print("Intersection DFA:")
print("States:", intersection_dfa.states)
print("Alphabet:", intersection_dfa.alphabet)
print("Transitions:", intersection_dfa.transitions)
print("Start State:", intersection_dfa.start_state)
print("Accept States:", intersection_dfa.accept_states)

union_dfa = dfa1.union(dfa2)

print("Union DFA:")
print("States:", union_dfa.states)
print("Alphabet:", union_dfa.alphabet)
print("Transitions:", union_dfa.transitions)
print("Start State:", union_dfa.start_state)
print("Accept States:", union_dfa.accept_states)

difference_dfa = dfa1.difference(dfa2)

# Print the difference DFA
print("Difference DFA:")
print("States:", difference_dfa.states)
print("Alphabet:", difference_dfa.alphabet)
print("Transitions:", difference_dfa.transitions)
print("Start State:", difference_dfa.start_state)
print("Accept States:", difference_dfa.accept_states)
disjoint = dfa1.is_disjoint(dfa2)

    # Print the result
if disjoint:
    print("The two DFAs are disjoint.")
else:
    print("The two DFAs are not disjoint.")
equivalent = dfa1.is_equivalent(dfa2)

# Print the result
if equivalent:
    print("The two DFAs are equivalent.")
else:
    print("The two DFAs are not equivalent.")


print(dfa.minimize())