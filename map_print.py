import geopandas as gpd
import matplotlib.pyplot as plt
from cities_matrix import city_dictionary
import warnings

#ignore gdp futurewarning
warnings.filterwarnings("ignore")

def print_in_map(cromosome: list[int], ax):
    ax.clear()

    # Dibujar el mapa de España
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    spain = world[world.name == "Spain"]
    spain.plot(ax=ax, color='white', edgecolor='black')

    # Dibujar los puntos de las ciudades
    for idx, ciudad in city_dictionary.items():
        ax.plot(ciudad["coordenadas"][0], ciudad["coordenadas"][1], 'ro')
        ax.text(ciudad["coordenadas"][0], ciudad["coordenadas"][1], '  ' + ciudad["nombre"], fontsize=9)

    # Dibujar las líneas entre las ciudades en el orden del cromosoma
    for i in range(len(cromosome)):
        ciudad_actual = city_dictionary[cromosome[i]]
        ciudad_siguiente = city_dictionary[cromosome[(i + 1) % len(cromosome)]]
        x_actual, y_actual = ciudad_actual["coordenadas"]
        x_siguiente, y_siguiente = ciudad_siguiente["coordenadas"]
        ax.plot([x_actual, x_siguiente], [y_actual, y_siguiente], 'k-')
        ax.text((x_actual + x_siguiente) / 2, (y_actual + y_siguiente) / 2, str(i + 1), horizontalalignment='center', verticalalignment='center')

    plt.title('Mapa de España con ciudades')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.pause(0.01)  # Pausa la ejecución para permitir que se actualice la ventana


def print_final(cromosome: list[int]):
    plt.close()  # Cierra la ventana actual antes de abrir una nueva

    # Cargar el archivo shapefile de España
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Filtrar España
    spain = world[world.name == "Spain"]

    # Dibujar el mapa de España
    fig, ax = plt.subplots(figsize=(10, 10))
    spain.plot(ax=ax, color='white', edgecolor='black')

    # Dibujar los puntos de las ciudades
    for idx, ciudad in city_dictionary.items():
        ax.plot(ciudad["coordenadas"][0], ciudad["coordenadas"][1], 'ro')
        ax.text(ciudad["coordenadas"][0], ciudad["coordenadas"][1], '  ' + ciudad["nombre"], fontsize=9)

    # Dibujar las líneas entre las ciudades en el orden del cromosoma
    for i in range(len(cromosome)):
        ciudad_actual = city_dictionary[cromosome[i]]
        ciudad_siguiente = city_dictionary[cromosome[(i + 1) % len(cromosome)]]
        x_actual, y_actual = ciudad_actual["coordenadas"]
        x_siguiente, y_siguiente = ciudad_siguiente["coordenadas"]
        ax.plot([x_actual, x_siguiente], [y_actual, y_siguiente], 'k-')
        ax.text((x_actual + x_siguiente) / 2, (y_actual + y_siguiente) / 2, str(i + 1), horizontalalignment='center', verticalalignment='center')

    plt.title('Mapa de España con ciudades')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.show()