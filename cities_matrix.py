import openrouteservice
import time

city_dictionary = {
    0: {"nombre": "A Coruña", "coordenadas": (-8.4188, 43.3713)}, 
    1: {"nombre": "Álava", "coordenadas": (-2.6769, 42.8448)}, 
    2: {"nombre": "Albacete", "coordenadas": (-1.8555, 38.9976)}, 
    3: {"nombre": "Alicante", "coordenadas": (-0.4831, 38.3452)}, 
    4: {"nombre": "Almería", "coordenadas": (-2.4649, 36.8340)}, 
    5: {"nombre": "Asturias", "coordenadas": (-5.8611, 43.3614)}, 
    6: {"nombre": "Ávila", "coordenadas": (-4.7150, 40.6566)}, 
    7: {"nombre": "Badajoz", "coordenadas": (-6.9707, 38.8786)}, 
    8: {"nombre": "Barcelona", "coordenadas": (2.1734, 41.3851)}, 
    9: {"nombre": "Burgos", "coordenadas": (-3.7058, 42.3430)}, 
    10: {"nombre": "Cáceres", "coordenadas": (-6.3703, 39.4762)}, 
    11: {"nombre": "Cádiz", "coordenadas": (-6.2987, 36.5298)}, 
    12: {"nombre": "Castellón", "coordenadas": (-0.0488, 39.9864)}, 
    13: {"nombre": "Ciudad Real", "coordenadas": (-3.9270, 38.9863)}, 
    14: {"nombre": "Córdoba", "coordenadas": (-4.7794, 37.8882)}, 
    15: {"nombre": "Cuenca", "coordenadas": (-2.1374, 40.0712)}, 
    16: {"nombre": "Girona", "coordenadas": (2.8260, 41.9794)}, 
    17: {"nombre": "Granada", "coordenadas": (-3.6018, 37.1773)}, 
    18: {"nombre": "Guadalajara", "coordenadas": (-3.1667, 40.6333)}, 
    19: {"nombre": "Guipúzcoa", "coordenadas": (-2.0183, 43.3209)}, 
    20: {"nombre": "Huelva", "coordenadas": (-6.9500, 37.2664)}, 
    21: {"nombre": "Huesca", "coordenadas": (-0.4098, 42.1351)}, 
    22: {"nombre": "Jaén", "coordenadas": (-3.7888, 37.7796)}, 
    23: {"nombre": "La Rioja", "coordenadas": (-2.4456, 42.4650)}, 
    24: {"nombre": "León", "coordenadas": (-5.5667, 42.5986)}, 
    25: {"nombre": "Lleida", "coordenadas": (0.6223, 41.6178)}, 
    26: {"nombre": "Lugo", "coordenadas": (-7.5560, 43.0129)}, 
    27: {"nombre": "Madrid", "coordenadas": (-3.7026, 40.4168)}, 
    28: {"nombre": "Málaga", "coordenadas": (-4.4214, 36.7213)}, 
    29: {"nombre": "Murcia", "coordenadas": (-1.1307, 37.9922)}, 
    30: {"nombre": "Navarra", "coordenadas": (-1.6761, 42.6954)}, 
    31: {"nombre": "Ourense", "coordenadas": (-7.8639, 42.3409)}, 
    32: {"nombre": "Palencia", "coordenadas": (-4.5250, 42.0095)}, 
    33: {"nombre": "Pontevedra", "coordenadas": (-8.6446, 42.4312)}, 
    34: {"nombre": "Salamanca", "coordenadas": (-5.6639, 40.9701)}, 
    35: {"nombre": "Segovia", "coordenadas": (-4.1216, 40.9493)}, 
    36: {"nombre": "Sevilla", "coordenadas": (-5.9869, 37.3772)}, 
    37: {"nombre": "Soria", "coordenadas": (-2.4717, 41.7668)}, 
    38: {"nombre": "Tarragona", "coordenadas": (1.2561, 41.1189)}, 
    39: {"nombre": "Teruel", "coordenadas": (-1.1065, 40.3456)}, 
    40: {"nombre": "Toledo", "coordenadas": (-4.0244, 39.8628)}, 
    41: {"nombre": "Valencia", "coordenadas": (-0.3763, 39.4699)}, 
    42: {"nombre": "Valladolid", "coordenadas": (-4.7245, 41.6523)}, 
    43: {"nombre": "Zaragoza", "coordenadas": (-0.8773, 41.6560)}
}



# New client with key
client = openrouteservice.Client(key='keyy') #own API key

#path to the txt 
file_path = "distances_matrix.txt"


#return distance between two cities
def get_distance_between_cities(a_coord: str, b_coord: str) -> int:
    # Obtain distance between cities
    try:
        # Request route between coordinates
        ruta = client.directions(coordinates=[a_coord, b_coord])
        # Extract distance from route response and convert to kilometers
        distance = ruta['routes'][0]['summary']['distance'] / 1000
    except KeyError:
        # If the same city is provided, return 0
        return 0
    except openrouteservice.exceptions.ApiError as e:
        # Handle API errors
        
        print(a_coord)
        print(b_coord)
        time.sleep(5)  # Pause for 5 seconds
        return get_distance_between_cities(a_coord, b_coord)  # Retry the request

    return distance

def calculate_distance_matrix():
    num_cities = len(city_dictionary)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]  # Inicialize

    for i in range(num_cities):
        for j in range(i+1, num_cities):  # Evita calcular la distancia de una ciudad consigo misma
            coord1 = city_dictionary[i]["coordenadas"]
            coord2 = city_dictionary[j]["coordenadas"]
            distance = get_distance_between_cities(coord1, coord2)
            print(distance)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance  # La matriz es simétrica

    return distance_matrix


def write_file(data):
    # Open the file or create it if it doesn't exist
    with open(file_path, "w") as open_file:
        # Write data to the file
        for row in data:
            # Convert each row of the matrix to a string and write to the file
            row_str = " ".join(str(distance) for distance in row)
            open_file.write(row_str + "\n")

    
if __name__ == "__main__":
    #we generate in a txt file distances matrix
    data=calculate_distance_matrix()
    write_file(data)