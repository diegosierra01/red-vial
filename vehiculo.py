#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np


class Vehiculo:

    dibujo = None  # Es la referencia del dibujo que pertenece a esta particula en el canvas
    angle = 0

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
        # depende de la velocidad
        self.distanciaPrudente = 10
        self.color = ("#%03x" % random.randint(0, 0xFFF))  # Aleatorio Hexadecimal
        # print self.coordenadas

    def setPosicion(self):
        if self.carril == 1:  # Carril superior
            y = self.via['limiteSuperior'] + ((self.via['divisionCarriles'] - self.via['limiteSuperior']) / 2)
        else:
            y = self.via['divisionCarriles'] + ((self.via['limiteInferior'] - self.via['divisionCarriles']) / 2)
        self.posicion = np.array([-self.height, y])

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
            if self.posicion[1] > self.via['limiteSuperior'] + ((self.via['divisionCarriles'] - self.via['limiteSuperior']) / 2):
                y = self.posicion[1] - 3
                self.angle = 130
            else:
                self.carril = 1
                self.angle = 0
                y = self.posicion[1]
        else:  # Esta en el superior hay que cambiar
            if self.posicion[1] < self.via['divisionCarriles'] + ((self.via['limiteInferior'] - self.via['divisionCarriles']) / 2):
                y = self.posicion[1] + 3
                self.angle = 230
            else:
                self.carril = 2
                self.angle = 0
                y = self.posicion[1]
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
                y0 = self.posicion[1]
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


