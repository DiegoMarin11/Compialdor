from Sintax.TreeNode import TreeNode
'''
UpdateQuery -> UPDATE Table SET Assignments WhereClause
Assignments -> Assignment | Assignment "," Assignments
Assignment -> Column "=" Value
WhereClause -> WHERE Condition | Epsilon
Condition -> Column Operator Value
Operator -> "=" | ">" | "<"
Column -> IDENTIFIER
Table -> IDENTIFIER
Value -> IDENTIFIER | NUMBER


'''

class ParseUpdate:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse_update(self):
        """UpdateQuery -> UPDATE Table SET Assignments WhereClause"""
        node = TreeNode("UpdateQuery")

        if self.current_token and self.current_token[0] == 'UPDATE':
            node.add_child(TreeNode('UPDATE'))
            self.next_token()

            if self.current_token and self.current_token[1] == 'IDENTIFIER':
                table_node = TreeNode(f"Table({self.current_token[0]})")
                node.add_child(table_node)
                self.next_token()

                if self.current_token and self.current_token[0] == 'SET':
                    node.add_child(TreeNode('SET'))
                    self.next_token()
                    node.add_child(self.parse_assignments())
                    node.add_child(self.parse_where_clause())
                else:
                    raise Exception("Error: Se esperaba 'SET'")
            else:
                raise Exception("Error: Se esperaba un IDENTIFIER para la tabla")
        else:
            raise Exception("Error: Se esperaba 'UPDATE'")

        return node

    def parse_assignments(self):
        """Assignments -> Assignment | Assignment ',' Assignments"""
        node = TreeNode("Assignments")
        node.add_child(self.parse_assignment())

        if self.current_token and self.current_token[0] == ',':
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_assignments())

        return node

    def parse_assignment(self):
        """Assignment -> Column '=' Value"""
        node = TreeNode("Assignment")
        node.add_child(self.parse_column())

        if self.current_token and self.current_token[0] == '=':
            node.add_child(TreeNode('='))
            self.next_token()
            node.add_child(self.parse_value())
        else:
            raise Exception("Error: Se esperaba un '=' para la asignación")

        return node

    def parse_column(self):
        """Column -> IDENTIFIER"""
        node = TreeNode("Column")

        if self.current_token and self.current_token[1] == 'IDENTIFIER':
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()
        else:
            raise Exception("Error: Se esperaba un IDENTIFIER para la columna")

        return node

    def parse_where_clause(self):
        """WhereClause -> WHERE Condition | Epsilon"""
        node = TreeNode("WhereClause")

        if self.current_token and self.current_token[0] == 'WHERE':
            node.add_child(TreeNode('WHERE'))
            self.next_token()
            node.add_child(self.parse_condition())
        else:
            node.add_child(TreeNode('Epsilon'))

        return node

    def parse_condition(self):
        """Condition -> Column Operator Value"""
        node = TreeNode("Condition")
        node.add_child(self.parse_column())

        if self.current_token and self.current_token[0] in ['=', '>', '<']:
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()
            node.add_child(self.parse_value())
        else:
            raise Exception("Error: Se esperaba un operador (=, >, <)")

        return node

    def parse_value(self):
        """Value -> IDENTIFIER | NUMBER"""
        node = TreeNode("Value")

        if self.current_token and self.current_token[1] in ['IDENTIFIER', 'NUMBER']:
            node.add_child(TreeNode(self.current_token[0]))
            self.next_token()
        else:
            raise Exception("Error: Se esperaba un IDENTIFIER o NUMBER para el valor")

        return node
