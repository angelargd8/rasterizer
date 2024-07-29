from Mathlib import * 
import numpy as np
class Camara(object):
        def __init__(self):
            #en la camara no se necesita la escala
            self.translate = [0,0,0]
            self.rotate = [0,0,0]
            

        #recibir la matriz de vista
        def GetViewMatrix(self):
            traslateMat = TranslationMatrix(self.translate[0],
                                        self.translate[1],
                                        self.translate[2])
            rotateMat = RotationMatrixX(self.rotate[0],
                                    self.rotate[1],
                                    self.rotate[2])
            
            camMatrix =  traslateMat * rotateMat 
            
            #sacar la inversa de la matriz de camara
            
            #crear la funcion con numpy
            
            return np.linalg.inv(camMatrix)
    
              