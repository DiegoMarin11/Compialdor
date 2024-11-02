from Sintax.TreeNode import TreeNode
'''

SelectQuery -> SELECT Columns FROM Table WhereClause
Columns -> * | ColumnList
ColumnList -> Column | Column "," ColumnList
WhereClause -> WHERE Condition | Epsilon
Condition -> Column Operator Value
Operator -> "=" | ">" | "<"
Column -> IDENTIFIER
Table -> IDENTIFIER
Value -> IDENTIFIER | NUMBER


'''
class ParseSelect:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else None

    def parse_select(self):
        """SelectQuery -> SELECT Columns FROM Table WhereClause"""
        node = TreeNode("SelectQuery")

        if self.current_token and self.current_token[0] == 'SELECT':
            node.add_child(TreeNode('SELECT'))
            self.next_token()

            node.add_child(self.parse_columns())

            if self.current_token and self.current_token[0] == 'FROM':
                node.add_child(TreeNode('FROM'))
                self.next_token()

                if self.current_token and self.current_token[1] == 'IDENTIFIER':
                    table_node = TreeNode(f"Table({self.current_token[0]})")
                    node.add_child(table_node)
                    self.next_token()
                    node.add_child(self.parse_where_clause())
                else:
                    raise Exception("Error: Se esperaba un IDENTIFIER para la tabla")
            else:
                raise Exception("Error: Se esperaba 'FROM'")
        else:
            raise Exception("Error: Se esperaba 'SELECT'")

        return node

    def parse_columns(self):
        """Columns -> * | ColumnList"""
        node = TreeNode("Columns")

        if self.current_token and self.current_token[0] == '*':
            node.add_child(TreeNode('*'))
            self.next_token()
        else:
            node.add_child(self.parse_column_list()) 

        return node

    def parse_column_list(self):
        """ColumnList -> Column | Column ',' ColumnList"""
        node = TreeNode("ColumnList")
        node.add_child(self.parse_column())

        if self.current_token and self.current_token[0] == ',':
            node.add_child(TreeNode(','))
            self.next_token()
            node.add_child(self.parse_column_list())

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
