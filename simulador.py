#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import random
import time
import threading
from vehiculo import Vehiculo
from ventana import Ventana
from ventana import Via


class Simulador:

    anchoVentana = 1000
    alturaVentana = 700

    def __init__(self):
        # self.generarVias()
        self.ventana = Ventana({'ancho': self.anchoVentana, 'alto': self.alturaVentana})
        # self.ventana.crearDesdeGrafo()
        self.ventana.inicializar()

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
            vehiculo = Vehiculo(self.ventana.vias[random.randrange(0, len(self.ventana.vias))], self.vehiculos, self.anchoVentana, self.alturaVentana)
            self.vehiculos.append(vehiculo)
            espera = np.random.uniform(0.1, 5)
            time.sleep(espera)
            pass

    # ....Hilo.....
    def moverParticulas(self):
        while True:
            for x in xrange(0, len(self.vehiculos)):
                self.vehiculos[x].mover()
                if self.vehiculos[x].verificiarContencion() is False:
                    if self.vehiculos[x].sentido == 1:
                        if self.ventana.reaccionarSemaforo(self.vehiculos[x].via.fin, self.vehiculos[x].via) is True:
                            self.vehiculos[x].frenar(np.array([0, 0]))
                        else:
                            self.vehiculos[x].setVelocidad()
                    else:
                        if self.ventana.reaccionarSemaforo(self.vehiculos[x].via.inicio, self.vehiculos[x].via) is True:
                            self.vehiculos[x].frenar(np.array([0, 0]))
                        else:
                            self.vehiculos[x].setVelocidad()
                pass
            self.ventana.dibujarOvalos(self.vehiculos)
            time.sleep(0.01)

    def actualizarSemaforos(self):
        while True:
            self.ventana.actualizarSemaforos()
            time.sleep(30)

    def mostrarVentana(self):
        self.ventana.mostrar()


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

simulador.mostrarVentana()
