import  numpy as np
import matplotlib.pyplot as plt
import random

SEMILLA = 17
TAMANO_POBLACION = 400
GENERACIONES = 500
TASA_CRUCE = 0.9
TASA_MUTACION = 0.01
TAM_TORNEO = 3
NUM_ELITES = 2
random.seed(SEMILLA)
np.random.seed(SEMILLA)

puntos = [
    {"nombre": "Abedul (Punto partida)", "latitud": 21.901101424443024, "longitud": -102.3040012533693},
    {"nombre": "The Home Depot", "latitud": 21.853087360458733, "longitud": -102.29388398860823},
    {"nombre": "H-E-B Santa Monica", "latitud": 21.84553768519487, "longitud": -102.32043895938828},
    {"nombre": "Walmart Express", "latitud": 21.862315711269652, "longitud": -102.33978794910628},
    {"nombre": "Centro Comercial Altaria", "latitud": 21.92561581878823, "longitud": -102.29019621691815},
    {"nombre": "Refaccionaria Autozone", "latitud": 21.917045413444306, "longitud": -102.25331493638625},
    {"nombre": "Costco Wholesale", "latitud": 21.91798172418564, "longitud": -102.28859563519714},
    {"nombre": "Cantia", "latitud": 21.873447784154173, "longitud": -102.33197264063998},
    {"nombre": "Abramex", "latitud": 21.87405059172399, "longitud": -102.37065828907802},
    {"nombre": "UTA", "latitud": 21.84108808925548, "longitud": -102.35400808743637},
    {"nombre": "Iron Black", "latitud": 21.8721699077842, "longitud": -102.31063108141613},
    {"nombre": "Estadio Victoria", "latitud": 21.88275225853007, "longitud": -102.27555416898866},
    {"nombre": "Catedral de Aguascalientes", "latitud": 21.88181461356139, "longitud": -102.29720658397149},
    {"nombre": "El carnes", "latitud": 21.87512307062271, "longitud": -102.3123454491299},
    {"nombre": "Bodega Aurrera", "latitud": 21.886240985779608, "longitud": -102.31162370185136},
    {"nombre": "El Parian", "latitud": 21.88300881635597, "longitud": -102.29504589927252}
]

def haversine (lat1, lon1, lat2, lon2):
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    R = 6371        
    dlat = (lat2 - lat1)
    dlon = (lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    d = 2 * R * np.arcsin(np.sqrt(a))

    return d

def construir_matriz(puntos):
    n = len(puntos)
    m = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            p1 = puntos[i]
            p2 = puntos[j]
            m[i][j] = haversine(p1["latitud"], p1["longitud"], p2["latitud"], p2["longitud"])    
    return m

n = len(puntos)
matriz = construir_matriz(puntos)

ruta_inicial = list(range(1, n))

def distancia_total(ruta):
    recorrido = [0] + ruta + [0]
    total_distancia = 0

    for k in range(len(recorrido) - 1):
        a = recorrido[k]
        b = recorrido[k + 1]
        total_distancia += matriz[a][b]
    return total_distancia

def crear_ruta_azar():
    ruta = list(range(1, n))
    random.shuffle(ruta)
    return ruta

def crear_poblacion(tam):
    poblacion = []
    for i in range(tam):
        ruta = crear_ruta_azar()
        poblacion.append(ruta)
    return poblacion

def seleccion_torneo(poblacion, distancias):
    candidatos = random.sample(range(len(poblacion)), TAM_TORNEO)
    
    mejor = candidatos[0]
    for i in candidatos:
        if distancias[i] < distancias[mejor]:
            mejor = i

    return poblacion[mejor].copy()

def cruzamiento_ox(padre1, padre2):
    a, b = sorted(random.sample(range(len(padre1)+1), 2))
    segmento = padre1[a:b]
    resto = []
    for gen in padre2:
        if gen not in segmento:
            resto.append(gen)
    hijo = resto[:a] + segmento + resto[a:]
    return hijo

def mutacion_swap(ruta):
    ruta = ruta.copy()
    if random.random() < TASA_MUTACION:
        c, d = random.sample(range(len(ruta)), 2)
        ruta[c], ruta [d] = ruta[d], ruta[c]
    return ruta

def nueva_generacion(poblacion, distancias):
    # 1. orden (el sorted con lambda)
    poblacion_ordenada = sorted(range(len(poblacion)), key=lambda i: distancias[i])
    # 2. elites
    elites = [poblacion[i].copy() for i in poblacion_ordenada[:NUM_ELITES]]
    # 3. nueva_poblacion = elites.copy()
    nueva_poblacion = elites.copy()
    # 4. el while completo, con el append
    while len(nueva_poblacion) < TAMANO_POBLACION:
        padre1 = seleccion_torneo(poblacion, distancias)
        padre2 = seleccion_torneo(poblacion, distancias)
        if random.random() < TASA_CRUCE:
            hijo = cruzamiento_ox(padre1, padre2)
        else:
            hijo = padre1.copy()
        
        hijo = mutacion_swap(hijo)
        nueva_poblacion.append(hijo)
    return nueva_poblacion

def correr_ga(semilla):
    random.seed(semilla)
    np.random.seed(semilla)
    
    pob = crear_poblacion(TAMANO_POBLACION)
    historial_mejor = []
    
    for gen in range(GENERACIONES):
        dist = [distancia_total(r) for r in pob]
        historial_mejor.append(min(dist))
        pob = nueva_generacion(pob, dist)
    
    dist_final = [distancia_total(r) for r in pob]
    return min(dist_final), historial_mejor, pob[dist_final.index(min(dist_final))]

def dibujar_ruta(ruta, titulo, archivo):
    lons = [puntos[i]["longitud"] for i in [0] + ruta + [0]]
    lats = [puntos[i]["latitud"] for i in [0] + ruta + [0]]
    plt.figure(figsize=(8, 8))
    plt.plot(lons, lats, "-o")
    plt.plot(lons[0], lats[0], "r*", markersize=18)

    for i in range(n):
        plt.text(puntos[i]["longitud"], puntos[i]["latitud"], str(i))

    plt.title(titulo)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True)
    plt.savefig(archivo, dpi=150)
    
