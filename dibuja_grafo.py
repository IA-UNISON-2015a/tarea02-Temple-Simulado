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
instalado (en Anaconda se instala por default. Si no se encuentra instalado, 
desde la termnal se puede instalar utilizando
$pip install pillow
"""

__author__ = 'Giovanni Lopez Celaya'

import blocales
import random
import itertools
import math
import time
from PIL import Image, ImageDraw


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
                                 en pixeles (cuadrada por facilidad)
        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.
        Un estado para este problema de define como:
           s = [s(1), s(2),..., s(2*len(vertices))],
 
        en donde s(i) \dim {10, 11, ..., self.dim - 10} es la posición
        en x del nodo i/2 si i es par, o la posicion en y
        del nodo (i-1)/2 si i es non y(osease las parejas (x,y)).
        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de
                 cada vertice en la imagen.
        """
        #genera 
        return tuple(random.randint(10, self.dim - 10) for _ in
                     range(2 * len(self.vertices)))
                
                #FUNCION DE VECINO ALEATORIO ANTERIOR
    #def vecino_aleatorio(self, estado, dmax=10):
    #    """
    #    Encuentra un vecino en forma aleatoria. En esta primera
    #    versión lo que hacemos es tomar un valor aleatorio, y
    #    sumarle o restarle x pixeles al azar.
    #
    #    Este es un vecino aleatorio muy malo. Por lo que deberás buscar
    #    como hacer un mejor vecino aleatorio y comparar las ventajas de
    #    hacer un mejor vecino en el algoritmo de temple simulado.

    #   @param estado: Una tupla con el estado.
    #   @param dispersion: Un flotante con el valor de dispersión para el
    #                      vertice seleccionado
    
    #   @return: Una tupla con un estado vecino al estado de entrada.
    #
        
    #   vecino = list(estado)
    #   i = random.randint(0, len(vecino) - 1)   
    #    vecino[i] = max(10,min(self.dim - 10,
    #                        vecino[i] + random.randint(-dmax,  dmax)))
    #    print(vecino)
    #    return tuple(vecino)
    
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Por supuesto que esta no es la mejor manera de generar vecinos.
        #
        # Propon una manera alternativa de vecino_aleatorio y muestra que
        # con tu propuesta se obtienen resultados mejores o en menor tiempo
    def vecino_aleatorio(self, estado, dmax=5):
        """
        Esta forma en que se genera el vecino ayuda a que encuentre una solucion mas
        rápido
        """
        vecino = list(estado)
        #escojemos un vertice al azar
        i = random.randint(0, len(vecino) - 1)
        
        #volvemos a generar un vecino aleatorio en x,y
        if i%2 == 0:#significa que cayo en un vertice en la componente x el valor de i
            vecino[i]=random.randint(10, self.dim - 10)
            vecino[i+1]=random.randint(10, self.dim - 10)
        else:#sino entonces cayo en la componente y
            vecino[i]=random.randint(10, self.dim - 10)
            vecino[i-1]=random.randint(10, self.dim - 10)
            
        #Este metodo comentado no daba muy buenos resultados 
        #hacia que el grafo se moviera a las esquinas y se miraba feo
        #Mi plan era mover la componente x,y positiva o negativamente
        #aleatoriamente de un vertice escogido al azar
        """xD = math.ceil(random.uniform(-1, 1)*dmax)
        yD = math.ceil(random.uniform(-1, 1)*dmax)
        print("yD",yD,"xD",xD)
        #print(i)
        #print(len(vecino)-1)
        if i%2 == 0:
            #quiere decir que cayo un vertice en la componente y
            vecino[i]=((vecino[i]+xD) if(vecino[i]+xD < self.dim-30 and vecino[i]+xD > 30) else vecino[i])
            vecino[i+1]=(vecino[i]+yD if(vecino[i+1]+xD < self.dim-20 and vecino[i+1]+xD > 10) else vecino[i+1])
        else:
            #quiere decir que cayo un vertice en la componente y
            vecino[i]=(vecino[i]+yD if(vecino[i]+xD < self.dim-30 and vecino[i]+xD > 30) else vecino[i])
            vecino[i-1]=(vecino[i-1]+xD if(vecino[i-1]+xD < self.dim-30 and vecino[i-1]+xD > 30) else vecino[i-1])            
        """
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
        K1 = 10.0
        K2 = 3.0
        K3 = 7.0
        K4 = 3.0

        # Genera un diccionario con el estado y la posición
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

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
        total = 0
        #recorremos los vertices
        angulo=30
        for v in self.vertices:
            #juntamos las aristas si hay una incidencia del vertice en el que estamos
            aris = [ar for ar in self.aristas if v in ar]
            #generamos combinaciones de aristas de un vertice[v] 
            for (aristaA, aristaB) in itertools.combinations(aris, 2):
                (x0A, y0A) = estado_dic[aristaA[0]]
                (xFA, yFA) = estado_dic[aristaA[1]]
                (x0B, y0B) = estado_dic[aristaB[0]]
                (xFB, yFB) = estado_dic[aristaB[1]]
                try:
                    #print(estado_dic)
                    m1=(yFA-y0A)/(xFA-x0A)
                    m2=(yFB-y0B)/(xFB-x0B)
                    angulo=(math.degrees(abs(math.atan(((m2-m1)/(1+(m1*m2)))))))
                    #print(angulo)
                    if(angulo < 30):
                        total += 1-((angulo)/30)
                except ZeroDivisionError:
                    pass
                    """para que no salga el mensaje de division muchas veces en pantalla
                       lo comentamos
                    """
                    #print("Division sobre 0")
            
        # Agrega el método que considere el angulo entre aristas de
        # cada vertice. Dale diferente peso a cada criterio hasta
        # lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
        #K1=10 K2=3 y K3=7
        return total

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
        """
        Si, mi criterio es uno que mide las distancias de las aristas para 
        asi el grafo se vea mas o menos las aristas del mismo tamaño y asi no tenga 
        aristas ni muy largas ni muy cortas haciendo que se vea visualmente
        mas atractivo manteniendo un estandar en la longitud de aristas.
        """
        # Desarrolla un criterio propio y ajusta su importancia en el
        # costo total con K4 ¿Mejora el resultado? ¿En que mejora el
        # resultado final?
        total=0
        longitudArista=math.ceil(self.dim/3)
        
        for (arista) in self.aristas:
            (x0A, y0A) = estado_dic[arista[0]]
            (xFA, yFA) = estado_dic[arista[1]]
            d=math.sqrt((xFA-x0A)**2+((yFA-y0A)**2))
            if(d < longitudArista):
                total+= 1- d/longitudArista
            else:
                total+= 1- longitudArista/d
        
        return total

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma de diccionario
        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)
        @return: Un diccionario cuyas llaves son el nombre de cada
                 arista y su valor es una tupla (x, y)
        """
        #crea el diccionario (las listas los convierte a un diccionario)
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

def calendarizadorExp(K=100,delta=.001):
    calendarizador = (K*(math.exp(-delta*i)) for i in range(int(1e10)))
    
    return calendarizador

def main():
    """
    La función principal
    """

    # Vamos a definir un grafo sencillo
    vertices_completo= ['A','B','C','D','E']
    aristas_completo = [('A','B'),('A','C'),('A','D'),('A','E'),
                        ('B','C'),('B','D'),('B','E'),
                        ('C','D'),('C','E'),
                        ('D','E'),
                        
            ]
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
    
    #grafo_sencillo = problema_grafica_grafo(vertices_completo,
    #                                        aristas_completo,
    #                                        dimension)
    
    
    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    costo_inicial = grafo_sencillo.costo(estado_aleatorio)
    grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
    print("Costo del estado aleatorio: {}".format(costo_inicial))

    # Ahora vamos a encontrar donde deben de estar los puntos
    """t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)
    """
    t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo,calendarizadorExp())
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)
    
    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("\nUtilizando la calendarización exponencial")
    print("Costo de la solucion encontrada: {}".format(costo_final))
    print("Tiempo de ejecucion en segundos: {}".format(t_final - t_inicial))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    """
    Cambiar de calendarizador por defaul por uno exponencial, en promedio 
    tardaba al rededor de 15-20 minutos para poder terminar de 
    encontrar la solucion del grafo.
    Ahora con la calendarizacion exponencial no pasa de los 2 -3 minutos
    en promedio.
    Y al cambiar la funcion de vecino aleatorio se redujo a segundos!!
    """
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    """
    Es dificil de elegir el criterio mas importante, puesto que al 
    definir que es bonito o no puede influir en la desicion,
    en mi caso pienso que lo mas importante es el angulo del 
    vertice. Pero a su vez tambien influye la distancia de los 
    vertices es decir que no esten pegados, tambien entra el numero de cruces
    aunque si cumple con estas dos el numero de cruces en algunos frafos
    que estan totalmente conexos se ve bien aunque los tengan.
    Tambien es importante el modo en que se generan los vecinos 
    aleatorios ya que el tiempo y el costo de solicion se ve afectada.
    """
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizar una función de calendarización acorde con
    # el metodo en que se genera el vecino aleatorio.  Existen en la
    # literatura varias combinaciones. Busca en la literatura
    # diferentes métodos de calendarización (al menos uno más
    # diferente al que se encuentra programado) y ajusta los
    # parámetros para que obtenga la mejor solución posible en el
    # menor tiempo posible.
    #


if __name__ == '__main__':
    main()