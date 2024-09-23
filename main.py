from Lexer.LexerAnalyzer import *
from Resources.Keywords import *
from Resources.Automata import *
from Data_processing.Readfile import *
from Data_processing.ProcessString import *
from prettytable import PrettyTable

def print_table(tokens):
    table = PrettyTable()
    table.field_names = ["String", "Type"]

    for token in tokens:
        table.add_row(token)

    print(table)


if __name__ == "__main__":

    file =  './Resources/input.txt'
    string = read_file(file)

    if string:
        string_no_spaces = replace_spaces(string)
        processed_string = extract_words(string_no_spaces)
        tokens = tokenize(processed_string, Automaton, keywords)

        print_table(tokens)

        
    #print(tokens)
    

