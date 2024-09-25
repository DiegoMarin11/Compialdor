def replace_spaces(string):

 
    sub_expression = []
    inside_parentheses = False
    result = []
    for c in string:

        if c == "(":
            inside_parentheses = True
            result.append(c)

        elif c == ")":
            inside_parentheses = False 
            result.append("".join(sub_expression).replace(" ", ""))
            result.append(c)
            sub_expression = []
             
        elif inside_parentheses:
          
            sub_expression.append(c)
        
        elif c == " ":
            result.append("/")

        else:
            result.append(c)
           
        
    return "".join(result)


def extract_words(string, delimiter='/'):
    words = []
    current_word = []
    string = string.replace("Insertar/a/", "Insertar a/")

    #print(string)
    for char in string:
        if char == delimiter: #or char == ',':  # if char == _
            if current_word:
                words.append(''.join(current_word))
                current_word = []  # reset
        elif  char in ["(", ")", ",", '"']:
            if current_word:
                words.append(''.join(current_word))  
                current_word = []
            words.append(char)    
        else:
            current_word.append(char)
    
    if current_word:
        words.append(''.join(current_word))
    

    
    return words

