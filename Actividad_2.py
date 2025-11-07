from sqlalchemy import create_engine, text
import pandas as pd

# Conexión a la BD
BD ='postgresql://neondb_owner:npg_fIiXbhue64mC@ep-summer-tooth-adr0lw79-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
engine = create_engine(BD)

# ---------------- FUNCIONES -------------------

# Verificar conexión
def Verif_Con():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Conexión establecida correctamente")
    except Exception as e:
        print("Error en la conexión con la Base de datos.")
        print(e)
        exit()

def In_Vendedor(nombre,ciudad):
    try:
        with engine.connect() as conn:
                consulta = text("""
                    INSERT INTO vendedores (nombre, ciudad) 
                    VALUES (:nombre, :ciudad)""")
                conn.execute(consulta,{"nombre":nombre,"ciudad":ciudad})
                conn.commit()
                print("Vendedor agregado con éxito.")
    except Exception as e:
        print("Error al agregar el vendedor.",e)

def In_Venta(vendedor_id,monto,fecha):
    try:
        with engine.connect() as conn:
            consulta = text("""
                            INSERT INTO venta (vendedor_id,monto,fecha)
                            VALUES (:vendedor_id,:monto,:fecha)
                            """)
            conn.execute(consulta,{"vendedor_id":vendedor_id,"monto":monto,"fecha":fecha})
            conn.commit()
            print("Venta agregada con éxito.")
    except Exception as e:
        print("Error al agregar venta.",e)
        
from sqlalchemy import text

def Consul_ventas_vendedor(nombre_vendedor):
    try:
        consulta = text("""
        SELECT v.id, v2.nombre AS vendedor, v.monto, v.fecha
        FROM venta v
        JOIN vendedores v2 ON v.vendedor_id = v2.id
        WHERE v2.nombre ILIKE :nombre
        """)

        with engine.connect() as conn:
            df = pd.read_sql(consulta, conn, params={"nombre": f"%{nombre_vendedor}%"})

        if df.empty:
            print("No se encontraron ventas para este vendedor.")
        else:
            print(df)
            exportar = input("¿Desea exportar el resultado a CSV? (s/n): ").lower()
            if exportar == "s":
                df.to_csv("ventas_por_vendedor.csv", index=False)
                print("Archivo 'ventas_por_vendedor.csv' exportado correctamente.")

            exportar2 = input("¿Desea exportar el resultado a Excel? (s/n): ").lower()
            if exportar2 == "s":
                df.to_excel("ventas_por_vendedor.xlsx", index=False)
                print("Archivo 'ventas_por_vendedor.xlsx' exportado correctamente.")

    except Exception as e:
        print("Error al consultar la venta:", e)

def mostrar_ventas():
    try:
        df = pd.read_sql(""" 
                        SELECT v.id, v2.nombre AS vendedor, v.monto, v.fecha
                        FROM venta v
                        JOIN vendedores v2 ON v.vendedor_id = v2.id
                        ORDER BY v.fecha DESC;
                        """,engine)
        print(df)
    except Exception as e:
        print("Error al mostrar ventas:",e)

def mostrar_vendedores():
    try:
        with engine.connect() as conn:
            df = pd.read_sql(""" SELECT * FROM vendedores;""",conn)
            if df.empty:
                print("No hay vendedores registrados...")
            else:
                print("\n--- Lista de vendedores ---")
                print(df.to_string(index=False))
    except Exception as e:
        print("Error al mostrar vendedores:",e)

def actualizar_vendedor(vendedor_id, nuevo_nombre, nueva_ciudad):
    """Actualiza los datos de un vendedor."""
    try:
        with engine.connect() as conn:
            consulta = text("""
                UPDATE vendedores
                SET nombre = :nombre, ciudad = :ciudad
                WHERE id = :id
            """)
            resultado = conn.execute(consulta, {
                "nombre": nuevo_nombre,
                "ciudad": nueva_ciudad,
                "id": vendedor_id
            })
            conn.commit()

            if resultado.rowcount == 0:
                print("No se encontró ningún vendedor con ese ID.")
            else:
                print("Datos del vendedor actualizados correctamente.")
    except Exception as e:
        print("Error al actualizar vendedor:", e)

from sqlalchemy import text

def eliminar_vendedor(id_vendedor):
    try:
        with engine.begin() as conn:
            # eliminamos las ventas del vendedor
            conn.execute(text("DELETE FROM venta WHERE vendedor_id = :id"), {"id": id_vendedor})

            # eliminamos al vendedor
            conn.execute(text("DELETE FROM vendedores WHERE id = :id"), {"id": id_vendedor})

        print("Vendedor y sus ventas eliminados correctamente.")
    except Exception as e:
        print("Error al eliminar vendedor:", e)


# Menú principal

def menu():
    while True:
        print("\n ------- GESTOR DE VENTAS 2.0 -------")
        print("1. Insertar vendedor.")
        print("2. Mostrar todos los vendedores.")
        print("3. Insertar venta.")
        print("4. Mostrar todas las ventas.")
        print("5. Consultar ventas por vendedor.")
        print("6. Actualizar vendedor.")
        print("7. Eliminar vendedor por ID.")
        print("8. Salir")

        try:
            eleccion = int(input("\nIngrese una opción: "))
            if eleccion == 1:
                nombre = input("Nombre del vendedor: ")
                ciudad = input("Ciudad: ")
                In_Vendedor(nombre,ciudad)
            elif eleccion == 2:
                mostrar_vendedores()
            elif eleccion == 3:
                vendedor_id = input("ID del vendedor: ")
                monto = input("Monto de la venta: ")
                fecha = input("Fecha (YYYY-MM-DD): ")
                In_Venta(vendedor_id,monto,fecha)
            elif eleccion == 4:
                mostrar_ventas()
            elif eleccion == 5:
                nombre = input("Ingresa el nombre del vendedor: ")
                Consul_ventas_vendedor(nombre)
            elif eleccion == 6:
                vendedor_id= int(input("ID del vendedor a actualizar: "))
                nuevo_nombre = input("Nuevo nombre: ")
                nueva_ciudad= input("Nueva ciudad: ")
                actualizar_vendedor(vendedor_id,nuevo_nombre,nueva_ciudad)
            elif eleccion == 7:
                vendedor_id=int(input("ID del vendedor a eliminar: "))
                eliminar_vendedor(vendedor_id)
            elif eleccion == 8:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

        except ValueError:
            print("Ingrese un número entre 1 y 5.")
        except Exception as e:
            print("Error:", e)

# Iniciar programa 
if __name__ == "__main__":
    Verif_Con()
    menu()