# CONCLUSIONES DEL ANÁLISIS:
# 1. El departamento con más casos es: [piura con 239078 casos]
# 2. La mayoría de los casos son de tipo: [clínico]
# 3. La columna con más datos vacíos es: [localcod con 149652 cantidad de datos vacíos]
import pandas as pd

# 1. Cargar el archivo 
df = pd.read_csv(r"C:\Users\Carlos\OneDrive\Documentos\datos_abiertos_vigilancia_dengue_2000_2024.csv.csv")

# 2. Ver las primeras 5 filas
print(df.head())

# 3. Ver cuántas filas y columnas tiene
print(f"El dataset tiene {df.shape[0]} filas y {df.shape[1]} columnas")

# 4. Ver los nombres de las columnas
print(df.columns)
 # 5. ¿Qué departamentos tienen más casos registrados? (Top 5)
print("\n--- Top 5 Departamentos con más casos ---")
print(df['departamento'].value_counts().head(5))

# 6. ¿Cuántos casos hay por tipo de diagnóstico?
print("\n--- Casos por tipo de diagnóstico ---")
print(df['tipo_dx'].value_counts())

# 7. ¿Hay valores vacíos en nuestro dataset?
print("\n--- Valores vacíos por columna ---")
print(df.isnull().sum())

import matplotlib.pyplot as plt
import seaborn as sns

# 8. Filtrar los 5 departamentos con más casos
top_departamentos = df['departamento'].value_counts().head(5)

# 9. Crear la figura
plt.figure(figsize=(10, 6)) # Esto hace el gráfico más grande

# 10. Hacer el gráfico de barras
sns.barplot(x=top_departamentos.index, y=top_departamentos.values, palette="viridis")

# 11. Ponerle título y nombres a los ejes
plt.title("Top 5 Departamentos con más Casos de Dengue en Perú", fontsize=16)
plt.xlabel("Departamento", fontsize=12)
plt.ylabel("Número de Casos", fontsize=12)

# 12. Mostrar el gráfico
plt.savefig("grafico_dengue_top5.png")
plt.show()