from Sintax.TreeNode import TreeNode


class SemanticSelect:
    def __init__(self, esquema_base_datos):
        self.esquema_base_datos = esquema_base_datos

    def analizar(self, node):
        if isinstance(node, TreeNode) and node.value == 'SelectQuery':
            self.analizar_select_query(node)

    def analizar_select_query(self, node):
  
        columns_node = next((child for child in node.children if child.value == 'Columns'), None)
        if columns_node:
            self.analizar_columns(columns_node)

    
        table_node = next((child for child in node.children if child.value == 'Table'), None)
        if not table_node:
            raise Exception("Error: No se encontró la tabla en la consulta SELECT.")
        
        table_name = table_node.children[0].value 
        if table_name not in self.esquema_base_datos:
            raise Exception(f"Error: La tabla '{table_name}' no existe en la base de datos.")
        
        print(f"Tabla '{table_name}' encontrada en la base de datos.")
        
    
        where_clause_node = next((child for child in node.children if child.value == 'WhereClause'), None)
        if where_clause_node:
            self.analizar_where_clause(where_clause_node, table_name)

    def analizar_columns(self, columns_node):
      
        for column_node in columns_node.children:
            if column_node.value == '*':
                print("Se seleccionaron todas las columnas.")
                continue 
            else:
                
                self.analizar_column(column_node)

    def analizar_column(self, column_node):
        column_name = column_node.value 

       
        found = False
        for table_name, columns in self.esquema_base_datos.items():
            if column_name in columns:
                print(f"Columna '{column_name}' válida en la tabla '{table_name}'.")
                found = True
                break

        if not found:
            raise Exception(f"Error: La columna '{column_name}' no existe en ninguna tabla.")

    def analizar_where_clause(self, where_clause_node, table_name):
        condition_node = next((child for child in where_clause_node.children if child.value == 'Condition'), None)
        if condition_node:
            self.analizar_condition(condition_node, table_name)

    def analizar_condition(self, condition_node, table_name):
       
        column_node = next((child for child in condition_node.children if child.value == "Column"), None)
        if column_node:
            column_name = column_node.children[0].value 
            if column_name not in self.esquema_base_datos[table_name]:
                raise Exception(f"Error: La columna '{column_name}' no existe en la tabla '{table_name}'.")
            
            column_type = self.esquema_base_datos[table_name][column_name]
            print(f"Columna '{column_name}' encontrada en la tabla '{table_name}' con tipo '{column_type}'.")
        
        # Verificar el valor
        value_node = next((child for child in condition_node.children if child.value == "Value"), None)
        if value_node:
            value = value_node.children[0].value  
            print(f"Valor en la condición: {value}")
            
            pass