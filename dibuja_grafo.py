#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dibuja_grafo.py
------------

Dibujar un grafo utilizando métodos de optimización

Estos métodos no son los que se utilizan en el dibujo de
gráfos por computadora pero da una idea de la utilidad de los métodos de
optimización en un problema divertido.

Para realizar este problema es necesario contar con el módulo Pillow
instalado (en Anaconda se instala por default. Si no se encuentr instalado,
desde la termnal se puede instalar utilizando

$pip install pillow

"""

__author__ = 'Escribe aquí tu nombre'

import blocales
import random
import itertools
import math
import time
import os
from PIL import Image, ImageDraw

from math import cos, sin

"""
Inicializa el valor de las k aleatoriamente para ver que combinaciones dan
costos decentes y las graficas se ven mejores.
"""
def inicializaKAleatorio():
    total = 10
    ks = [0,0,0,0,0]
    while total > 0:
        i = random.randrange(0, len(ks))
        ks[i] += 0.1
        total -= 0.1

    return ks

class problema_grafica_grafo(blocales.Problema):

    """
    Clase para el dibujo de un grafo simple no dirigido

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, en forma de
        lista (no conjunto, el orden es importante a la hora de
        graficar), y un conjunto (tambien en forma de lista) de pares
        ordenados de vertices, lo que forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a
        mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con pares de vertices, los cuales
                        definen las aristas.
        @param dimension_imagen: Entero con la dimension de la imagen
                                 en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema de define como:

           s = [s(1), s(2),..., s(2*len(vertices))],

        en donde s(i) \in {10, 11, ..., self.dim - 10} es la posición
        en x del nodo i/2 si i es par, o la posicion en y
        del nodo (i-1)/2 si i es non y(osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de
                 cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in
                     range(2 * len(self.vertices)))

    def vecino_aleatorio(self, estado, dmax=10):
        """
        Encuentra un vecino en forma aleatoria. En esta primera
        versión lo que hacemos es tomar un valor aleatorio, y
        sumarle o restarle x pixeles al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar
        como hacer un mejor vecino aleatorio y comparar las ventajas de
        hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.
        @param dispersion: Un flotante con el valor de dispersión para el
                           vertice seleccionado

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        """
        vecino = list(estado)

        i = random.randint(0, len(vecino) - 1)
        vecino[i] = max(10,
                        min(self.dim - 10,
                            vecino[i] + random.randint(-dmax,  dmax)))
        return tuple(vecino)
        """

        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Por supuesto que esta no es la mejor manera de generar vecinos.
        #
        # Propon una manera alternativa de vecino_aleatorio y muestra que
        # con tu propuesta se obtienen resultados mejores o en menor tiempo

        """
        Nueva idea: Tomar un vertice del grafo y moverlo aleatoriamente a otra
        posicion que este limitada por una circunferencia del radio de la
        dispersion. Ya que se mueve tanto en x como en y, es posible explorar
        el area de soluciones en menos pasos (o eso pienso).
        """
        vecino = list(estado)

        x = random.randint(0, len(vecino) - 1)
        y = x+1 if x % 2 == 0 else x-1
        if x > y:   #hace vecino[x] horizontal, vecino[y] vertical si no lo eran
            x,y = y,x
        theta = 2 * math.pi * random.random()
        magnitud  = dmax * random.random()
        dx = int(magnitud*cos(theta))
        dy = int(magnitud*sin(theta))
        vecino[x] = max(10, min(self.dim - 10, vecino[x] + dx))
        vecino[y] = max(10, min(self.dim - 10, vecino[y] + dy))

        return tuple(vecino)

    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado
        es la cantidad de veces que dos aristas se cruzan cuando se dibujan.

        Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.

        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes
        # (default solo cuanta el criterio 1)
        K1 = 0.5
        K2 = 3
        K3 = 2.0
        K4 = 0.5
        K5 = 4

        # Genera un diccionario con el estado y la posición
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic) +
                K5 * self.criterioPropio2(estado_dic))

        # Como podras ver en los resultados, el costo inicial
        # propuesto no hace figuras particularmente bonitas, y esto es
        # porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el
        # costo el angulo entre dos aristas conectadas al mismo
        # vertice, dandole un mayor costo si el angulo es muy pequeño
        # (positivo o negativo). Igualemtente se puede penalizar el
        # que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en trescuatro partes, una es el
        # numero de cruces (ya programada), otra la distancia entre
        # nodos (ya programada) y otro el angulo entre arista de cada
        # nodo (para programar). Por último, un criterio propio
        #
        # Al final, es necesario darle un peso lineal a cada uno de
        # los subcriterios.

    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo
        si se grafica como dice estado_dic

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de
        # aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los
            # vertices de una arista y los valores (x0B,y0B), (x0B,
            # y0B) para los vertices de la otra arista
            (x0A, y0A) = estado_dic[aristaA[0]]
            (xFA, yFA) = estado_dic[aristaA[1]]
            (x0B, y0B) = estado_dic[aristaB[0]]
            (xFB, yFB) = estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar
            # interseccion entre dos lineas cuidando primero de
            # asegurarse que las lineas no son paralelas (para evitar
            # la división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A)
            if den == 0:
                continue
            # Y entonces sacamos el largo del cruce, normalizado por
            # den. Esto significa que en 0 se encuentran en la primer
            # arista y en 1 en la última. Si los puntos de cruce de
            # ambas lineas se encuentran en valores entre 0 y 1,
            # significa que se cruzan
            puntoA = ((xFB - x0B) * (y0A - y0B) -
                      (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) -
                      (yFA - y0A) * (x0A - x0B)) / den
            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización
        proporcional a cada par de vertices que se encuentren menos
        lejos que min_dist. Si la distancia entre vertices es menor a
        min_dist, entonces calcula una penalización proporcional a
        esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.  @param min_dist: Mínima distancia
                           aceptable en pixeles entre dos vértices en
                           el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total

    def angulo_aristas(self, estado_dic):
        """
        A partir de una posicion "estado", devuelve una penalizacion
        proporcional a cada angulo entre aristas menor a pi/6 rad (30
        grados). Los angulos de pi/6 o mayores no llevan ninguna
        penalización, y la penalizacion crece conforme el angulo es
        menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Agrega el método que considere el angulo entre aristas de
        # cada vertice. Dale diferente peso a cada criterio hasta
        # lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores le diste a K1, K2 y K3 respectivamente?
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------
        #

        anguloMin = math.pi/6
        penalizacion = 0

        for (a1, a2) in itertools.combinations(self.aristas, 2):
            #si las aristas no comparten un vertice
            if not a1[0] in a2 and not a1[1] in a2:
                continue

            v1 = estado_dic[a1[0]] if a1[0] in a2 else estado_dic[a1[1]]
            v2 = estado_dic[a1[0]] if a1[0] not in a2 else estado_dic[a1[1]]
            v3 = estado_dic[a2[0]] if a2[0] not in a1 else estado_dic[a2[1]]

            angulo = calcularAngulo(v1, v2, v3)

            if angulo < anguloMin:
                penalizacion += 1 - angulo/anguloMin

        return penalizacion

    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea
        conveniente para que un grafo luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # ¿Crees que hubiera sido bueno incluir otro criterio? ¿Cual?
        #
        # Desarrolla un criterio propio y ajusta su importancia en el
        # costo total con K4 ¿Mejora el resultado? ¿En que mejora el
        # resultado final?
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------
        #
        """
        Este criterio trata de encajar los vertices de la grafica en una
        circunferencia porque creo que eso lo hace bonito.
        La circunferencia tiene centro en el centro de la ventana y el diametro
        es el largo o ancho (el que sea menor) de la ventana menos un marco de
        10 pixeles.
        """
        centro = (int(self.dim/2), int(self.dim/2))
        radio = int(self.dim/2) - 10
        penalizacion = 0

        for i in estado_dic:
            distancia = math.sqrt((estado_dic[i][0]-centro[0])**2 + \
                        (estado_dic[i][1]-centro[1])**2)
            diferencia = abs(distancia-radio)
            penalizacion += abs(distancia-radio)/radio

        return penalizacion

    """
    Criterio que revisa que haya el mismo numero de vertices en la parte
    izquierda que la parte derecha y en la parte superior e inferior de la
    grafica.
    """
    def criterioPropio2(self, estado_dic):
        verticesIzq = 0
        verticesInf = 0
        mitadHorizontal = self.dim/2
        mitadVertical = self.dim/2

        for i in estado_dic:
            if estado_dic[i][0] < mitadHorizontal:
                verticesIzq += 1
            if estado_dic[i][1] < mitadVertical:
                verticesInf += 1

        penalizacion1 = 1 - 2*abs(len(self.vertices)-verticesIzq)/len(self.vertices)
        penalizacion2 = 1 - 2*abs(len(self.vertices)-verticesInf)/len(self.vertices)

        return (penalizacion1+penalizacion2)/2

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma
        de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada
                 arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1])
                for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None, filename="prueba.gif"):
        """
        Dibuja el grafo utilizando el modulo pillow, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es la
        posición en x y y respectivamente de cada vertice. dim es la
        dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        # Imagen en blanco
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))
        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))

        imagen.save(filename)


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    dimension = 400

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para
    # ajustarlo.
    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    costo_inicial = grafo_sencillo.costo(estado_aleatorio)
    grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
    print("Costo del estado aleatorio: {}".format(costo_inicial))

    # Ahora vamos a encontrar donde deben de estar los puntos
    t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("\nUtilizando la calendarización por default")
    print("Costo de la solución encontrada: {}".format(costo_final))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizar una función de calendarización acorde con
    # el metodo en que se genera el vecino aleatorio.  Existen en la
    # literatura varias combinaciones. Busca en la literatura
    # diferentes métodos de calendarización (al menos uno más
    # diferente al que se encuentra programado) y ajusta los
    # parámetros para que obtenga la mejor solución posible en el
    # menor tiempo posible.
    #
    # Escribe aqui tus conclusiones
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

"""
Funcion que calcula el angulo de un arco dado 3 puntos.
Cada punto es una tupla de la fomar (posX, posY).

