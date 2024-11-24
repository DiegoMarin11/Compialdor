from Sintax.TreeNode import TreeNode

class SemanticInsert:
    def __init__(self, esquema_base_datos):
        self.esquema_base_datos = esquema_base_datos

    def analize(self, node):
      
        if isinstance(node, TreeNode) and node.value == 'InsertQuery':
            self.analize_insert_query(node)

    def analize_insert_query(self, node):
      
        table_node = next((child for child in node.children if child.value == 'Table'), None)
        if not table_node:
            raise Exception("Error: No se encontró la tabla en la consulta INSERT.")
        
        table_name = table_node.children[0].value 
        if table_name not in self.esquema_base_datos:
            raise Exception(f"Error: La tabla '{table_name}' no existe en la base de datos.")
        
        print(f"Tabla '{table_name}' encontrada en la base de datos.")

        value_nodes = self.search_values(node)

       
        num_columns = len(self.esquema_base_datos[table_name])  
        total_values = len(value_nodes)
        if total_values != num_columns:
            raise Exception(f"Error: El número de valores ({total_values}) no coincide con el número de columnas ({num_columns}) en la tabla '{table_name}'.")

      
        columns = list(self.esquema_base_datos[table_name].keys())
        current_column = 0

        for value_node in value_nodes:
            value = value_node.children[0].value 
            column_name = columns[current_column] 
            column_type = self.esquema_base_datos[table_name][column_name] 

            # Verificar tipo de datos
            self.analize_tipo(value, column_type, column_name)
            current_column += 1

    def search_values(self, node):
        """Recorre el árbol y busca todos los nodos 'Value'"""
        value_nodes = []

        if isinstance(node, TreeNode):
            if node.value == 'Value':
                value_nodes.append(node)
            else:
                for child in node.children:
                    value_nodes.extend(self.search_values(child)) 

        return value_nodes

    def analize_tipo(self, value, column_type, column_name):
            """Verifica que el tipo de dato sea compatible con el tipo de la columna"""
           
            if (value.isdigit()):
                print(f"Valor numérico: {value} ")
         
            elif isinstance(value, str):
                print(f"Valor de cadena: '{value}' ")

            else:
                raise Exception(f"Error: Tipo de valor '{value}' no reconocido para la columna '{column_name}'.")