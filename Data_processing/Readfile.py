def read_file(inputfile):
    try:
        string = ""
        with open(inputfile, 'r') as file:
            # Lee todo el contenido del archivo como una sola cadena
            content = file.read()

            if not content:  # Si el archivo está vacío
                print(f"Archivo {inputfile} vacío")
                return None

            # Reemplaza los saltos de línea por espacios
            string = content.replace('\n', ' ').strip()  # Elimina espacios adicionales al principio o final
        return string

    except FileNotFoundError:
        print(f"Error: Archivo {inputfile} no encontrado.")
        return None

    except IOError as e:
        print(f"Error: Entrada no válida.")
        return None