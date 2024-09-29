def replace_spaces(string):

 

               
        
    return string.replace(" ", "/")




def extract_words(string, delimiter='/'):
    words = []
    current_word = []
  

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

