

def process_word(word, automaton, keywords):


    state = 'd0'
    read_word = []
    #print(word)
    for char in word:
        #print(char)
        transitions = automaton.get(state, {})
        next_state = transitions.get(char, 'q_generic')
        #next_state = automaton.get(state, {}).get(char, 'q_generic')  # q_generic as default state if no valid transitions
       
        read_word.append(char)  # Agrega el carácter directamente a read_word
      
        print(f"Transition: {state} --({char})--> {next_state}")
        state = next_state
    read_word_str = ''.join(read_word)

    if state == 'd6' or state == 'd45':  # Acceptance states
        if word in keywords:
            return (read_word_str, "KEYWORD")
        if word.isdigit():
            return (read_word_str, "NUMBER")
        if word == '=':
            return (read_word_str, "OPERATOR")
        
    elif state == 'd36':
        if word in ['(', ')', '"', ',']:
            return (word, "PUNCTUATION")
        #if is_value:#Does not work currently
         #   return (read_word_str,"VALUE")
    elif state == 'd34':
        return (read_word_str, "INVALID IDENTIFIER")
    else:
        return (read_word_str,"IDENTIFIER")

def tokenize(processed_string, automaton, keywords):
    
    tokens = []

    for word in processed_string:
        processed_word, token_type = process_word(word, automaton, keywords)
        tokens.append((processed_word, token_type))


    #Temporary workaround for values 
    for i in range(len(tokens)):
        current_token = tokens[i]

        if current_token[1] == "IDENTIFIER" or current_token[1] == "NUMBER":

            if i > 0 and tokens[i-1][0] == '"':  # Token anterior es una comilla
    
                if i < len(tokens) - 1 and tokens[i+1][0] == '"':
                    tokens[i] = (current_token[0], "VALUE")

    return tokens


