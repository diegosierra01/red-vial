#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import random
import sys
import time
import threading
from vehiculo import Vehiculo
from ventana import Ventana
from ventana import Via


class Simulador:

    anchoVentana = 1000
    alturaVentana = 600
    tiempo = 0
    estado = 0

    def __init__(self):
        # self.generarVias()
        self.ventana = Ventana({'ancho': self.anchoVentana, 'alto': self.alturaVentana})
        # self.ventana.crearDesdeGrafo()
        self.ventana.inicializar()
        self.tiempomaximo = int(self.ventana.gui.tiempo) * 120
        self.definirArea()

    def generarVias(self):
        self.vias = []
        x = random.randrange(100, 300, 100)
        y = random.randrange(100, 300, 100)
        via = Via(x, y)
        self.vias.append(via)
        if via.posicion == 1:
            x = via.limiteInferior + random.randrange(100, 300, 100)
        else:
            y = via.limiteInferior + random.randrange(100, 300, 100)
        while(x < self.anchoVentana and y < self.alturaVentana):
            via = Via(x, y)
            self.vias.append(via)
            if via.posicion == 1:
                x = via.limiteInferior + random.randrange(100, 300, 100)
            else:
                y = via.limiteInferior + random.randrange(100, 300, 100)

    def generar(self, cantidadParticulas=50):
        self.vehiculos = []
        for i in xrange(0, cantidadParticulas):
            #origen = self.ventana.gui.vertices.vertices[0]

            origen = self.seleccionarOrigen()

            destino = self.ventana.gui.vertices.vertices[random.randrange(0, len(self.ventana.gui.vertices.vertices))]
            vehiculo = Vehiculo(self.estado, origen, destino, self.vehiculos, self.anchoVentana, self.alturaVentana, self.ventana.gui.vertices.vertices, self.ventana, self.ventana.peatones)
            # self.ventana.vias[random.randrange(0, len(self.ventana.vias))]
            vehiculo.setVia(self.ventana.seleccionarDestino(origen, None))
            vehiculo.recorrido = vehiculo.recorrido + 1
            hiloVerificador = threading.Thread(target=vehiculo.reaccionar)
            hiloVerificador.daemon = True
            hiloVerificador.start()
            self.vehiculos.append(vehiculo)
            espera = np.random.uniform(0.1, 5)
            if self.estado == 1:
                print "SIMULACION TERMINADA"
                sys.exit()
            time.sleep(espera)
            pass

       # if origen == via.inicio:
       #     return via.fin
       # else:
       #     return via.iniciio

    def seleccionarOrigen(self):
        origenes = self.ventana.gui.origenes
        cantidadOrigenes = len(origenes)
        index = random.randrange(0, cantidadOrigenes)
        return origenes[index]

    # ....Hilo.....
    def moverParticulas(self):
        while True:
            self.tiempo = self.tiempo + 1
            self.ventana.dibujarOvalos(self.vehiculos)
            if (self.tiempo / 100) > self.tiempomaximo:
                self.estado = 1
                print "SIMULACION TERMINADA"
                sys.exit()
            time.sleep(0.01)

    def actualizarSemaforos(self):
        while True:
            self.ventana.actualizarSemaforos()
            time.sleep(30)

    def mostrarVentana(self):
        self.ventana.mostrar()

    def definirArea(self):
        self.xmax = self.ventana.gui.vertices.vertices[0].position['x']
        self.xmin = self.ventana.gui.vertices.vertices[0].position['x']
        self.ymin = self.ventana.gui.vertices.vertices[0].position['y']
        self.ymax = self.ventana.gui.vertices.vertices[0].position['y']
        for vertice in self.ventana.gui.vertices.vertices:
            if vertice.position['x'] > self.xmax:
                self.xmax = vertice.position['x']
            elif vertice.position['x'] < self.xmin:
                self.xmin = vertice.position['x']
            elif vertice.position['y'] > self.ymax:
                self.ymax = vertice.position['y']
            elif vertice.position['y'] < self.ymin:
                self.ymin = vertice.position['y']

    def crearPersonas(self):
        while True:
            self.ventana.crearPeatones(self.xmax, self.xmin, self.ymax, self.ymin)
            time.sleep(5)

    def moverPersonas(self):
        while True:
            self.ventana.moverPeatones()
            time.sleep(0.1)


simulador = Simulador()

hiloGenerador = threading.Thread(target=simulador.generar)
hiloGenerador.daemon = True
hiloGenerador.start()

# Hilo que mueve y dibuja
hilo = threading.Thread(target=simulador.moverParticulas)
hilo.daemon = True
hilo.start()

hilosem = threading.Thread(target=simulador.actualizarSemaforos)
hilosem.daemon = True
hilosem.start()

hilopeatones = threading.Thread(target=simulador.crearPersonas)
hilopeatones.daemon = True
hilopeatones.start()

hilomovpeatones = threading.Thread(target=simulador.moverPersonas)
hilomovpeatones.daemon = True
hilomovpeatones.start()

simulador.mostrarVentana()
