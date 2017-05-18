#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
import random
from Tkinter import *
import numpy as np


class Ventana:

    diametro = 20
    nodos = []

    def __init__(self, tamano):
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho']-100, height=tamano['alto']-100, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<Button-1>", self.detectarClick)
        self.dibujos = []
        self.vias = [] # Aristas
        b = Button(self.ventana, text="Crear vias", command=self.crearVias)
        b.pack()

    def crearVias(self):
        self.crearMatriz()


    def crearMatriz(self): # Crear la matriz de adyacencia
        self.matriz = np.zeros(len(self.nodos), len(self.nodos))
        print self.matriz
        return 1


    def detectarClick(self, evento):
        #diametro = 20
        x = evento.x
        y = evento.y
        for dibujo in self.dibujos:
            if (self.estaRangoCirculo(x,y,dibujo)):                
                self.agregarNodo({'x':dibujo['x'], 'y':dibujo['y']})
                #self.agregarNodo({'x':evento.x, 'y':evento.y})
                break # Para que ya no revise mas
        
        #if len(self.via)==2:
        #    self.canvas.create_line(self.via[0]['x']+(self.diametro/2), self.via[0]['y']+(self.diametro/2), self.via[1]['x']+(self.diametro/2), self.via[1]['y']+(self.diametro/2), fill="black", width=2)
        #    self.via = []

        #dibujo = self.canvas.create_oval(x, y, x + diametro, y + diametro, fill='red') 

    def estaRangoCirculo(self, x,y,dibujo):
        return (x>dibujo['x'] and x<dibujo['x'] + self.diametro) and (y>dibujo['y'] and y<dibujo['y'] + self.diametro)

    def agregarNodo(self, coordenadas):
        centroNodoX = coordenadas['x'] + (self.diametro/2)
        centroNodoY = coordenadas['y'] + (self.diametro/2)
        nodo = {
                'index' : len(self.nodos),
                'x' : coordenadas['x'], 
                'y' : coordenadas['y'], 
                'centro' : {'x' : centroNodoX, 'y' : centroNodoY}
                }
        aristaAgregada = self.agregarArista(nodo)
        if aristaAgregada:
            self.nodos.append(nodo)


    # El ultimo agregado es el nodo de inicio el nodo que llega por parametro,
    # es el nodo final
    def agregarArista(self, nodo):
        if(len(self.nodos) > 0):
            ultimoAgregado = self.nodos[len(self.nodos)-1] 
            
            # Arista
            xInicio = ultimoAgregado['centro']['x']
            yInicio = ultimoAgregado['centro']['y']
            xFin = nodo['centro']['x']
            yFin = nodo['centro']['y']
            arista = {
                    'indexInicio' : ultimoAgregado['index'],
                    'indexFin' : nodo['index'],
                    'x' : xInicio,
                    'y' : yInicio,
                    'x2' : xFin,
                    'y2' : yFin
            }
            existeArista = self.existeArista(arista)
            if not existeArista and ultimoAgregado['centro'] == nodo['centro']:
                self.vias.append(arista)
                # print self.vias
                self.canvas.create_line(xInicio, yInicio, xFin, yFin, fill="black", width=2)
                return True 
            else:
                print 'Arista ya existe'
                return False
        return True

    def existeArista(self,arista):
        aristaInvertida = {
                    'indexInicio' : arista['indexFin'],
                    'indexFin' : arista['indexInicio'],
                    'x' : arista['x2'],
                    'y' : arista['y2'],
                    'x2' : arista['x'],
                    'y2' : arista['y']
            }
        return self.estaRepetido(arista,aristaInvertida)

    def estaRepetido(self,arista,aristaInvertida):
        #return (arista in self.vias or aristaInvertida in self.vias)
        for via in self.vias:
            if ( (via['x'] == arista['x'] and via['y'] == arista['y']) or 
            (via['x'] == aristaInvertida['x'] and via['y'] == aristaInvertida['y'])):
                return True

    def dibujarNodos(self):
        cantidadDivisiones = 10
        distanciaDivisionesX = self.tamano['ancho'] / cantidadDivisiones
        distanciaDivisionesY = self.tamano['alto'] / cantidadDivisiones

        for y in range(self.diametro, self.tamano['alto'], distanciaDivisionesY):
            for x in range(self.diametro, self.tamano['ancho'], distanciaDivisionesX):
                dibujo = self.canvas.create_oval(x , y, x + self.diametro, y + self.diametro, fill='red')
                self.dibujos.append({'x':x,'y':y})
            pass
        

    def mostrar(self):
        self.ventana.mainloop()

anchoVentana = 800
alturaVentana = 700
ventana = Ventana({'ancho': anchoVentana, 'alto': alturaVentana})
ventana.dibujarNodos()
ventana.mostrar()
