#aqui se va a guardar la informacion 
from obj import Obj
from Mathlib import *
class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)
        self.vertices = objFile.vertices
        self.faces = objFile.faces
        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        self.scale  = [1,1,1]
        

    def GetModelMatrix(self):
        traslateMat = TranslationMatrix(self.translate[0],
                                        self.translate[1],
                                        self.translate[2])
        
        rotateMat = RotationMatrixX(self.rotate[0],
                                    self.rotate[1],
                                    self.rotate[2])
        
        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                                self.scale[2])
        
        #multiplicar los elementos
        res= multiplicacionMatrices(traslateMat, rotateMat)
        res= multiplicacionMatrices(res, scaleMat)
        return res #res de resultado xd

    