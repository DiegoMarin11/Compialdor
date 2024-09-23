


def process_word(word, automaton, keywords):
    state = 'd0'
    for char in word:
        transitions = automaton.get(state, {})
        next_state = transitions.get(char, 'q_generic')
        #next_state = automaton.get(state, {}).get(char, 'q_generic')  # q_generic as default state if no valid transitions
        #print(f"Transition: {state} --({char})--> {next_state}")
        state = next_state
   
    if state == 'd6':  # Acceptance state
        if word in keywords:
            return ("KEYWORD")
        if word.isdigit():
            return ("NUMBER")
        if word == '=':
            return ("OPERATOR")
    elif state == 'd34':
        return ("INVALID IDENTIFIER")
    else:
        return ("IDENTIFIER")

def tokenize(processed_string, automaton, keywords):
    
    tokens = []

    for word in processed_string:
        token_type = process_word(word, automaton, keywords)
        tokens.append((word, token_type))

    return tokens


