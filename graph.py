#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
import random
from Tkinter import *


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
        self.canvas.bind("<Button-1>", self.dibujarOvalo)

    def dibujarOvalo(self, evento):
        diametro = 20
        x = evento.x
        y = evento.y
        dibujo = self.canvas.create_oval(x, y, x + diametro, y + diametro, fill='red')

    def dibujarNodos(self):
        radioNodo = 10
        cantidadDivisiones = 20
        distanciaDivisionesX = self.tamano['ancho'] / cantidadDivisiones
        distanciaDivisionesY = self.tamano['alto'] / cantidadDivisiones

        for y in range(radioNodo, self.tamano['alto'], distanciaDivisionesY):
            for x in range(radioNodo, self.tamano['ancho'], distanciaDivisionesX):
                dibujo = self.canvas.create_oval(x - radioNodo, y - radioNodo, x + radioNodo, y + radioNodo, fill='red')
            pass

    def mostrar(self):
        self.ventana.mainloop()

anchoVentana = 1000
alturaVentana = 800
ventana = Ventana({'ancho': anchoVentana, 'alto': alturaVentana})
ventana.dibujarNodos()
ventana.mostrar()
