def replace_spaces(string):
    return string.replace(" ", "/")

def extract_words(string, delimiter='/'):
    words = []
    current_word = []
    
    for char in string:
        if char == delimiter:  # if char == _
            if current_word:
                words.append(''.join(current_word))
                current_word = []  # reset
        else:
            current_word.append(char)
    
    if current_word:
        words.append(''.join(current_word))
    
    return words