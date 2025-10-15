import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("pastel")
plt.rcParams["figure.autolayout"]=True

#1 Cargar los datos.
datos = pd.read_csv("ventas_500.csv")

print("------------ Analisis de datos ------------")
# imprimir los primeros datos del archivo csv.
print(datos.head(11),"\n")

#2 Normalizar nombres de columnas (minúsculas y sin espacios).
datos.columns=datos.columns.str.strip().str.lower()

#3 Convertir la columna fecha en Datetime.
datos["fecha"]=pd.to_datetime(datos["fecha"])

#4 Limpiar los datos (eliminando ventas en 0 o negativo)
datos_limpios=datos[datos["monto"]>0].copy()
print("\n ------------- Datos limpios. -------------")
print(datos_limpios.head(10), "\n")  # imprimir los primeros 10 datos limpios.

#5 Mostrar ventas en 0 o negativo.
datos_negativos=datos[datos["monto"]<=0].copy()
print("\n ----------- Ventas negativas. -----------")
print(datos_negativos.head(10),"\n")

#Total de ventas por vendedor.
Total_vendedor=datos_limpios.groupby("vendedor")["monto"].sum().reset_index(name="Total_Vendido")
print("\n Total de ventas por vendedor.")
print(Total_vendedor,"\n")

#Total ventas por ciudad.
Total_ciudad=datos_limpios.groupby("ciudad")["monto"].sum().reset_index(name="Total_Vendido")
print("\n Total de ventas por ciudad.")
print(Total_ciudad,"\n")

#Total ventas mensuales.
datos_limpios.loc[:,"mes"]=datos_limpios["fecha"].dt.to_period("M")   # Extraer mes
Total_mes = datos_limpios.groupby("mes")["monto"].sum().reset_index(name="Total_Vendido")
print("\n Total vendido por mes.")
print(Total_mes,"\n")

#Total ventas año.
datos_limpios.loc[:,"año"]=datos_limpios["fecha"].dt.to_period("Y") # extraer año
Total_año = datos_limpios.groupby("año")["monto"].sum().reset_index(name="Total_vendido")
print("\n Total vendido por año.")
print(Total_año,"\n")

#Estadisticas con datos limpios
prom=datos_limpios["monto"].mean()
median=datos_limpios["monto"].median()
desvi=datos_limpios["monto"].std()

# Estadisticas con todos los datos.
estadisticas=datos["monto"].describe()

print(f"El promedio es de: {prom:.2f}") # 2f = 2 decimales después de la coma.
print(f"La mediana es de: {median:.2f}")
print(f"La desviación es de: {desvi:.2f}")
print("\nLas estadísticas básicas es de: ")
print(estadisticas)

#exportar resultados por separado.
datos_limpios.to_csv("Ventas-sin datos negativos.csv",index=False)
datos_negativos.to_csv("Ventas negativas.csv", index=False)
Total_vendedor.to_csv("Ventas_por_vendedor.csv", index=False)
Total_ciudad.to_csv("Ventas_por_ciudad.csv", index=False)
Total_mes.to_csv("Ventas_por_mes.csv", index=False)
Total_año.to_csv("Ventas_por_año.csv",index=False)

# Exportar resultados a un excel todo junto.
with pd.ExcelWriter("Analisis_ventas.xlsx") as writer:
    datos_limpios.to_excel(writer, sheet_name="Ventas Limpias", index=False)
    Total_vendedor.to_excel(writer, sheet_name="Por Vendedor", index=False)
    Total_ciudad.to_excel(writer, sheet_name="Por Ciudad", index=False)
    Total_mes.to_excel(writer, sheet_name="Por Mes", index=False)
    Total_año.to_excel(writer, sheet_name="Por año",index=False)
print("Resultados exportados.\n ")

# Grafico de datos.
df=datos_limpios

# Gráfico de barras - Ventas por vendedor.
Total_vendedor=df.groupby("vendedor")["monto"].sum().reset_index()
# el reset_index() devuelve un Dataframe limpio.
plt.Figure(figsize=(7,4))
sns.barplot(x="vendedor", y="monto", data=Total_vendedor) # crea un grafico de barras
plt.title("Ventas totales por vendedor", fontsize=14, weight="bold") # titulo del gráfico, tamaño 14 y en negrita
plt.ylabel("Monto total ($)")
plt.xlabel("Vendedor")
plt.show()

# Grafico de barras horizontal - Ventas por ciudad.
Total_ciudad=df.groupby("ciudad")["monto"].sum().reset_index()
plt.Figure(figsize=(7,4))
sns.barplot(x="monto", y="ciudad", data=Total_ciudad)
plt.title("Ventas totales por ciudad", fontsize=14, weight="bold")
plt.xlabel("Monto total")
plt.ylabel("Ciudad")
plt.show()

# Grafico de lineas - Ventas por mes.
# Convierte el periodo a texto para que se vea en el eje X
Total_mes=df.groupby(df["fecha"].dt.to_period("M"))["monto"].sum().reset_index()
Total_mes["fecha"] = Total_mes["fecha"].astype(str)  
plt.figure(figsize=(7,4))
# Gráfico de líneas con marcador en cada punto
sns.lineplot(x="fecha", y="monto", data=Total_mes, marker="o")
plt.title("Ventas Totales por Mes", fontsize=14, weight="bold")
plt.xlabel("Mes")
plt.ylabel("Monto Total ($)")
plt.show()

# Boxplot - Distribución por vendedor.
plt.Figure(figsize=(7,4))
sns.boxplot(x="vendedor",y="monto", data=df)
plt.title("Distribucion de ventas por vendedor", fontsize=14, weight="bold")
plt.ylabel("Monto por vendedor")
plt.xlabel("Vendedor")
plt.show()

# Histograma - Frecuencia de montos.
plt.Figure(figsize=(6,4))
sns.histplot(df["monto"], bins=10, kde=True)
plt.title("Distribucion de Montos de venta", fontsize=14, weight="bold")
plt.xlabel("Monto")
plt.ylabel("Frecuencia")
plt.show()

# Gráfico de dispersión - Relación fecha/monto.
plt.Figure(figsize=(7,4))
sns.scatterplot(x="fecha", y="monto", hue="vendedor", size="monto", data=df, sizes=(50,200))
plt.title("Ventas por fecha y monto", fontsize=14, weight="bold")
plt.xlabel("Fecha")
plt.ylabel("Monto")
plt.xticks(rotation=45) 
plt.show()
