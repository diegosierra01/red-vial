#!/usr/bin/python
# -*- coding: utf-8 -*-
import cmath
import math
import random
from Tkinter import *


class Ventana:

    diametro = 20

    def __init__(self, tamano):
        self.tamano = tamano
        self.ventana = Tk()
        self.ventana.title('Vehiculos')
        # self.ventana.geometry("1000x500")
        self.ventana.geometry(str(tamano['ancho']) + "x" + str(tamano['alto']))
        # self.ventana.geometry(tamano['ancho'], tamano['alto'])
        self.canvas = Canvas(width=tamano['ancho'], height=tamano['alto'], bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<Button-1>", self.detectarClick)
        self.dibujos = []
        self.via = []

    def detectarClick(self, evento):
        #diametro = 20
        x = evento.x
        y = evento.y
        for dibujo in self.dibujos:
            if (x>dibujo['x'] and x<dibujo['x'] + self.diametro) and (y>dibujo['y'] and y<dibujo['y'] + self.diametro):
                self.via.append({'x':dibujo['x'], 'y':dibujo['y']})
        if len(self.via)==2:
            self.canvas.create_line(self.via[0]['x']+(self.diametro/2), self.via[0]['y']+(self.diametro/2), self.via[1]['x']+(self.diametro/2), self.via[1]['y']+(self.diametro/2), fill="black", width=2)
            self.via = []

        #dibujo = self.canvas.create_oval(x, y, x + diametro, y + diametro, fill='red')

    def dibujarNodos(self):
        cantidadDivisiones = 20
        distanciaDivisionesX = self.tamano['ancho'] / cantidadDivisiones
        distanciaDivisionesY = self.tamano['alto'] / cantidadDivisiones

        for y in range(self.diametro, self.tamano['alto'], distanciaDivisionesY):
            for x in range(self.diametro, self.tamano['ancho'], distanciaDivisionesX):
                dibujo = self.canvas.create_oval(x , y, x + self.diametro, y + self.diametro, fill='red')
                self.dibujos.append({'x':x,'y':y})
            pass

    def mostrar(self):
        self.ventana.mainloop()

anchoVentana = 1000
alturaVentana = 800
ventana = Ventana({'ancho': anchoVentana, 'alto': alturaVentana})
ventana.dibujarNodos()
ventana.mostrar()
