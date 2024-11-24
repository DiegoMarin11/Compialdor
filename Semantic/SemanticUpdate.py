from Sintax.TreeNode import TreeNode

class SemanticUpdate:
    def __init__(self, esquema_base_datos):
        self.esquema_base_datos = esquema_base_datos

    def analize(self, node):
        if isinstance(node, TreeNode) and node.value == 'UpdateQuery':
            self.analize_update_query(node)

    def analize_update_query(self, node):
      
        table_node = next((child for child in node.children if child.value == 'Table'), None)
        if not table_node:
            raise Exception("Error: No se encontró la tabla en la consulta UPDATE.")
        
        table_name = table_node.children[0].value 
        if table_name not in self.esquema_base_datos:
            raise Exception(f"Error: La tabla '{table_name}' no existe en la base de datos.")
        
        print(f"Tabla '{table_name}' encontrada en la base de datos.") 

 
        assignments_node = next((child for child in node.children if child.value == 'Assignments'), None)
        if assignments_node:
            self.analize_assignments(assignments_node, table_name)

     
        where_clause_node = next((child for child in node.children if child.value == 'WhereClause'), None)
        if where_clause_node and len(where_clause_node.children) > 1:
            condition_node = where_clause_node.children[1] 
            if condition_node:
                self.analize_condition(condition_node, table_name)
        else:
            print("falta condicional")

    def analize_assignments(self, assignments_node, table_name):
      
        for assignment_node in assignments_node.children:
            if assignment_node.value == 'Assignment':
                column_node = next((child for child in assignment_node.children if child.value == 'Column'), None)
                value_node = next((child for child in assignment_node.children if child.value == 'Value'), None)

                if column_node and value_node:
                    column_name = column_node.children[0].value
                    value = value_node.children[0].value

                   
                    if column_name not in self.esquema_base_datos[table_name]:
                        raise Exception(f"Error: La columna '{column_name}' no existe en la tabla '{table_name}'.")

                    
                    column_type = self.esquema_base_datos[table_name][column_name]
                    self.analize_tipo(value, column_type, column_name)

    def analize_condition(self, condition_node, table_name):
        
        column_node = next((child for child in condition_node.children if child.value == "Column"), None)
        if not column_node:
            raise Exception("Error: Se esperaba una columna en la condición.")

        column_name = column_node.children[0].value
        if column_name not in self.esquema_base_datos[table_name]:
            raise Exception(f"Error: La columna '{column_name}' no existe en la tabla '{table_name}'.")

        
        operator_node = next((child for child in condition_node.children if child.value in ['=', '>', '<']), None)
        value_node = next((child for child in condition_node.children if child.value == "Value"), None)

        if operator_node and value_node:
            value = value_node.children[0].value
            column_type = self.esquema_base_datos[table_name][column_name]
            self.analize_tipo(value, column_type)

    def analize_tipo(self, value, column_type, column_name = None):
        
        if column_type == "INT":
            if not isinstance(value, str) and value.isdigit():
                raise Exception(f"Error: El valor '{value}' no es un numero entero esperado para la columna '{column_name}'.")
        elif column_type in ["VARCHAR"] and not isinstance(value, str):
            raise Exception(f"Error: El valor '{value}' no es una cadena esperada para la columna '{column_name}'.")
      
    
