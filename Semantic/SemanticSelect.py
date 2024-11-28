from Sintax.TreeNode import TreeNode


class SemanticSelect:
    def __init__(self, esquema_base_datos):
        self.esquema_base_datos = esquema_base_datos

    def analize(self, node):
        if isinstance(node, TreeNode) and node.value == 'SelectQuery':
            self.analize_select_query(node)

    def analize_select_query(self, node):
  
        columns_node = next((child for child in node.children if child.value == 'Columns'), None)
        if columns_node:
            self.analize_columns(columns_node)

    
        table_node = next((child for child in node.children if child.value == 'Table'), None)
        if not table_node:
            raise Exception("Error: No se encontro la tabla en la consulta SELECT.")
        
        table_name = table_node.children[0].value 
        if table_name not in self.esquema_base_datos:
            raise Exception(f"Error: La tabla '{table_name}' no existe en la base de datos.")
        
        print(f"Tabla '{table_name}' encontrada en la base de datos.")
        
    
        where_clause_node = next((child for child in node.children if child.value == 'WhereClause'), None)
        if where_clause_node:
            self.analize_where_clause(where_clause_node, table_name)

    def analize_columns(self, columns_node):
      
        for column_node in columns_node.children:
            if column_node.value == '*':
                #print("Se seleccionaron todas las columnas.")
                continue 
            elif column_node.value == 'ColumnList':
                # Ignorar `ColumnList` explícitamente.
                #print("Se ignoró ColumnList en la consulta.")
                continue
            else:
                
                self.analize_column(column_node)

    def analize_column(self, column_node):
        column_name = column_node.value 

       
        found = False
        for table_name, columns in self.esquema_base_datos.items():
            if column_name in columns:
                print(f"Columna '{column_name}' valida en la tabla '{table_name}'.")
                found = True
                break

        if not found:
            raise Exception(f"Error: La columna '{column_name}' no existe en ninguna tabla.")

    def analize_where_clause(self, where_clause_node, table_name):
        condition_node = next((child for child in where_clause_node.children if child.value == 'Condition'), None)
        if condition_node:
            self.analize_condition(condition_node, table_name)

    def analize_condition(self, condition_node, table_name):

        column_node = next((child for child in condition_node.children if child.value == "Column"), None)
        if not column_node:
            raise Exception("Error: Se esperaba una columna en la condición.")

        column_name = column_node.children[0].value
        if column_name not in self.esquema_base_datos[table_name]:
            raise Exception(f"Error: La columna '{column_name}' no existe en la tabla '{table_name}'.")

        column_type = self.esquema_base_datos[table_name][column_name]
        print(f"Columna '{column_name}' encontrada en la tabla '{table_name}' con tipo '{column_type}'.")

        operator_node = next((child for child in condition_node.children if child.value in ['=', '>', '<']), None)
        if not operator_node:
            raise Exception("Error: Se esperaba un operador valido (=, >, <) en la condición.")
        print(f"Operador '{operator_node.value}' válido.")

        value_node = next((child for child in condition_node.children if child.value == "Value"), None)
        if not value_node:
            raise Exception("Error: Se esperaba un valor en la condición.")

        value = value_node.children[0].value
        self.validate_value(value, column_type, column_name)

    def validate_value(self, value, column_type, column_name):
        """Valida que el valor sea compatible con el tipo de la columna."""
        if column_type == "INT":
            if isinstance(value, str) and not value.isdigit():
                raise Exception(f"Error: El valor '{value}' no es un número entero válido para la columna '{column_name}'.")
        elif column_type in ["VARCHAR", "TEXT"]:
            if not isinstance(value, str):
                raise Exception(f"Error: El valor '{value}' no es una cadena válida para la columna '{column_name}'.")
        else:
            raise Exception(f"Error: Tipo de columna '{column_type}' no soportado.")

        print(f"Valor '{value}' válido para la columna '{column_name}' de tipo '{column_type}'.")
