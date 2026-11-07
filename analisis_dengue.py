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
# 13. ¿Qué porcentaje de la columna 'localcod' son nulos?
porcentaje_nulos = (df['localcod'].isnull().sum() / len(df)) * 100
print(f"El porcentaje de nulos en 'localcod' es: {porcentaje_nulos:.2f}%")

# 14. Llenar los nulos de 'localcod' con un texto descriptivo
# En lugar de dejar vacíos (NaN), le pondremos "NO REGISTRADO"
df['localcod'] = df['localcod'].fillna('NO REGISTRADO')

# 15. Verificar que ya no haya nulos en esa columna
print("\n--- Nulos restantes en 'localcod' después de la limpieza ---")
print(df['localcod'].isnull().sum())
# 16. Agrupar los casos por año para ver la evolución
casos_por_ano = df['ano'].value_counts().sort_index()

# 17. Crear el gráfico de líneas
plt.figure(figsize=(12, 6))
sns.lineplot(x=casos_por_ano.index, y=casos_por_ano.values, marker='o', color='red')

plt.title("Evolución Histórica de Casos de Dengue en Perú")
plt.xlabel("Año")
plt.ylabel("Número de Casos")
plt.grid(True) # Esto pone una cuadrícula de fondo

# Guardar el gráfico como imagen ANTES de mostrarlo
plt.savefig("grafico_evolucion_dengue.png") 

plt.show()
# ==========================================
# PREPARACIÓN PARA MACHINE LEARNING
# ==========================================
from sklearn.model_selection import train_test_split

# 18. Elegir nuestras "pistas" (Features) y nuestra "respuesta" (Target)
# Vamos a usar la edad, el sexo y el departamento como pistas.
# Nuestra respuesta será el tipo de diagnóstico (tipo_dx).

# Para que el modelo entienda las letras (como "Piura" o "M"), 
# las convertimos en números (0, 1, 2...).
df_ml = df[['edad', 'sexo', 'departamento', 'tipo_dx']].dropna().copy()

df_ml['sexo_num'] = df_ml['sexo'].map({'M': 1, 'F': 0}) # Masculino=1, Femenino=0
df_ml['depto_num'] = df_ml['departamento'].astype('category').cat.codes

# Definimos X (las pistas) e y (la respuesta)
X = df_ml[['edad', 'sexo_num', 'depto_num']]
y = df_ml['tipo_dx']

# 19. Dividir los datos: 80% para entrenar al modelo, 20% para evaluarlo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n--- Datos listos para Machine Learning ---")
print(f"Filas para entrenar (X_train): {X_train.shape[0]}")
print(f"Filas para evaluar (X_test): {X_test.shape[0]}")
# ==========================================
# ENTRENANDO EL MODELO
# ==========================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 20. Crear el modelo (como un bebé que aún no sabe nada)
modelo = RandomForestClassifier(random_state=42, class_weight='balanced')

# 21. Entrenar al modelo (¡aquí aprende!)
print("\nEntrenando el modelo...")
modelo.fit(X_train, y_train)

# 22. Hacer que el modelo prediga en los datos que NUNCA vio (el examen)
predicciones = modelo.predict(X_test)

# 23. Evaluar qué tan bueno es
precision = accuracy_score(y_test, predicciones)
print(f"\nPrecisión del modelo: {precision * 100:.2f}%")

# 24. Ver un resumen más detallado
print("\n--- Reporte de Clasificación ---")
print(classification_report(y_test, predicciones))
# 25. Obtener la importancia de cada variable (Feature Importance)
importancias = modelo.feature_importances_
# 26. Crear una pequeña tabla para verlo ordenado
import pandas as pd
tabla_importancia = pd.DataFrame({
    'Variable': X.columns,
    'Importancia': importancias
}).sort_values(by='Importancia', ascending=False)

print("\n--- ¿Qué pista (variable) fue la más importante para el modelo? ---")
print(tabla_importancia)

# 27. Graficar la importancia
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))
sns.barplot(x='Importancia', y='Variable', data=tabla_importancia, palette='magma')
plt.title("¿Qué variables importan más para predecir el Dengue?")
plt.xlabel("Nivel de Importancia")
plt.ylabel("Variable")
plt.savefig("grafico_importancia_variables.png")
plt.show()

