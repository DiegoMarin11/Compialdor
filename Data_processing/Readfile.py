def read_file(inputfile):
    try:
        string = ""
        with open(inputfile, 'r') as file:
            lines = file.readlines()  # Lee cada línea por separado

            if not lines: #No se leyo nada
                print(f"Archivo{inputfile}vacio")
                return None


    # Procesa cada línea
        for line in lines:
            string = line.strip()  # Elimina espacios en blanco alrededor de la línea
        return string



    except FileNotFoundError:
        print(f"Error: Archivo no encontrado.")

    except IOError as e:
        print(f"Error: Entrada no valida.")
