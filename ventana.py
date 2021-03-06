#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
import random
from Tkinter import *

from gui import *


class Ventana:

    def __init__(self, tamano, vias):
        self.vias = []
        self.intersecciones = []
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho'], height=tamano['alto'], bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        self.dibujarVias()

    def __init__(self, tamano):
        self.vias = []
        self.intersecciones = []
        self.peatones = []
        self.tamano = tamano
        self.gui = Gui(self.tamano)
        self.gui.dibujarNodos()
        self.gui.mostrar()
        self.crearVias(self.gui.aristas.aristas)
        self.crearIntersecciones(self.gui.vertices.vertices)

    def inicializar(self):
        self.ventanaPrincipal = Tk()
        self.ventanaPrincipal.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventanaPrincipal.geometry(str(self.tamano['ancho']) + "x" + str(self.tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvasPrincipal = Canvas(width=self.tamano['ancho'], height=self.tamano['alto'], bg='white')
        self.canvasPrincipal.pack(expand=YES, fill=BOTH)
        self.dibujarVias()
        self.dibujarIntersecciones()

    def dibujarViasOld(self):
        for x in xrange(0, len(self.vias)):
            # Dibuja via
            if self.vias[x].posicion == 1:
                self.canvas.create_line(0, self.vias[x].limiteSuperior, self.tamano['ancho'], self.vias[x].limiteSuperior, width=2)
                self.canvas.create_line(0, self.vias[x].limiteInferior, self.tamano['ancho'], self.vias[x].limiteInferior, width=2)
                self.canvas.create_line(0, self.vias[x].divisionCarriles, self.tamano['ancho'], self.vias[x].divisionCarriles, width=1, fill='gray')
            else:
                self.canvas.create_line(self.vias[x].limiteSuperior, 0, self.vias[x].limiteSuperior, self.tamano['alto'], width=2)
                self.canvas.create_line(self.vias[x].limiteInferior, 0, self.vias[x].limiteInferior, self.tamano['alto'], width=2)
                self.canvas.create_line(self.vias[x].divisionCarriles, 0, self.vias[x].divisionCarriles, self.tamano['alto'], width=1, fill='gray')

    def dibujarOvalos(self, particulas):
        for particula in particulas:
            x = particula.posicion[0]
            y = particula.posicion[1]

            self.canvasPrincipal.delete(particula.dibujo)  # Borra el dibujo anterior

            # Dibuja el circulo
            coord = x, y, x + particula.height, y + particula.width
            xy = [(coord[0], coord[1]), (coord[0], coord[3]), (coord[2], coord[3]), (coord[2], coord[1])]
            dibujo = self.canvasPrincipal.create_polygon(xy, fill=particula.color)
            angle = cmath.exp(math.radians(particula.angle) * 1j)
            center = x + (particula.height / 2), y + (particula.width / 2)
            offset = complex(center[0], center[1])
            newxy = []
            for x, y in xy:
                v = angle * (complex(x, y) - offset) + offset
                newxy.append(v.real)
                newxy.append(v.imag)
            self.canvasPrincipal.coords(dibujo, *newxy)
            particula.setDibujo(dibujo)

    def mostrar(self):
        self.ventanaPrincipal.mainloop()

    def crearVias(self, aristas):
        for arista in aristas:
            via = Via(arista)
            self.vias.append(via)

    def dibujarVias(self):
        for via in self.vias:
            self.canvasPrincipal.create_line(via.divisionInicio['x'], via.divisionInicio['y'], via.divisionFin['x'], via.divisionFin['y'], width=1, fill='red')
            self.canvasPrincipal.create_line(via.limiteSuperior['x1'], via.limiteSuperior['y1'], via.limiteSuperior['x2'], via.limiteSuperior['y2'], width=1, fill='blue')
            self.canvasPrincipal.create_line(via.limiteInferior['x1'], via.limiteInferior['y1'], via.limiteInferior['x2'], via.limiteInferior['y2'], width=1, fill='blue')

    def crearIntersecciones(self, vertices):
        for vertice in vertices:
            adyacentes = []
            for via in self.vias:
                if vertice == via.arista.vertice1 or vertice == via.arista.vertice2:
                    adyacentes.append(via)
            if len(adyacentes) > 1:
                interseccion = Interseccion(vertice, adyacentes)
                self.intersecciones.append(interseccion)

    def dibujarIntersecciones(self):
        for interseccion in self.intersecciones:
            if len(interseccion.coordenadas) > 3:
                self.canvasPrincipal.create_rectangle(interseccion.coordenadas['x1'], interseccion.coordenadas['y1'], interseccion.coordenadas['x2'], interseccion.coordenadas['y2'])
                for semaforo in interseccion.semaforos:
                    if semaforo.via.posicion == 1:
                        semaforo.setDibujo(self.canvasPrincipal.create_oval(semaforo.posicion['x'] - 20, semaforo.posicion['y'] - 10, semaforo.posicion['x'], semaforo.posicion['y'] + 10, fill=semaforo.color))
                    elif semaforo.via.posicion == 2:
                        semaforo.setDibujo(self.canvasPrincipal.create_oval(semaforo.posicion['x'] - 10, semaforo.posicion['y'] - 20, semaforo.posicion['x'] + 10, semaforo.posicion['y'], fill=semaforo.color))

    def actualizarSemaforos(self):
        for interseccion in self.intersecciones:
            if len(interseccion.coordenadas) > 3:
                for semaforo in interseccion.semaforos:
                    semaforo.estado = not semaforo.estado
                    semaforo.asignarColor()
                    self.canvasPrincipal.itemconfig(semaforo.dibujo, fill=semaforo.color)

    def reaccionarSemaforo(self, vertice, via):
        for interseccion in self.intersecciones:
            if interseccion.vertice == vertice:
                for semaforo in interseccion.semaforos:
                    if via == semaforo.via:
                        if semaforo.estado is False:
                            return True
        return False

    def buscarVia(self, vertice1, vertice2):
        resultado = None
        for via in self.vias:
            if (via.inicio == vertice1 and via.fin == vertice2) or (via.inicio == vertice2 and via.fin == vertice1):
                # print "encontrada"
                resultado = via
        if resultado is None:
            self.canvasPrincipal.create_oval(vertice1.position['x'], vertice1.position['y'], vertice1.position['x'] + 10, vertice1.position['y'] + 10)
            self.canvasPrincipal.create_oval(vertice2.position['x'], vertice2.position['y'], vertice2.position['x'] + 10, vertice2.position['y'] + 10)
        return resultado

    def buscarInterseccion(self, vertice):
        for interseccion in self.intersecciones:
            if interseccion.vertice == vertice:
                return interseccion
        return None

    def buscarVias(self, vertice, viaactual):
        resultado = []
        # print vertice
        # print ""
        for via in self.vias:
            if (via.inicio == vertice or via.fin == vertice) and via != viaactual:
                resultado.append(via)
        if len(resultado) < 1:
            resultado.append(viaactual)
        return resultado

    def seleccionarDestino(self, origen, viaactual):
        vias = self.buscarVias(origen, viaactual)
        index = random.randrange(0, len(vias))
        via = vias[index]
        return via

    def crearPeatones(self, xmax, xmin, ymax, ymin):
        peaton = Peaton(random.randrange(xmin - 50, xmax + 50), random.randrange(ymin - 50, ymax + 50))
        self.peatones.append(peaton)

    def moverPeatones(self):
        for peaton in self.peatones:
            peaton.mover()
            self.canvasPrincipal.delete(peaton.dibujo)  # Borra el dibujo anterior
            dibujo = self.canvasPrincipal.create_oval(peaton.x, peaton.y, peaton.x + 5, peaton.y + 5, fill='green')
            peaton.setDibujo(dibujo)


class Peaton:

    dibujo = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direccionx = random.randrange(1, 3)
        self.direcciony = random.randrange(1, 3)

    def mover(self):
        if self.direccionx == 1:
            self.x = self.x + random.randrange(0, 3)
        elif self.direccionx == 2:
            self.x = self.x - random.randrange(0, 3)
        if self.direcciony == 1:
            self.y = self.y + random.randrange(0, 3)
        elif self.direcciony == 2:
            self.y = self.y - random.randrange(0, 3)

    # Para referenciar el dibujo en la pantalla
    def setDibujo(self, dibujo):
        self.dibujo = dibujo


class Via:

    def __init__(self, lineaDivision):
        # self.sentido1 = random.randrange(1, 3)
        # self.sentido2 = random.randrange(1, 3)
        self.sentido1 = 1
        self.sentido2 = 2
        self.pendiente = 1
        # problema
        self.arista = lineaDivision
        self.divisionInicio = lineaDivision.vertice1.position
        self.divisionFin = lineaDivision.vertice2.position
        self.ancho = random.randrange(1, 6)
        self.limiteSuperior = {}
        self.limiteInferior = {}
        try:
            self.width = {1: 48, 2: 50, 3: 52, 4: 54, 5: 56}[self.ancho]
        except KeyError:
            self.width = 100

        if self.divisionInicio['y'] == self.divisionFin['y']:
            # Arr a aba
            self.posicion = 1
            self.limiteSuperior['y1'] = self.divisionInicio['y'] - (self.width / 2)
            self.limiteSuperior['y2'] = self.divisionInicio['y'] - (self.width / 2)
            self.limiteSuperior['x1'] = self.divisionInicio['x']
            self.limiteSuperior['x2'] = self.divisionFin['x']

            self.limiteInferior['y1'] = self.divisionInicio['y'] + (self.width / 2)
            self.limiteInferior['y2'] = self.divisionInicio['y'] + (self.width / 2)
            self.limiteInferior['x1'] = self.divisionInicio['x']
            self.limiteInferior['x2'] = self.divisionFin['x']

            if self.divisionFin['x'] > self.divisionInicio['x']:
                self.inicio = lineaDivision.vertice1
                self.fin = lineaDivision.vertice2
            elif self.divisionFin['x'] < self.divisionInicio['x']:
                self.inicio = lineaDivision.vertice2
                self.fin = lineaDivision.vertice1

        elif self.divisionInicio['x'] == self.divisionFin['x']:
            # Der a izq
            self.posicion = 2
            self.limiteSuperior['x1'] = self.divisionInicio['x'] - (self.width / 2)
            self.limiteSuperior['x2'] = self.divisionInicio['x'] - (self.width / 2)
            self.limiteSuperior['y1'] = self.divisionInicio['y']
            self.limiteSuperior['y2'] = self.divisionFin['y']
            self.limiteInferior['x1'] = self.divisionInicio['x'] + (self.width / 2)
            self.limiteInferior['x2'] = self.divisionInicio['x'] + (self.width / 2)
            self.limiteInferior['y1'] = self.divisionInicio['y']
            self.limiteInferior['y2'] = self.divisionFin['y']
            if self.divisionFin['y'] > self.divisionInicio['y']:
                self.inicio = lineaDivision.vertice1
                self.fin = lineaDivision.vertice2
            elif self.divisionFin['y'] < self.divisionInicio['y']:
                self.inicio = lineaDivision.vertice2
                self.fin = lineaDivision.vertice1
        else:
            # diagonal
            self.posicion = 3


class Interseccion:

    def __init__(self, vertice, vias):
        self.semaforos = []
        self.vertice = vertice
        self.vias = vias
        self.coordenadas = {}
        for via in vias:
            # Vertical
            if via.posicion == 1:
                self.coordenadas['y1'] = self.vertice.position['y'] + (via.width / 2)
                self.coordenadas['y2'] = self.vertice.position['y'] - (via.width / 2)
            elif via.posicion == 2:
                self.coordenadas['x1'] = self.vertice.position['x'] + (via.width / 2)
                self.coordenadas['x2'] = self.vertice.position['x'] - (via.width / 2)
        print self.coordenadas
        if len(self.coordenadas) > 3:
            self.crearSemaforos()

    def crearSemaforos(self):
        viascubiertas = []
        estado = True
        while len(viascubiertas) < (len(self.vias) - 1):
            numerorandom = random.randrange(0, len(self.vias) - 1)
            valido = True
            for numero in viascubiertas:
                if numero == numerorandom:
                    valido = False
            if valido is True:
                estado = not estado
                semaforo = Semaforo(self.vias[numerorandom], self.coordenadas, estado)
                self.semaforos.append(semaforo)
                viascubiertas.append(numerorandom)
            print str(len(viascubiertas))


class Semaforo:

    def __init__(self, via, coord, estado):
        # verde
        self.via = via
        self.posicion = {}
        self.estado = estado
        if via.posicion == 1:
            self.posicion['x'] = coord['x2']
            self.posicion['y'] = via.limiteSuperior['y1']
        elif via.posicion == 2:
            self.posicion['x'] = via.limiteSuperior['x1']
            self.posicion['y'] = coord['y2']
        self.asignarColor()

    def asignarColor(self):
        if self.estado is True:
            self.color = 'green'
        else:
            self.color = 'red'

    def setDibujo(self, dibujo):
        self.dibujo = dibujo
