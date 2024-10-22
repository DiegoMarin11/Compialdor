from Lexer.LexerAnalyzer import *
from Resources.Keywords import *
from Resources.Automata import *
from Data_processing.Readfile import *
from Data_processing.ProcessString import *
from prettytable import PrettyTable
from Sintax.Parser import ParseInsert
def print_table(tokens):
    table = PrettyTable()
    table.field_names = ["String", "Type"]

    for token in tokens:
        table.add_row(token)

    print(table)


if __name__ == "__main__":

    file =  './Resources/input.txt'
    string = read_file(file)
    #print(string)
    if string:
        string_no_spaces = replace_spaces(string)
        #print(string_no_spaces)
        processed_string = extract_words(string_no_spaces)
        #print(processed_string)
        tokens = tokenize(processed_string, Automaton, keywords)

        #print_table(tokens)

                
        print(tokens)
        query_type = tokens[0][0]
        print(query_type)
        parse = ParseInsert(tokens)

        parse_tree = parse.parse_insert()
        
        
        parse_tree.print_productions()
    