def dibujar_convergencia(historial_mejor,titulo, archivo):
    plt.figure(figsize=(9, 5))
    plt.plot(historial_mejor, label="Mejor distancia")
    plt.xlabel("Generación")
    plt.ylabel("Distancia (km)")
    plt.title("Convergencia del algoritmo genético")
    plt.legend()
    plt.grid(True)
    plt.savefig(archivo, dpi=150)

    
while True:
    print("\n=== Optimizador de rutas ===")
    print("1. Ver puntos")
    print("2. Agregar punto")
    print("3. Eliminar punto")
    print("4. Calcular mejor ruta")
    print("5. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        for i, punto in enumerate(puntos):
            print(f"{i}: {punto['nombre']} (Lat: {punto['latitud']}, Lon: {punto['longitud']})")
    elif opcion == "2":
        nombre = input("Nombre del punto: ")
        try:
            latitud = float(input("Latitud: "))
            longitud = float(input("Longitud: "))
        except ValueError:
            print("Latitud y longitud deben ser numeros validos.")
            continue
        puntos.append({"nombre": nombre, "latitud": latitud, "longitud": longitud})
    elif opcion == "3":
        for i, punto in enumerate(puntos):
            print(f"{i}: {punto['nombre']} (Lat: {punto['latitud']}, Lon: {punto['longitud']})")
        try:
            indice = int(input("Indice del punto a eliminar: "))
            if indice == 0:
                print("No se puede eliminar el punto de partida.")
            elif 1 <= indice < len(puntos):
                puntos.pop(indice)
        except ValueError:
            print("El indice debe ser un numero válido.")
    elif opcion == "4":
        if len(puntos) < 2:
            print("Se necesitan al menos dos puntos para calcular una ruta.")
            continue
        n = len(puntos)
        matriz = construir_matriz(puntos)
        d_inicial = distancia_total(ruta_inicial)
        d_final, hist_opt, ruta_opt = correr_ga(SEMILLA)
        print(f"Mejor distancia encontrada: {d_final:.2f} km")
        print(" -> ".join ([puntos[i]['nombre'] for i in [0] + ruta_opt + [0]]))
        dibujar_ruta(ruta_opt, f"Mejor Ruta Encontrada (Distancia: {d_final:.2f} km)", "mejor_ruta.png")
        dibujar_ruta(ruta_inicial, f"Ruta inicial ({d_inicial:.2f} km)", "ruta_inicial_menu.png")
        dibujar_convergencia(hist_opt, "Convergencia del algoritmo genético", "convergencia_menu.png")
        plt.show()
    elif opcion == "5":
        print("Hasta luego!")
        break
    else:
        print("Opcion no valida")
        
