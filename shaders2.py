import numpy as np
from Mathlib import *

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


def unlitShader(**kwargs):
	# Se lleva a cabo por cada pixel individual
	
	# Obtenemos la informacion requerida
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]

	# Sabiendo que las coordenadas de textura
	# estan en la 4ta y 5t posicion de cada 
	# indice del vertice, los obtenemos y
	# y guardamos

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	# Empezamos siempre con color blanco
	r = 1
	g = 1
	b = 1

	# P = uA + vB + wC
	vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
			u * vtA[1] + v * vtB[1] + w * vtC[1] ]
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]
		
	# Se regresa el color
	return [r,g,b]


def gouradShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	nA = [A[5], A[6], A[7]]
	nB = [B[5], B[6], B[7]]
	nC = [C[5], C[6], C[7]]
	
	normal = [u * nA[0] + v * nB[0] + w * nC[0],
			  u * nA[1] + v * nB[1] + w * nC[1],
		      u * nA[2] + v * nB[2] + w * nC[2] ]
	
	r = 1
	g = 1
	b = 1

	vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
			u * vtA[1] + v * vtB[1] + w * vtC[1] ]
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]
		
	# intensity = normal DOT -dirlight
	#intensity = np.dot(normal, -np.array(dirLight) )
	intensity = ProductoPunto(normal, -(dirLight))  
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	# Se regresa el color
	return [r,g,b]


def flatShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	nA = [A[5], A[6], A[7]]
	nB = [B[5], B[6], B[7]]
	nC = [C[5], C[6], C[7]]
	
	normal = [  (nA[0] + nB[0] + nC[0]) / 3,
				(nA[1] + nB[1] + nC[1]) / 3,
				(nA[2] + nB[2] + nC[2]) / 3]



	
	r = 1
	g = 1
	b = 1

	vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
			u * vtA[1] + v * vtB[1] + w * vtC[1] ]
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]
		
	# intensity = normal DOT -dirlight
	#intensity = np.dot(normal, -np.array(dirLight) )
	intensity = ProductoPunto(normal, -(dirLight))  
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	# Se regresa el color
	return [r,g,b]


def toonShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	nA = [A[5], A[6], A[7]]
	nB = [B[5], B[6], B[7]]
	nC = [C[5], C[6], C[7]]
	
	normal = [u * nA[0] + v * nB[0] + w * nC[0],
			  u * nA[1] + v * nB[1] + w * nC[1],
		      u * nA[2] + v * nB[2] + w * nC[2] ]
	
	r = 1
	g = 1
	b = 1

	vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
			u * vtA[1] + v * vtB[1] + w * vtC[1] ]
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]
		
	# intensity = normal DOT -dirlight
	#intensity = np.dot(normal, -np.array(dirLight) )
	intensity = ProductoPunto(normal, -(dirLight)) 
	intensity = max(0, intensity)
	
	if intensity < 0.33:
		intensity = 0.3
	elif intensity < 0.66:
		intensity = 0.6
	else:
		intensity = 1.0


	r *= intensity
	g *= intensity
	b *= intensity
	
	# Se regresa el color
	return [r,g,b]
