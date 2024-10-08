

def process_word(word, automaton, keywords):


    state = 'd0'
    read_word = []



    for char in word:
        #print(char)
        transitions = automaton.get(state, {})
        next_state = transitions.get(char, 'q_generic')
        #next_state = automaton.get(state, {}).get(char, 'q_generic')  # q_generic as default state if no valid transitions
       
        read_word.append(char)  # Agrega el carácter directamente a read_word
      
        #print(f"Transition: {state} --({char})--> {next_state}")
        state = next_state




    read_word_str = ''.join(read_word)



    if state == 'd6' or state == 'd45':  # Acceptance states
        if word in keywords:
            return (read_word_str, "KEYWORD")
        if word.isdigit():
            return (read_word_str, "NUMBER")
        if word in["=",">","<"]:
            return (read_word_str, "OPERATOR")
        
    elif state == 'd36':
        if word in ['(', ')', '"', ',']:
            return (word, "PUNCTUATION")
    elif state == 'd34':
        return (read_word_str, "INVALID IDENTIFIER")
    else:
        return (read_word_str,"IDENTIFIER")

def tokenize(processed_string, automaton, keywords):
    
    tokens = []

    for word in processed_string:
        processed_word, token_type = process_word(word, automaton, keywords)
        tokens.append((processed_word, token_type))


    return tokens


