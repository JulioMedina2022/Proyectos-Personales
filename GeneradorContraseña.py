import random 
import string

def contraseña(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = "".join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

# Programa


print("----------------------------------------------------------")
print("\n Bienvenido al generador de contraseñas de Julio.")
print("\n-----------------------------------------------------------")
    
try:
    Longitud = int(input("Ingrese la longitud de la contraseña: "))
    password = contraseña(Longitud)
    print(f"Su contraseña es: {password}")
except ValueError:
    print("Ingrese un número entero.")


    
    