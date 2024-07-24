#matriz x matriz
#matriz x vector
#nomalizar un vector
#magnitud de un vector
#mtriz de identidad
#inversa de una matriz
import numpy as np
from math import e, pi, sin, cos


def TranslationMatrix(x,y,z): 
   return  [[1,0,0,x],
            [0,1,0,y],
            [0,0,1,z],
            [0,0,0,1]]
                     

def ScaleMatrix(x,y,z):
   return  [[x,0,0,0],
            [0,y,0,0],
            [0,0,z,0],
            [0,0,0,1]]
  

def RotationMatrixX(pitch, yaw, roll):
   #convertir a radianes
   pitch *= pi/180
   yaw *= pi/180
   roll *= pi/180
   
   #creamos la matriz de toracion para eje
   pitchMat = [[1,0,0,0],
                [0,cos(pitch),-sin(pitch),0],
                [0,sin(pitch),cos(pitch),0],
                [0,0,0,1]]
   
   yawMat = [[cos(yaw),0,sin(yaw),0],
                [0,1,0,0],
                [-sin(yaw),0,cos(yaw),0],
                [0,0,0,1]]
   
   rollMat = [[cos(roll),-sin(roll),0,0],
            [sin(roll),cos(roll),0,0],
                [0,0,1,0],
                [0,0,0,1]]
   
   resul = multiplicacionMatrices(pitchMat, yawMat)
   resul = multiplicacionMatrices(resul, rollMat)
   return resul 

#multiplicacion de matrices
def multiplicacionMatrices(a, b):
    try:   
        n_filas= len(a)
        n_columnas= len(b[0])
        n_comun = len(b) #n de columns de a y filas de b
   
        resultadoM = [[0 for x in range(n_columnas)] for y in range(n_filas)] #crea la matriz con 0's
        for i in range(n_filas):
            for j in range(n_columnas):
                for k in range(n_comun):
                    resultadoM[i][j] += a[i][k] * b[k][j]
        
        return resultadoM
    except Exception: 
        print("")

#multiplicacion de elementos en la misma posicion xd
def multiplicacionElementos(a, b):
    try:
        n = len(a)
        n2 = len(b)
        if n != n2:
            print("No se pueden multiplicar los elementos")
            return 0
        else:
            resultado = [[0 for x in range(len(a[0]))] for y in range(n)]
            for i in range(n):
                for j in range(len(a[0])):
                    resultado[i][j] = a[i][j] * b[i][j]                   
            return resultado
    except Exception: 
        print("no se puede multiplicar")
        

def multiplicacionMatrizVector(matriz, vector):
   try: 
       n_filas = len(matriz)
       n_columnas = len(matriz[0])
       if n_columnas != len(vector):
           print("No se pueden multiplicar")
           return 0
       else: 
            resultado = [0 for x in range(n_filas)]
            for i in range(n_filas):
                for j in range(len(vector)):
                        resultado[i] += matriz[i][j] * vector[j]
            return resultado
   except Exception: 
       print("no se puede multiplicar")
       return None

def normalizarVector(v):
   pass

def magnitudVector(v):
   pass

def tolist(array):
    try:
        return list(array)
    except Exception: 
        print("")