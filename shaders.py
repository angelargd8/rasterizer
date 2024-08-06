from Mathlib import *
import numpy as np
#import numpy
def vertexShader(vertex, **kwargs): #** = argumentos
    #se lleva a cabo por cada vertice
    #se va a encargar de transformar los vertices
    modelMatrix = kwargs["modelMatrix"]
    
    #recibir la matrix de vista
    viewMatrix= kwargs["viewMatrix"]
    projectionMatrix= kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    
    vt = [vertex[0], vertex[1], vertex[2], 1]
    #vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt
    temp1 = multiplicacionMatrices(viewportMatrix, projectionMatrix)
    temp2 = multiplicacionMatrices(viewMatrix, modelMatrix)
    temp3 = multiplicacionMatrices(temp1, temp2)
    vt = multiplicacionMatrizVector(temp3, vt)
    
    vt = [ (vt[0]/vt[3]) ,( vt[1]/vt[3]), (vt[2]/vt[3])]
        
    return vt

def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    
    #sabindoque las coordenadas de textira
    #estan en la cuarta y quinta posicion de cada 
    # indice de vertice, los obtenemos y guardmos
    
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]
    

    
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1

    #vts del pixel
    #P = uA + vB + wC
    vtP = [vtA[0]*u + vtB[0]*v + vtC[0]*w, 
           vtA[1]*u + vtB[1]*v + vtC[1]*w]
    
    if texture: 
        textColor = texture.getColor(vtP[0], vtP[1])
        r *= textColor[0]
        g *= textColor[1]
        b *= textColor[2]


    # # Para el proposito de mostrar las coordenadas de textura
    # # en accion, las usamos para el color
    # r *= u
    # g *= v
    # b *= w
        
    # Se regresa el color
    return [r,g,b]