#matriz x matriz
#matriz x vector
#nomalizar un vector
#magnitud de un vector
#mtriz de identidad
#inversa de una matriz
import numpy as np
from math import pi, sin, cos
def TranslationMatrix(x,y,z): 
   return np.matrix([[1,0,0,x],
                    [0,1,0,y],
                    [0,0,1,z],
                    [0,0,0,1]]
                     )

def ScaleMatrix(x,y,z):
   return np.matrix([[x,0,0,0],
                    [0,y,0,0],
                    [0,0,z,0],
                    [0,0,0,1]])

def RotationMatrixX(pitch, yaw, roll):
   #convertir a radianes
   pitch *= pi/180
   yaw *= pi/180
   roll *= pi/180
   
   #creamos la matriz de toracion para eje
   pitchMat = np.matrix([[1,0,0,0],
                         [0,cos(pitch),-sin(pitch),0],
                            [0,sin(pitch),cos(pitch),0],
                            [0,0,0,1]])
   
   yawMat = np.matrix([[cos(yaw),0,sin(yaw),0],
                       [0,1,0,0],
                        [-sin(yaw),0,cos(yaw),0],
                        [0,0,0,1]])
   
   rollMat = np.matrix([[cos(roll),-sin(roll),0,0],
                        [sin(roll),cos(roll),0,0],
                            [0,0,1,0],
                            [0,0,0,1]])
   
   return pitchMat * yawMat * rollMat


#multiplicacion de matrices
def multiplicacionMatrices(a, b):
   pass


def multiplicacionMatrizVector(m, v):
   pass

def normalizarVector(v):
   pass

def magnitudVector(v):
   pass