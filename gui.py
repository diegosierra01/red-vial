#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
import random
from Tkinter import *
import numpy as np
import imp
from aristas import *
from vertices import *


class Gui:

    diametro = 20
    nodos = []
    vertices = Vertices()
    aristas = Aristas()
    matriz = np.zeros((0, 0))

    def __init__(self, tamano):
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Grafo')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho'] - 100, height=tamano['alto'] - 100, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<Button-1>", self.detectarClick)
        # self.boton = Button(self.ventana, text="GUARDAR RED VIAL", width=tamano['ancho'], command=self.guardarRedVial, bg='green')
        self.boton = Button(self.ventana, text="GUARDAR RED VIAL", command=self.guardarRedVial, bg='green')
        self.boton.pack()
        self.dibujos = []

    def guardarRedVial(self):

        print '*********** NODOS ***************'
        nombre = 1
        for vertice in self.vertices:
            nombre = 1
            print vertice.nombre
            # vertices.agregar(Vertice(str(nombre), {'x': nodo['x'], 'y': nodo['y']}, 20))
        print '*********** VIAS ***************'
        for arista in self.aristas:
            nombre = 1
            # print 'arista:'+str(arista.vertice1.position)+' - '+str(arista.vertice2.position)+' - distancia: '+str(arista.distancia)
            print 'arista:' + str(arista.vertice1.nombre) + ' - ' + str(arista.vertice2.nombre) + ' - distancia: ' + str(arista.distancia)

        self.generarMatriz()

    def generarMatriz(self):
        self.matriz = np.zeros((len(self.vertices.vertices), len(self.vertices.vertices)))  # +1 de los nombres
        print self.matriz
        for arista in self.aristas.aristas:
            # Como es no dirigido, se agrega en ambos sentidos
            self.matriz[arista.vertice1.nombre][arista.vertice2.nombre] = 1
            self.matriz[arista.vertice2.nombre][arista.vertice1.nombre] = 1
        print self.matriz

    def detectarClick(self, evento):
        # diametro = 20
        x = evento.x
        y = evento.y
        for dibujo in self.dibujos:
            if (self.estaRangoCirculo(x, y, dibujo)):
                self.agregarVertice({'x': dibujo['x'], 'y': dibujo['y']})
                # self.agregarVertice({'x':evento.x, 'y':evento.y})
                break  # Para que ya no revise mas

        # if len(self.via)==2:
        #    self.canvas.create_line(self.via[0]['x']+(self.diametro/2), self.via[0]['y']+(self.diametro/2), self.via[1]['x']+(self.diametro/2), self.via[1]['y']+(self.diametro/2), fill="black", width=2)
        #    self.via = []

        # dibujo = self.canvas.create_oval(x, y, x + diametro, y + diametro, fill='red')

    def estaRangoCirculo(self, x, y, dibujo):
        return (x > dibujo['x'] and x < dibujo['x'] + self.diametro) and (y > dibujo['y'] and y < dibujo['y'] + self.diametro)

    def agregarVertice(self, coordenadas):
        position = {
            'x': coordenadas['x'] + (self.diametro / 2),
            'y': coordenadas['y'] + (self.diametro / 2),
        }

        # vertice = Vertice(str(len(self.vertices)+1),position)
        vertice = Vertice((len(self.vertices)), position)

        if self.vertices.existeVertice(vertice.position):  # Es un vetice ya agregado, se obtiene para no enviar uno nuevo con nombre diferente
            print "existe"
            vertice = self.vertices.obtenerConPosicion(vertice.position)

        aristaAgregada = self.agregarArista(vertice)
        if aristaAgregada:
            self.vertices.agregar(vertice)

    def agregarArista(self, vertice):
        if(len(self.vertices) > 0):
            # ultimoVertice = self.vertices.obtenerUltimoAgregado()
            ultimoVertice = self.vertices.ultimoAgregado
            # arista = Arista(vertice,ultimoVertice)
            arista = Arista(ultimoVertice, vertice)
            if not self.aristas.existeArista(arista) and ultimoVertice.position != vertice.position:
                self.aristas.agregar(arista)
                print arista.distancia
                self.canvas.create_line(arista.vertice1.position['x'], arista.vertice1.position['y'], arista.vertice2.position['x'], arista.vertice2.position['y'], fill="black", width=2)
                print 'Arista pintada'
                return True
            else:
                print 'Arista ya existe'
                return False
        else:
            return True

    def dibujarNodos(self):
        cantidadDivisiones = 8
        distanciaDivisionesX = self.tamano['ancho'] / cantidadDivisiones
        distanciaDivisionesY = self.tamano['alto'] / cantidadDivisiones

        for y in range(self.diametro, self.tamano['alto'], distanciaDivisionesY):
            for x in range(self.diametro, self.tamano['ancho'], distanciaDivisionesX):
                dibujo = self.canvas.create_oval(x, y, x + self.diametro, y + self.diametro, fill='red')
                self.dibujos.append({'x': x, 'y': y})
            pass

    def mostrar(self):
        self.ventana.mainloop()


# anchoVentana = 800 #1300
# alturaVentana = 680
# ventana = Gui({'ancho': anchoVentana, 'alto': alturaVentana})
# ventana.dibujarNodos()
# ventana.mostrar()
