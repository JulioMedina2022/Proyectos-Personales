import os

def crearArchivo(NombreArchivo):
    with open(f"{NombreArchivo}.txt", "w", encoding="utf-8") as archivo:
        mensaje = input("Ingrese el mensaje que desea: ")
        archivo.write(f"{mensaje}.\n")
        print(f"Su archivo {NombreArchivo} fue creado con exito.")

def leerArchivo(NombreArchivo):
    try:
        with open(f"{NombreArchivo}.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            print(contenido)
    except FileNotFoundError:
        print(f"El archivo {NombreArchivo} no existe.")

def AgregarArchivo(NombreArchivo):
    with open(f"{NombreArchivo}.txt", "a", encoding="utf-8") as archivo:
        mensaje = input("Ingrese el mensaje que desea agregar: ")
        archivo.write(f"{mensaje}.\n")
        print("Mensaje editado.")

def ReemplazarContenido(NombreArchivo):
    with open(f"{NombreArchivo}.txt", "w", encoding="utf-8") as archivo:
        mensaje = input("Ingrese el mensaje que desea reemplazar: ")
        archivo.write(f"{mensaje}.\n")
        print("Mensaje reemplazado.")

def EliminarArchivo(NombreArchivo):
    try: 
        Elimi = f"{NombreArchivo}.txt"
        os.remove(Elimi)
        print(f"{NombreArchivo} fue eliminado exitosamente.")
    except FileExistsError:
        print(f"El archivo {NombreArchivo}.txt no existe")
    except Exception as e:
        print(f"Error al eliminar archivo: {e}")


while True:
    print("---------------------------------------------------")
    print("\n Bienvenido al gestor de notas personalizado.")
    print("\n 1. Crear un nuevo archivo.")
    print(" 2. Leer un archivo.")
    print(" 3. Escribir en un archivo.")
    print(" 4. Eliminar archivo.")
    print(" 5. Salir del programa.")
    print("---------------------------------------------------")

    try:
        eleccion = int(input("Ingrese una opción: "))

        if eleccion==1:
            print("\nIngresando...")
            NombreArchivo = input("Elige un nombre para tu archivo:")
            crearArchivo(NombreArchivo)

        elif eleccion == 2:
            print("\nIngresando...")
            NombreArchivo = input("Ingrese el nombre del archivo que desea leer.")
            leerArchivo(NombreArchivo)
        
        elif eleccion == 3:
            print("\n Ingresando...")
            NombreArchivo = input("Escriba el nombre del archivo que quiere seguir escribiendo:")
            try:
                while True:
                    print("\n Qué acción desea hacer?")
                    print("1. Agregar contenido al archivo.")
                    print("2. Reemplazar el contenido completamente.")
                    print("3. Salir al menú principal.")

                    try:
                        print("---------------------------------------")
                        eleccion2 = int(input("Ingrese una opción: "))

                        if eleccion2 == 1:
                            AgregarArchivo(NombreArchivo)
                            break

                        elif eleccion2 == 2:
                            ReemplazarContenido(NombreArchivo)
                            break
                        
                        elif eleccion2 == 3:
                            print("Saliendo al menú principal...")

                    except ValueError:
                        print("Ingrese un número (1-3).")
        
            except FileNotFoundError:
                print(f"El archivo {NombreArchivo} no existe.")

        elif eleccion == 4:
            NombreArchivo = input("Ingrese el nombre del archivo que desea eliminar: ")
            EliminarArchivo(NombreArchivo)
            print("Archivo eliminado.")

        elif eleccion == 5:
            print("Saliendo del programa...")
            break

    except ValueError:
        print("Ingrese un número (1-4).")



 
        