@param punto1: Es el punto que une los otros dos en el arco
@param punto2: Uno de los puntos del arco
@param punto3: Uno de los puntos del arco

@return El angulo en radianes del punto 2 al punto 3 unidos por el punto 1
"""
def calcularAngulo(punto1, punto2, punto3):
    #crea 2 vectores que van de p1 a p2 y de p1 a p3
    if punto1 == punto2 or punto1 == punto3 or punto2 == punto3:
        return 0
    vector12 = (punto1[0] - punto2[0], punto1[1] - punto2[1])
    vector13 = (punto1[0] - punto3[0], punto1[1] - punto3[1])

    prodPunto = vector12[0]*vector13[0] + vector12[1]*vector13[1]
    magnitud12 = math.sqrt(vector12[0]**2 + vector12[1]**2)
    magnitud13 = math.sqrt(vector13[0]**2 + vector13[1]**2)
    val = prodPunto/(magnitud12*magnitud13)
    #Arregla errores de punto flotante para que acos siempre tenga valor
    if val < -1:
        val = -1
    if val > 1:
        val = 1

    return math.acos(val)

"""
Funcion que asigna un nombre al archivo de prueba final asegurandose que no sobreescriba
uno pasado.

@return El nombre del archivo con extension gif y el numero de prueba que es.
"""
def asignaNombre():
    nombreFinal = "prueba_final"
    numero = 0
    extension = ".gif"
    nombre = nombreFinal+str(numero)+extension
    while os.path.isfile(nombre):
        numero += 1
        nombre = nombreFinal+str(numero)+extension

    return nombre, numero

"""
Dado un numero de [0,4] regresa un calendarizador para el problema de
dibujar grafos.

