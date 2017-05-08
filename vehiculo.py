#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
from Tkinter import *
import threading
import time
import numpy as np


class Simulador:

    anchoVentana = 1000
    alturaVentana = 600

    def __init__(self):
        self.ventana = Ventana({'ancho': self.anchoVentana, 'alto': self.alturaVentana})

    def generar(self, cantidadParticulas=50):
        self.vehiculos = []
        for i in xrange(0, cantidadParticulas):
            vehiculo = Vehiculo(self.ventana.via, self.vehiculos, self.anchoVentana)
            self.vehiculos.append(vehiculo)
            espera = np.random.uniform(0.1, 5)
            time.sleep(espera)
            pass

    # ....Hilo.....
    def moverParticulas(self):
        while True:
            self.ventana.dibujarVias()
            for x in xrange(0, len(self.vehiculos)):
                self.vehiculos[x].mover()
                pass
            self.ventana.dibujarOvalos(self.vehiculos)
            time.sleep(0.01)

    def mostrarVentana(self):
        self.ventana.mostrar()


class Vehiculo:

    dibujo = None  # Es la referencia del dibujo que pertenece a esta particula en el canvas
    distanciaPrudente = 5

    def __init__(self, via, vehiculos, limiteVentana):
        self.height = random.randrange(30, 80)
        self.width = 20
        self.limiteVentana = limiteVentana
        self.carril = random.randrange(1, 3)  # La vía tiene dos carriles
        self.via = via
        self.vehiculos = vehiculos
        self.setPosicion()
        self.velocidad = np.array([random.randrange(1, 4), 0])  # Velocidad en Y = 0
        self.velocidadOriginal = self.velocidad
        self.color = ("#%03x" % random.randint(0, 0xFFF))  # Aleatorio Hexadecimal
        # print self.coordenadas

    def setPosicion(self):
        if self.carril == 1:  # Carril superior
            y = self.via['limiteSuperior'] + ((self.via['divisionCarriles'] - self.via['limiteSuperior']) / 2)
        else:
            y = self.via['divisionCarriles'] + ((self.via['limiteInferior'] - self.via['divisionCarriles']) / 2)
        self.posicion = np.array([-self.width, y])

    def mover(self):

        if self.verificarAdelante() is False:  # hay un veliculo adelante
            if self.verificarLateral() is True:  # hay un vehiculo en el otro carril
                self.frenar()
            else:
                self.cambiarCarril()
        else:
            self.acelerar()

        # self.velocidad = self.velocidadOriginal
        self.posicion = self.posicion + self.velocidad

    def frenar(self):
        self.velocidad[0] = self.velocidad[0] / float(2)
        if self.velocidad[0] < 1:
            self.velocidad[0] = 1

    def acelerar(self):
        self.velocidad[0] = self.velocidad[0] + random.randrange(0, 1)

    def cambiarCarril(self):
        if self.carril == 2:  # Esta en el inferior hay que cambiar
            y = self.via['limiteSuperior'] + ((self.via['divisionCarriles'] - self.via['limiteSuperior']) / 2)
            self.carril = 1
        else:  # Esta en el superior hay que cambiar
            y = self.via['divisionCarriles'] + ((self.via['limiteInferior'] - self.via['divisionCarriles']) / 2)
            self.carril = 2
        self.posicion = np.array([self.posicion[0], y])

    def verificarAdelante(self):
        for vehiculo in self.vehiculos:
            if self.carril == vehiculo.carril:
                distancia = (vehiculo.posicion[0] - (self.posicion[0] + self.height))
                if distancia <= self.distanciaPrudente and distancia > -1 * self.height:
                    return False
        return True

    def verificarLateral(self):
        resultado = False
        for vehiculo in self.vehiculos:
            if self.carril != vehiculo.carril:
                x0 = self.posicion[0]
                y0 = vehiculo.posicion[1]
                R0 = self.height / float(2)

                x1 = vehiculo.posicion[0]
                y1 = vehiculo.posicion[1]
                R1 = vehiculo.height / float(2)

                # Delante
                if x0 <= x1 <= x0 + self.height + self.distanciaPrudente:
                    return True
                # Atras
                if x1 <= x0 <= x1 + vehiculo.height + self.distanciaPrudente:
                    return True

        return resultado

    def verificarColision(self, vehiculo):  # Retorna false si toca a otra particula

        x0 = self.posicion[0]
        y0 = self.posicion[1]
        R0 = self.height / float(2)

        x1 = vehiculo.posicion[0]
        y1 = vehiculo.posicion[1]
        R1 = vehiculo.height / float(2)
        return abs(R0 - R1) <= math.sqrt(pow((x0 - x1), 2) + pow((y0 - y1), 2)) <= (R0 + R1)

    # Para referenciar el dibujo en la pantalla
    def setDibujo(self, dibujo):
        self.dibujo = dibujo


class Ventana:
    def __init__(self, tamano):
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho'], height=tamano['alto'], bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        self.dibujarVias()

    def dibujarVias(self):
        anchoVia = 100
        # Se dibuja en la mitad
        limiteSuperior = (self.tamano['alto'] / 2) - (anchoVia / 2)
        limiteInferior = (self.tamano['alto'] / 2) + (anchoVia / 2)
        lineaDivisionCarril = limiteSuperior + ((limiteInferior - limiteSuperior) / 2)
        self.via = {'ancho': anchoVia, 'limiteSuperior': limiteSuperior, 'limiteInferior': limiteInferior, 'divisionCarriles': lineaDivisionCarril}

        # Dibuja via
        self.canvas.create_line(0, limiteSuperior, self.tamano['ancho'], limiteSuperior, width=2)
        self.canvas.create_line(0, limiteInferior, self.tamano['ancho'], limiteInferior, width=2)

        self.canvas.create_line(0, lineaDivisionCarril, self.tamano['ancho'], lineaDivisionCarril, width=1, fill='gray')

    def dibujarOvalos(self, particulas):
        for particula in particulas:
            x = particula.posicion[0]
            y = particula.posicion[1]

            self.canvas.delete(particula.dibujo)  # Borra el dibujo anterior

            # Dibuja el circulo
            dibujo = self.canvas.create_rectangle(x, y, x + particula.height, y + particula.width, fill=particula.color)
            particula.setDibujo(dibujo)

    def mostrar(self):
        self.ventana.mainloop()


simulador = Simulador()

hiloGenerador = threading.Thread(target=simulador.generar)
hiloGenerador.daemon = True
hiloGenerador.start()

# Hilo que mueve y dibuja
hilo = threading.Thread(target=simulador.moverParticulas)
hilo.daemon = True
hilo.start()

simulador.mostrarVentana()
