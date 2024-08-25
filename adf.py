import geopandas as gpd
import matplotlib.pyplot as plt

# Ruta al archivo GeoJSON
geojson_path = 'output.geojson'

# Leer el archivo GeoJSON con GeoPandas
gdf = gpd.read_file(geojson_path)

# Crear la visualización con Matplotlib
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', edgecolor='black')

# Ajustar el título y las etiquetas
ax.set_title('Visualización de GeoJSON con Matplotlib')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Mostrar el gráfico
plt.show()