@param n: Indicador de que calendarizador se quiere

@return Calendarizador
"""
def calendarizarGrafo(problema, n):
    costos = [problema.costo(problema.estado_aleatorio())
              for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)

    if n == 1:
        #Tipo 1, exponencial multiplicativa. .8 <= a <= .9
        a = 0.85
        calendarizador = (T_ini*a**i for i in range(1, int(1e5)))

    elif n == 2:
        #Tipo 2, logaritmica multiplicativa. a > 1
        a = 2
        calendarizador = (T_ini / (1+a*math.log(1+i)) for i in range(1, int(1e5)))

    elif n == 3:
        #Tipo 3, lineal multiplicativa. a > 0
        a = 1
        calendarizador = (T_ini / (1 + a*i) for i in range(1, int(1e5)))
    
    elif n == 4:
        #Tipo 4, cuadratica multiplicativa. a > 0
        a = 1
        calendarizador = (T_ini / (1 + a*i**2) for i in range(1, int(1e5)))

    else:
        #Calendarizador por default
        calendarizador = None

    return calendarizador

"""
Es casi una copia de main
"""
def pruebaMain(kaleatorio = True):
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    dimension = 400

    #mejores k encontradas a prueba y error
    K1 = 1.6
    K2 = 2.1
    K3 = 2.1
    K4 = 2.1
    K5 = 2.2

    grafoCalendarizador = problema_grafica_grafo(vertices_sencillo,
                                                 aristas_sencillo,
                                                 dimension)

    def prueba(calendarizador = None):

        if kaleatorio:
            K1, K2, K3, K4, K5 = inicializaKAleatorio()

        grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                                aristas_sencillo,
                                                dimension)

        estado_aleatorio = grafo_sencillo.estado_aleatorio()
        costo_inicial = grafo_sencillo.costo(estado_aleatorio)
        grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
        print("Costo del estado aleatorio: {}".format(costo_inicial))


        # Ahora vamos a encontrar donde deben de estar los puntos
        t_inicial = time.time()
        solucion = blocales.temple_simulado(grafo_sencillo, calendarizador)
        t_final = time.time()
        costo_final = grafo_sencillo.costo(solucion)

        nombreFinal, numeroPrueba = asignaNombre()
        grafo_sencillo.dibuja_grafo(solucion, nombreFinal)
        print("\nPrueba numero: {}".format(numeroPrueba))
        if calendarizador is None:
            print("Utilizando la calendarización por default")
        else:
            print("Utilizando un calendarizador que no es default")

        print("Los valores de K son:")
        print("K1: {}\nK2: {}\nK3: {}\nK4: {}\nK5: {}".format(K1, K2, K3, K4, K5))

        print("Costo de la solución encontrada: {}".format(costo_final))
        print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))

    for i in range(2):
        print("\nCalendarizador default")
        prueba(calendarizarGrafo(grafoCalendarizador, 0))
        print("\nCalendarizador 1, exponencial multiplicativo")
        prueba(calendarizarGrafo(grafoCalendarizador, 1))
        print("\nCalendarizador 2, logaritmico multiplicativo")
        prueba(calendarizarGrafo(grafoCalendarizador, 2))
        print("\nCalendarizador 3, lineal multiplicativo")
        prueba(calendarizarGrafo(grafoCalendarizador, 3))
        print("\nCalendarizador 4, cuadratico multiplicativo")
        prueba(calendarizarGrafo(grafoCalendarizador, 4))

if __name__ == '__main__':
    #main()
    main()

"""
Conclusiones:
El temple simulado lo deje casi exacto como fue codificado. La unica diferencia es
que utilice otro calendarizador (con trampa). Hice pruebas con varios calendarizadores
simples y los que mejor costo daban eran el default y el que utilice al final, asi que
decidi usar el que no era default.

La manera en que encontre que pesos lineales deberia darle a los criterios fue hechando
a correr muchos diferentes, ver cuales daban costos mas bajos y volver a correrlos para
ver si era coincidencia. Asi llegue a los pesos finales y sorprendentemente son bastante
equilibrados. Personalmente creo que el criterio con el que los vertices deben estar con
el mismo numero en la parter izquierda, derecha, superior e inferior es la que hace mas
bonito el grafo, o que asi se puede parchar mas facilmente uno feo.

En general las graficas generadas no son hermosas pero tampoco son horriblemente feas. Son
en su mayoria aceptables pero de seguro utilizando otra combinacion de calendarizacion,
diferentes criterios y pesos lineales para criterios se podrian conseguir graficas mas
bonitas, pero una vez mas, creo que las que se generan con esta combinacion de parametros
son aceptables.
"""

