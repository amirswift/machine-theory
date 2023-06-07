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
