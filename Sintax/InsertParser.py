from Sintax.TreeNode import TreeNode
'''
InsertQuery -> INSERT INTO Table Values ValesGroup
ValuesGroup -> “(“ Values ”)”  ValuesGroupPrime
ValuesGroupPrime -> “,” ValuesGroup | Epsilon
Values -> Value ValuePrime
ValuePrime -> “,” Value | Epsilon
Table -> IDENTIFIER
VALUE -> IDENTIFIER | NUMBER


TOP DOWN LL1
'''
class ParseInsert:
    def __init__(self, tokens):
        self.tokens = tokens 
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse_insert(self):
        """InsertQuery -> INSERT INTO Table VALUES ValuesGroup"""
        node = TreeNode("InsertQuery")

        if self.current_token and self.current_token[0] == 'INSERT':
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()

            if self.current_token and self.current_token[0] == 'INTO': 
                node.add_child(TreeNode('INTO'))
                self.next_token()

                if self.current_token and self.current_token[1] == 'IDENTIFIER': 
                    table_node = TreeNode("Table")
                    node.add_child(table_node)

                    table_name_node = TreeNode(self.current_token[0]) 
                    table_node.add_child(table_name_node)
                    self.next_token()
                    print(self.current_token[0])
                    if self.current_token and self.current_token[0] == 'VALUES': 
                        node.add_child(TreeNode('Values'))
                        self.next_token()
                        node.add_child(self.parse_values_group())
                    else:
                        raise Exception("Error: Se esperaba 'VALUES'")
                else:
                    raise Exception("Error: Se esperaba un IDENTIFIER para la tabla")
            else:
                raise Exception("Error: Se esperaba 'INTO'")
        else:
            raise Exception("Error: Se esperaba 'INSERT'")

        return node

    def parse_values_group(self): 
        """ValuesGroup -> '(' Values ')' ValuesGroupPrime"""
        node = TreeNode("ValuesGroup")

        if self.current_token and self.current_token[0] == '(': 
            #node.add_child(TreeNode('(')) 
            self.next_token() 
            node.add_child(self.parse_values()) 

            if self.current_token and self.current_token[0] == ')': 
                #node.add_child(TreeNode(')')) 
                self.next_token()
                node.add_child(self.parse_values_group_prime())  
            else:
                raise Exception("Error: Se esperaba ')'")
        else:
            raise Exception("Error: Se esperaba '('")

        return node

    def parse_values_group_prime(self):
        """ValuesGroupPrime -> ',' ValuesGroup | Epsilon"""
        node = TreeNode("ValuesGroupPrime")

        if self.current_token and self.current_token[0] == ',':  
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_values_group())
        else:
            node.add_child(TreeNode('Epsilon'))  

        return node

    def parse_values(self): 
        """Values -> Value ValuesPrime"""
        node = TreeNode("Values")
        node.add_child(self.parse_value())  
        node.add_child(self.parse_values_prime())

        return node

    def parse_values_prime(self):
        """ValuesPrime -> ',' Values | Epsilon"""
        node = TreeNode("ValuesPrime")

        if self.current_token and self.current_token[0] == ',':  
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_values()) 
        else:
            node.add_child(TreeNode('Epsilon')) 

        return node

    def parse_value(self):
        """Value -> IDENTIFIER | NUMBER"""
        node = TreeNode("Value")

        if self.current_token and self.current_token[0] == '"': 
            self.next_token()

            if self.current_token and self.current_token[1] == 'IDENTIFIER':
                node.add_child(TreeNode(self.current_token[0]))
                self.next_token()
            else:
                raise Exception("Error: Se esperaba un IDENTIFIER dentro de las comillas")

            if self.current_token and self.current_token[0] == '"': 
                self.next_token()
            else:
                raise Exception("Error: Se esperaba un cierre de comillas")
        elif self.current_token and self.current_token[1] == 'NUMBER':  
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()
        else:
            raise Exception("Error: Se esperaba un valor valido (NUMBER o cadena entre comillas)")

        return node