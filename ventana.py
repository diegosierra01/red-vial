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
        self.tamano = tamano
        self.crearDesdeGrafo()  # Crea las vías a partir del grafo

    def inicializar(self):
        self.ventanaPrincipal = Tk()
        self.ventanaPrincipal.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventanaPrincipal.geometry(str(self.tamano['ancho']) + "x" + str(self.tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvasPrincipal = Canvas(width=self.tamano['ancho'], height=self.tamano['alto'], bg='white')
        self.canvasPrincipal.pack(expand=YES, fill=BOTH)

    def dibujarVias(self):
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

            self.canvas.delete(particula.dibujo)  # Borra el dibujo anterior

            # Dibuja el circulo
            coord = x, y, x + particula.height, y + particula.width
            xy = [(coord[0], coord[1]), (coord[0], coord[3]), (coord[2], coord[3]), (coord[2], coord[1])]
            dibujo = self.canvas.create_polygon(xy, fill=particula.color)
            angle = cmath.exp(math.radians(particula.angle) * 1j)
            center = x + (particula.height / 2), y + (particula.width / 2)
            offset = complex(center[0], center[1])
            newxy = []
            for x, y in xy:
                v = angle * (complex(x, y) - offset) + offset
                newxy.append(v.real)
                newxy.append(v.imag)
            self.canvas.coords(dibujo, *newxy)
            particula.setDibujo(dibujo)

    def mostrar(self):
        self.ventanaPrincipal.mainloop()

    def crearDesdeGrafo(self):
        gui = Gui(self.tamano)
        gui.dibujarNodos()
        gui.mostrar()
        self.inicializar()
        self.crearVias(gui.aristas.aristas)
        self.crearIntersecciones(gui.vertices.vertices)

    def crearVias(self, aristas):
        for arista in aristas:
            via = Via(arista)
            self.canvasPrincipal.create_line(via.divisionInicio['x'], via.divisionInicio['y'], via.divisionFin['x'], via.divisionFin['y'], width=1, fill='red')
            self.canvasPrincipal.create_line(via.limiteSuperior['x1'], via.limiteSuperior['y1'], via.limiteSuperior['x2'], via.limiteSuperior['y2'], width=1, fill='blue')
            self.canvasPrincipal.create_line(via.limiteInferior['x1'], via.limiteInferior['y1'], via.limiteInferior['x2'], via.limiteInferior['y2'], width=1, fill='blue')
            self.vias.append(via)

    def crearIntersecciones(self, vertices):
        for vertice in vertices:
            adyacentes = []
            for via in vias:
                if vertice == via.arista.vertice1 or vertice == via.arista.vertice2:
                    adyacentes.append(via)
            interseccion = Interseccion(vertice, adyacentes)
            intersecciones.append(interseccion)


class Via:

    def __init__(self, x, y):
        # 1 -> horizontal 2 -> vertical
        self.posicion = random.randrange(1, 3)
        # 1 -> izq a der, arri a aba 2 -> der a izq, aba a arrib
        self.sentido1 = random.randrange(1, 3)
        self.sentido2 = random.randrange(1, 3)
        if self.posicion == 1:
            self.limiteSuperior = x
        else:
            self.limiteSuperior = y
        self.ancho = random.randrange(1, 6)
        try:
            self.width = {1: 75, 2: 100, 3: 125, 4: 150, 5: 175}[self.ancho]
        except KeyError:
            self.width = 100
        self.limiteInferior = self.limiteSuperior + self.width
        self.divisionCarriles = self.limiteSuperior + (self.width / 2)

        # De la clase Arista
    def __init__(self, lineaDivision):
        self.posicion = 3
        self.arista = lineaDivision
        self.divisionInicio = lineaDivision.vertice1.position
        self.divisionFin = lineaDivision.vertice2.position
        self.ancho = random.randrange(1, 6)
        self.limiteSuperior = {}
        self.limiteInferior = {}
        try:
            self.width = {1: 75, 2: 100, 3: 125, 4: 150, 5: 175}[self.ancho]
        except KeyError:
            self.width = 100
        if self.divisionInicio['x'] == self.divisionFin['x']:
            # Der a izq
            self.posicion = 1
            self.limiteSuperior['x1'] = self.divisionInicio['x'] + (self.width / 2)
            self.limiteSuperior['x2'] = self.divisionInicio['x'] + (self.width / 2)
            self.limiteSuperior['y1'] = self.divisionInicio['y']
            self.limiteSuperior['y2'] = self.divisionFin['y']
            self.limiteInferior['x1'] = self.divisionInicio['x'] - (self.width / 2)
            self.limiteInferior['x2'] = self.divisionInicio['x'] - (self.width / 2)
            self.limiteInferior['y1'] = self.divisionInicio['y']
            self.limiteInferior['y2'] = self.divisionFin['y']
        elif self.divisionInicio['y'] == self.divisionFin['y']:
            # Arr a aba
            self.posicion = 2
            self.limiteSuperior['y1'] = self.divisionInicio['y'] + (self.width / 2)
            self.limiteSuperior['y2'] = self.divisionInicio['y'] + (self.width / 2)
            self.limiteSuperior['x1'] = self.divisionInicio['x']
            self.limiteSuperior['x2'] = self.divisionFin['x']
            self.limiteInferior['y1'] = self.divisionInicio['y'] - (self.width / 2)
            self.limiteInferior['y2'] = self.divisionInicio['y'] - (self.width / 2)
            self.limiteInferior['x1'] = self.divisionInicio['x']
            self.limiteInferior['x2'] = self.divisionFin['x']
        else:
            # diagonal
            self.posicion = 3


class Interseccion:

    def __init__(self, vertice, vias):
        self.vertice = vertice
        for via in vias:
            self.linea.append(9)
            pass


anchoVentana = 800  # 1300
alturaVentana = 680
ventana = Ventana({'ancho': anchoVentana, 'alto': alturaVentana})
ventana.mostrar()
