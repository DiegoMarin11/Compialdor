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

        if self.current_token[0] == 'INSERT':
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()

            if self.current_token[0] == 'INTO': 
                node.add_child(TreeNode('INTO'))
                self.next_token()

                if self.current_token[1] == 'IDENTIFIER': 
                    table_node = TreeNode(f"Table({self.current_token[0]})") 
                    node.add_child(table_node)
                    self.next_token()

                    if self.current_token[0] == 'VALUES': 
                        node.add_child(TreeNode('VALUES'))
                        self.next_token()

                        # Llamamos a parse_values_group para procesar los valores
                        node.add_child(self.parse_values_group())

        return node

    def parse_values_group(self): 
        """ValuesGroup -> '(' Values ')' ValuesGroupPrime"""

        node = TreeNode("ValuesGroup")

        if self.current_token[0] == '(': 
            node.add_child(TreeNode('(')) 
            self.next_token() 
            node.add_child(self.parse_values())  # Procesamos el grupo de valores

            if self.current_token[0] == ')': 
                node.add_child(TreeNode(')')) 
                self.next_token()

                # Verificamos si hay otro grupo de valores
                node.add_child(self.parse_values_group_prime())  

        return node

    def parse_values_group_prime(self):
        """ValuesGroupPrime -> ',' ValuesGroup | Epsilon"""
        node = TreeNode("ValuesGroupPrime")

        if self.current_token and self.current_token[0] == ',':  # Si hay una coma, procesamos otro grupo de valores
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_values_group())
        else:
            node.add_child(TreeNode('Epsilon'))  # Producción vacía

        return node

    def parse_values(self): 
        """Values -> Value ValuesPrime"""
        node = TreeNode("Values")

        # Parseamos el primer valor
        node.add_child(self.parse_value())  

        # Llamamos a ValuesPrime para procesar más valores si es necesario
        node.add_child(self.parse_values_prime())

        return node

    def parse_values_prime(self):
        """ValuesPrime -> ',' Values | Epsilon"""
        node = TreeNode("ValuesPrime")

        if self.current_token and self.current_token[0] == ',':  # Si hay una coma, procesamos más valores
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_values())  # Recursión correcta para más valores
        else:
            node.add_child(TreeNode('Epsilon'))  # Producción vacía si no hay más valores

        return node

    def parse_value(self):
        """Value -> IDENTIFIER | NUMBER"""
        node = TreeNode("Value")

        # Ignoramos comillas dobles
        if self.current_token[0] == '"':
            self.next_token()

            if self.current_token[1] == 'IDENTIFIER' or self.current_token[1] == 'NUMBER':
                node.add_child(TreeNode(self.current_token[0]))
                self.next_token()

            if self.current_token[0] == '"':  # Ignoramos la comilla final
                self.next_token()
        elif self.current_token[1] == 'IDENTIFIER' or self.current_token[1] == 'NUMBER':
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()
        else:
            raise Exception("Error: Se esperaba un IDENTIFIER o NUMBER")

        return node
