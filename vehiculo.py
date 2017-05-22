#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np


class Vehiculo:

    dibujo = None  # Es la referencia del dibujo que pertenece a esta particula en el canvas

    def __init__(self, via, vehiculos, anchoVentana, altoVentana):
        self.height = random.randrange(30, 80)
        self.width = 20
        self.anchoVentana = anchoVentana
        self.altoVentana = altoVentana
        self.carril = random.randrange(1, 3)  # La vía tiene dos carriles
        self.via = via
        self.vehiculos = vehiculos
        self.setSentido()
        self.setPosicion()
        self.setVelocidad()
        # depende de la velocidad
        self.distanciaPrudente = 10
        self.color = ("#%03x" % random.randint(0, 0xFFF))  # Aleatorio Hexadecimal
        # print self.coordenadas

    def setVelocidad(self):
        if self.via.posicion == 1:
            self.angle = 0
            self.velocidad = np.array([random.randrange(1, 4), 0])  # Velocidad en Y = 0
        else:
            self.angle = 90
            self.velocidad = np.array([0, random.randrange(1, 4)])  # Velocidad en X = 0
        self.velocidadOriginal = self.velocidad

    def setSentido(self):
        if self.carril == 1:
            self.sentido = self.via.sentido1
        else:
            self.sentido = self.via.sentido2

    def setPosicion(self):
        if self.via.posicion == 1:
            if self.carril == 1:  # Carril superior
                coord = self.via.limiteSuperior['y1'] + (self.via.width / 4) - (self.width / 2)
            else:
                coord = self.via.divisionInicio['y'] + (self.via.width / 4) - (self.width / 2)
            if self.sentido == 1:
                self.posicion = np.array([self.via.inicio.position['x'], coord])
            else:
                self.posicion = np.array([self.via.fin.position['x'], coord])
        else:
            if self.carril == 1:  # Carril superior
                coord = self.via.limiteSuperior['x1'] + (self.via.width / 4)
            else:
                coord = self.via.divisionInicio['x'] + (self.via.width / 4)
            if self.sentido == 1:
                self.posicion = np.array([coord - (self.height / 2), self.via.inicio.position['y']])
            else:
                self.posicion = np.array([coord - (self.height / 2), self.via.fin.position['y']])

    def mover(self):
        adelante, velocidad = self.verificarAdelante()
        if adelante is False:  # hay un veliculo adelante
            if self.verificarLateral() is True:  # hay un vehiculo en el otro carril
                self.frenar(velocidad)
            else:
                self.cambiarCarril()
        else:
            self.acelerar()
        if self.sentido == 1:
            self.posicion = self.posicion + self.velocidad
        else:
            self.posicion = self.posicion - self.velocidad

    def frenar(self, velocidad):
        if self.via.posicion == 1:
            self.velocidad[0] = self.velocidad[0] / float(2)
            if self.velocidad[0] < velocidad[0]:
                self.velocidad[0] = velocidad[0]
        else:
            self.velocidad[1] = self.velocidad[1] / float(2)
            if self.velocidad[1] < velocidad[1]:
                self.velocidad[1] = velocidad[1]

    def acelerar(self):
        if self.via.posicion == 1:
            self.velocidad[0] = self.velocidad[0] + random.randrange(0, 1)
        else:
            self.velocidad[1] = self.velocidad[1] + random.randrange(0, 1)

    def verificiarContencion(self):
        if self.via.posicion == 1:
            if self.sentido == 1:
                if self.posicion[0] > self.via.fin.position['x']:
                    return False
            else:
                if self.posicion[0] < self.via.inicio.position['x']:
                    return False
        elif self.via.posicion == 2:
            if self.sentido == 1:
                if self.posicion[1] > self.via.fin.position['y']:
                    return False
            else:
                if self.posicion[1] < self.via.inicio.position['y']:
                    return False
        return True

    def cambiarCarril(self):
        if self.via.posicion == 1:
            self.cambiarCarrilEsteOeste(self.via.limiteSuperior['y1'], self.via.divisionInicio['y'])
        else:
            self.cambiarCarrilNorteSur(self.via.limiteSuperior['x1'], self.via.divisionInicio['x'])

    def cambiarCarrilEsteOeste(self, limiteSuperior, divisionCarriles):
        if self.carril == 2:  # Esta en el inferior hay que cambiar
            if self.posicion[1] > limiteSuperior + (self.via.width / 4) - (self.width / 2):
                y = self.posicion[1] - 3
                if self.sentido == 1:
                    self.angle = 130
                else:
                    self.angle = 50
            else:
                self.carril = 1
                self.angle = 0
                y = self.posicion[1]
        else:  # Esta en el superior hay que cambiar
            if self.posicion[1] < divisionCarriles + (self.via.width / 4) - (self.width / 2):
                y = self.posicion[1] + 3
                if self.sentido == 1:
                    self.angle = 230
                else:
                    self.angle = 310
            else:
                self.carril = 2
                self.angle = 0
                y = self.posicion[1]
        self.posicion = np.array([self.posicion[0], y])

    def cambiarCarrilNorteSur(self, limiteSuperior, divisionCarriles):
        if self.carril == 2:  # Esta en el inferior hay que cambiar
            if self.posicion[0] > limiteSuperior + (self.via.width / 4) - (self.width / 2):
                x = self.posicion[0] - 3
                if self.sentido == 1:
                    self.angle = 130
                else:
                    self.angle = 50
            else:
                self.carril = 1
                self.angle = 90
                x = self.posicion[0]
        else:  # Esta en el superior hay que cambiarCarril
            if self.posicion[0] < divisionCarriles + (self.via.width / 4) - (self.width / 2) - (self.height / 2):
                x = self.posicion[0] + 3
                if self.sentido == 1:
                    self.angle = 230
                else:
                    self.angle = 310
            else:
                self.carril = 2
                self.angle = 90
                x = self.posicion[0]
        self.posicion = np.array([x, self.posicion[1]])

    def verificarAdelante(self):
        for vehiculo in self.vehiculos:
            if self.carril == vehiculo.carril and vehiculo.via == self.via:
                if self.sentido == 1:
                    if self.via.posicion == 1:
                        distancia = (vehiculo.posicion[0] - (self.posicion[0] + self.height))
                    else:
                        distancia = (vehiculo.posicion[1] - (self.posicion[1] + self.height))
                else:
                    if self.via.posicion == 1:
                        distancia = (self.posicion[0] - (vehiculo.posicion[0] + vehiculo.height))
                    else:
                        distancia = (self.posicion[1] - (vehiculo.posicion[1] + vehiculo.height))
                if distancia <= self.distanciaPrudente and distancia > -1 * self.height:
                    return False, vehiculo.velocidad
        return True, 0

    def verificarLateral(self):
        resultado = False
        for vehiculo in self.vehiculos:
            if self.carril != vehiculo.carril and vehiculo.via == self.via:
                x0 = self.posicion[0]
                y0 = self.posicion[1]
                R0 = self.height / float(2)

                x1 = vehiculo.posicion[0]
                y1 = vehiculo.posicion[1]
                R1 = vehiculo.height / float(2)

                if self.via.posicion == 1:
                    # Delante
                    if x0 <= x1 <= x0 + self.height + self.distanciaPrudente:
                        return True
                    # Atras
                    if x1 <= x0 <= x1 + vehiculo.height + self.distanciaPrudente:
                        return True
                else:
                    # Delante
                    if y0 <= y1 <= y0 + self.height + self.distanciaPrudente:
                        return True
                    # Atras
                    if y1 <= y0 <= y1 + vehiculo.height + self.distanciaPrudente:
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
