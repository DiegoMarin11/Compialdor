

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

  
  





    if state == 'd6' or state == 'd45':  # Acceptance states
        if word in keywords:
            return (keywords[word], "KEYWORD")
        if word.isdigit():
            return (word, "NUMBER")
        if word in["=",">","<"]:
            return (word, "OPERATOR")
        
    elif state == 'd36':
        if word in ['(', ')', '"', ',']:
            return (word, "PUNCTUATION")
    elif state == 'd34':
        return (word, "INVALID IDENTIFIER")
    else:
        return (word,"IDENTIFIER")

def tokenize(processed_string, automaton, keywords):
    
    tokens = []
    open_parentheses = 0
    closed_parentheses = 0 
    open_quotes = 0

    for word in processed_string:
        processed_word, token_type = process_word(word, automaton, keywords)
        tokens.append((processed_word, token_type))
        if processed_word == '(':
            open_parentheses += 1
        if processed_word == ')':
            closed_parentheses += 1
        
        if processed_word == '"':
            open_quotes += 1

    if open_parentheses != closed_parentheses:
        raise ValueError (word, "ERROR: Unbalanced parentheses")

   
    if open_quotes % 2 != 0:
        raise ValueError (word, "ERROR: Unmatched quotes")



    return tokens


