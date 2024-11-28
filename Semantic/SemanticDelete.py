from Sintax.TreeNode import TreeNode

class SemanticDelete:
    def __init__(self, esquema_base_datos):
        self.esquema_base_datos = esquema_base_datos

    def analize(self, node):
        if isinstance(node, TreeNode):
            
            #print("Top tree ",node.value)
            if node.value == 'DeleteQuery':
                self.analize_delete_query(node)

    def analize_delete_query(self, node):
        
        table_node = next((child for child in node.children if child.value == "Table"), None)
        if not table_node:
            raise Exception("Error: No se encontro la tabla en la consulta DELETE.")
        
        table_name = table_node.children[0].value  
        if table_name not in self.esquema_base_datos:
            raise Exception(f"Error: La tabla '{table_name}' no existe en la base de datos.")
        
        print(f"Tabla '{table_name}' encontrada en la base de datos.")
        
        
        where_clause_node = next((child for child in node.children if child.value == 'WhereClause'), None)
        if where_clause_node:
            self.analize_where_clause(where_clause_node, table_name)

    def analize_where_clause(self, where_clause_node, table_name):
        condition_node = next((child for child in where_clause_node.children if child.value == 'Condition'), None)
        if condition_node:
            self.analize_condition(condition_node, table_name)

    def analize_condition(self, condition_node, table_name):

        column_node = next((child for child in condition_node.children if child.value == "Column"), None)
        if not column_node:
            raise Exception("Error: Se esperaba una columna en la condicion.")
        
        column_name = column_node.children[0].value  
        if column_name not in self.esquema_base_datos[table_name]:
            raise Exception(f"Error: La columna '{column_name}' no existe en la tabla '{table_name}'.")

        column_type = self.esquema_base_datos[table_name][column_name]
        print(f"Columna '{column_name}' encontrada en la tabla '{table_name}' con tipo '{column_type}'.")

        operator_node = next((child for child in condition_node.children if child.value in ['=', '>', '<']), None)
        if not operator_node:
            raise Exception("Error: Se esperaba un operador (=, >, <) en la condicion.")
        print(f"Operador '{operator_node.value}' valido.")

        value_node = next((child for child in condition_node.children if child.value == "Value"), None)
        if not value_node:
            raise Exception("Error: Se esperaba un valor en la condicion.")

        value = value_node.children[0].value
        self.validate_value(value, column_type, column_name)

    def validate_value(self, value, column_type, column_name):
        if column_type == "INT":
            if isinstance(value, str) and not value.isdigit():
                raise Exception(f"Error: El valor '{value}' no es un numero entero valido para la columna '{column_name}'.")
            elif not isinstance(value, (int, str)):
                raise Exception(f"Error: El valor '{value}' no es un numero valido para la columna '{column_name}'.")

        elif column_type in ["VARCHAR"]:
            if not isinstance(value, str):
                raise Exception(f"Error: El valor '{value}' no es una cadena valida para la columna '{column_name}'.")

        else:
            raise Exception(f"Error: Tipo de columna '{column_type}' no soportado.")
        
        print(f"Valor '{value}' valido para la columna '{column_name}' de tipo '{column_type}'.")