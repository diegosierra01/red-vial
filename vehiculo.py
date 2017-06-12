#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
import time


class Vehiculo:

    dibujo = None  # Es la referencia del dibujo que pertenece a esta particula en el canvas

    def __init__(self, origen, destino, vehiculos, anchoVentana, altoVentana, vertices, ventana):
        self.height = random.randrange(30, 80)
        self.width = 20
        self.ventana = ventana
        # provisional para dar una ruta al vehiculo
        self.vertices = vertices
        self.recorrido = 1
        self.origen = origen
        self.actual = origen
        self.destino = destino
        self.anchoVentana = anchoVentana
        self.altoVentana = altoVentana
        self.vehiculos = vehiculos
        self.llegada = False
        self.tiempo = 0
        self.color = ("#%03x" % random.randint(0, 0xFFF))  # Aleatorio Hexadecimal
        # print self.coordenadas if actual es igual al inicio de la via o al fin de la via par adarle sentido

    def reaccionar(self):
        while(True):
            # si el vehiculo sigue en la via o si se encuentra en una interseccion
            if self.verificiarContencion(self.distanciaPrudente) is False:
                self.tiempo = self.tiempo + 1
                if self.ventana.reaccionarSemaforo(self.via.fin, self.via) is True:
                    self.frenar(np.array([0, 0]))
                    # aqui se agrega el algoritmo de busqueda por peso, congestio, etc...
                else:
                    if self.sentido == 1:
                        self.actual = self.via.fin
                    else:
                        self.actual = self.via.inicio
                    self.verficarLlegada()
            else:
                self.mover()
                self.tiempo = self.tiempo + 1
            time.sleep(0.01)

    def verficarLlegada(self):
        if self.actual != self.destino:
            if self.girar() is True:
                self.setVia(self.ventana.buscarVia(self.actual, self.vertices[self.recorrido]))
                self.recorrido = self.recorrido + 1
            self.mover()
        else:
            self.setVelocidad()
            self.mover()
            if self.llegada is False:
                print self.tiempo
                self.llegada = True

    def setVia(self, via):
        self.via = via
        # self.setSentido()
        if self.actual == self.via.inicio:
            self.sentido = 1
            self.carril = 1  # La vía tiene dos carriles
        elif self.actual == self.via.fin:
            self.sentido = 2
            self.carril = 2  # La vía tiene dos carriles
        self.setPosicion()
        self.setVelocidad()

    def setVelocidad(self):
        if self.via.posicion == 1:
            self.angle = 0
            self.velocidad = np.array([random.randrange(1, 4), 0])  # Velocidad en Y = 0
        else:
            self.angle = 90
            self.velocidad = np.array([0, random.randrange(1, 4)])  # Velocidad en X = 0
        self.velocidadOriginal = self.velocidad
        if self.via.posicion == 1:
            # depende de la velocidad - distancia de frenado
            self.distanciaPrudente = self.velocidad[0] * 5
        elif self.via.posicion == 2:
            self.distanciaPrudente = self.velocidad[1] * 5

    def girar(self):
        # se busca la interseccion del vertice actual
        interseccion = self.ventana.buscarInterseccion(self.actual)
        # si el vehiculo se sale de la interseccion pasa a otra via
        if self.verificiarContencion(0):
            # se comparan los dos vertices, el actual y el proximo
            # noroccidente->50 nororiente->130
            # suroriente->230 suroccidente->310
            self.velocidad = np.array([1, 1])
            if self.via.posicion == 1:
                if self.actual.position['y'] > self.vertices[self.recorrido].position['y']:
                    if self.sentido == 1:
                        # nororiente
                        self.angle = 130
                        self.velocidad[1] = -1
                    else:
                        # noroccidente
                        self.angle = 50
                elif self.actual.position['y'] < self.vertices[self.recorrido].position['y']:
                    if self.sentido == 1:
                        # suroriente
                        self.angle = 230
                    else:
                        # suroccidente
                        self.angle = 310
                        self.velocidad[1] = -1
            elif self.via.posicion == 2:
                if self.actual.position['x'] > self.vertices[self.recorrido].position['x']:
                    if self.sentido == 1:
                        # suroccidente
                        self.angle = 310
                        self.velocidad[0] = -1
                    else:
                        # noroccidente
                        self.angle = 50
                elif self.actual.position['x'] < self.vertices[self.recorrido].position['x']:
                    if self.sentido == 1:
                        # suroriente
                        self.angle = 230
                    else:
                        # nororiente
                        self.angle = 130
                        self.velocidad[0] = -1
        # si el vehiculo se sale de la interseccion pasa a otra via
        if self.sentido == 1 and (self.posicion[0] > interseccion.coordenadas['x1'] or self.posicion[1] > interseccion.coordenadas['y1']):
            return True
        if self.sentido == 2 and (self.posicion[0] < interseccion.coordenadas['x2'] or self.posicion[1] < interseccion.coordenadas['y2']):
            return True
        return False

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
                coord = self.via.limiteSuperior['x1']
            else:
                coord = self.via.divisionInicio['x']
            if self.sentido == 1:
                self.posicion = np.array([coord, self.via.inicio.position['y']])
            else:
                self.posicion = np.array([coord, self.via.fin.position['y']])

    def mover(self):
        adelante, velocidad = self.verificarAdelante()
        if adelante is False:  # hay un veliculo adelante
            if self.verificarLateral() is True:  # hay un vehiculo en el otro carril
                self.frenar(velocidad)
            else:
                self.cambiarCarril()
        else:
            # self.acelerar()
            if (self.via.posicion == 1 and self.velocidad[0] == 0) or (self.via.posicion == 2 and self.velocidad[1] == 0):
                self.setVelocidad()
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
            self.velocidad[0] = self.velocidad[0] + random.randrange(0, 2)
        else:
            self.velocidad[1] = self.velocidad[1] + random.randrange(0, 2)

    def verificiarContencion(self, distancia):
        if self.via.posicion == 1:
            if self.sentido == 1:
                if self.posicion[0] + self.height + distancia > self.via.fin.position['x']:
                    return False
            else:
                if self.posicion[0] - distancia < self.via.inicio.position['x']:
                    return False
        elif self.via.posicion == 2:
            if self.sentido == 1:
                if self.posicion[1] + self.height + distancia > self.via.fin.position['y']:
                    return False
            else:
                if self.posicion[1] - distancia < self.via.inicio.position['y']:
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
