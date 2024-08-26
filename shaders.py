import numpy as np
from Mathlib import *
from math import sin, cos, tan, pi

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
	modelMatrix = kwargs["modelMatrix"]

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	nA = [A[5], A[6], A[7]]
	nB = [B[5], B[6], B[7]]
	nC = [C[5], C[6], C[7]]
	
	normal = [u * nA[0] + v * nB[0] + w * nC[0],
			  u * nA[1] + v * nB[1] + w * nC[1],
		      u * nA[2] + v * nB[2] + w * nC[2],
			  0 ] #direccion , cuando es posicion es sin el ultimo valor
	
	normal = multiplicacionMatrizVector(modelMatrix, normal)
	normal = [normal[0], normal[1], normal[2]]
	#normalizarla
	#normal = normalizar(normal)
	

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
	#intensity = np.dot(normal, -np.array(dirLight) 
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
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
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
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
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo) 
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


def blueToonShader(**kwargs):
	
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
	#intensity = np.dot(normal, -np.array(dirLight) 
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	blue = [ 0.5, 0.5, 1]
	r *= blue[0]
	g *= blue[1]
	b *= blue[2]
	
	# Se regresa el color
	return [r,g,b]

def glowShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]
	camMatrix = kwargs["camMatrix"]
	modelMatrix = kwargs["modelMatrix"]

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
	#intensity = np.dot(normal, -np.array(dirLight) 
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	# GLOW
	yellowGlow = [1,1,0]
	
	camForward = [camMatrix[0][2], 
			     camMatrix[1][2],
                 camMatrix[2][2]]

	glowIntensity = 1 - ProductoPunto(normal, camForward)
	glowIntensity = max(0, glowIntensity)
	
	r += yellowGlow[0] * glowIntensity
	g += yellowGlow[1] * glowIntensity
	b += yellowGlow[2] * glowIntensity
	
	# Se regresa el color
	return [min(1,r),min(1,g),min(1,b)]


def WaterShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]
	camMatrix = kwargs["camMatrix"]

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
	
	#simular las ondas estaticamente porque no tenemos tiempo
	
	
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]

	#valores de la onda
	waveFrequency = 10.0
	waveAmplitude= 1.4
	
	wavePerturbationX = waveAmplitude * sin(waveFrequency * vtP[0])
	wavePerturbationY = waveAmplitude * cos(waveFrequency * vtP[1])
	normal = [normal[0] + wavePerturbationX, normal[1] + wavePerturbationY, normal[2]]
		
	#reflexion
	reflection = [0.5, 0.5, 0.7]
	# intensity = normal DOT -dirlight
	#intensity = np.dot(normal, -np.array(dirLight) 
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
	intensity = max(0, intensity)
	
	r = reflection[0] * intensity
	g = reflection[1] *intensity
	b = reflection[2] * intensity
	
	#refraccion 
	refraction = [0.2, 0.4, 0.5]
	camForward = [camMatrix[0][2], 
                 camMatrix[1][2],
                 camMatrix[2][2]]
	
	refactionIntensity = max(0, ProductoPunto(normal, camForward))

	r += refraction[0] * refactionIntensity
	g += refraction[1] * refactionIntensity
	b += refraction[2] * refactionIntensity
	
	# Se regresa el color
	return [min(1,r),min(1,g),min(1,b)]

def holographicShader(**kwargs):
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
	

	#valores de la onda
	lineFrequency = 150 #30 50
	lineIntensity= 0.4 #9
	
	lineEffect = lineIntensity * sin(lineFrequency * vtP[1])# +lineIntensity *cos(lineFrequency * vtP[0])
	
	
	r += lineEffect
	g += lineEffect
	b += lineEffect

	#fresnel 
	fresnelEffect =  max(0, ProductoPunto(normal, [0,0,1]))
	fresnelEffect = 1.0 - fresnelEffect
	fresnelEffect = min(1, fresnelEffect)

	r *= fresnelEffect
	g *= fresnelEffect
	b *= fresnelEffect
	
	blue = [ 0.2, 0.6, 1]
	r *= blue[0]
	g *= blue[1]
	b *= blue[2]
	
	
	# Se regresa el color
	return [min(1,r),min(1,g),min(1,b)]
	
def iridescentShader(**kwargs):
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
		
	#efecto iridiscente
	angle = ProductoPunto(normal, [0,0,1])
	angle = clip(angle, 0, 1)
	iridescence = sin(angle * pi *2) * 0.4 +0.5
		
	
	# r= iridescence* 0.5
	# g= iridescence 
	# b= 1.0 - iridescence 

	r= iridescence * 0.4
	g= 0.9 - iridescence 
	b= iridescence * 0.7
	
	# r= iridescence
	# g= 1.0 - iridescence 
	# b=  iridescence * 0.5
	
	
	# Se regresa el color
	return [min(1,r),min(1,g),min(1,b)]

def LineShader(**kwargs):
	
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
		

	height = u * A[1] + v * B[1] + w * C[1] #posicion en y
	
	value = sin(height) *3
	
	if value < -0.8:
		return None
	
		
	# Se regresa el color
	return [r,g,b]
	
#tiene los bordes negros, luz de ambiente y glow azul
def ToonShaderOP(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]
	camMatrix = kwargs["camMatrix"]
	modelMatrix = kwargs["modelMatrix"]

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
	#intensity = np.dot(normal, -np.array(dirLight) 
	dirLightNegativo = [-dirLight[0], -dirLight[1], -dirLight[2]]
	intensity = ProductoPunto(normal, dirLightNegativo)  
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	if intensity < 0.33:
		intensity = 0.3
	elif intensity < 0.66:
		intensity = 0.6
	else:
		intensity = 1.0

	#color del ambiente
	ambientLight = [ 0.4, 0.6, 1.0]
	
	r*=  ambientLight[0]
	g*=  ambientLight[1]
	b*=  ambientLight[2]


	# Se regresa el color
	edgeColor = [0,0,0]
	edgeMixFactor = 0.5 #para que no sea tan oscuro
	
	#detectar los bordes
	edgeThreshold = 0.1 
	if abs(intensity -0.5) < edgeThreshold:
		r = r * (1 - edgeMixFactor) + edgeColor[0] * edgeMixFactor
		g = g * (1 - edgeMixFactor) + edgeColor[1] * edgeMixFactor
		b = b * (1 - edgeMixFactor) + edgeColor[2] * edgeMixFactor
	
	# GLOW
	blueGlow = [0,0,0.1]
	
	camForward = [camMatrix[0][2], 
			     camMatrix[1][2],
                 camMatrix[2][2]]

	glowIntensity = 1 - ProductoPunto(normal, camForward)
	glowIntensity = max(0, glowIntensity)
	
	r += blueGlow[0] * glowIntensity
	g += blueGlow[1] * glowIntensity
	b += blueGlow[2] * glowIntensity


	# Se regresa el color
	#return [r,g,b]
	return [min(1,r),min(1,g),min(1,b)]