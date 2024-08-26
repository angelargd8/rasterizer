
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import  vertexShader, unlitShader, gouradShader, flatShader, toonShader, blueToonShader,glowShader, WaterShader, holographicShader, iridescentShader, LineShader, ToonShaderOP

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

width = 960 #
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.glLoadBackground("textures/fondo2.bmp")

rend.vertexShader = vertexShader
rend.fragmentShader = unlitShader


#modelo = Model("models/model.obj") #cargar el modelo
#modelo.LoadTexture("textures/model.bmp") #cargar la textura)


def Modelo(modelo, textura, translate0, translate1, translate2, scale0, scale1, scale2, rotate1, rotate2, rotate3, fragmentShader):
    modelo = Model(modelo) #cargar el modelo
    modelo.LoadTexture(textura) #cargar la textura
    modelo.vertexShader = vertexShader
    modelo.fragmentShader = fragmentShader
    modelo.translate[0] = translate0
    modelo.translate[1] = translate1
    modelo.translate[2] = translate2
    modelo.scale[0] = scale0
    modelo.scale[2] = scale1
    modelo.scale[1] = scale2
    modelo.rotate[0] =rotate1
    modelo.rotate[1] =rotate2
    modelo.rotate[2] =rotate3
    return modelo

#modelos

#Pez tilapia
pez = "models/Tilapia.obj"; pezTextura = "textures/Tilapia.bmp"
modeloPez  = Modelo(pez, pezTextura,8, -3, -11, 0.5, 0.5, 0.5,0,90,0, iridescentShader)
rend.models.append(modeloPez)

#barco 
barco = "models/barco.obj"; barcoTextura = "textures/barco.bmp"
modeloBarco  = Modelo(barco, barcoTextura,-9, 3, -15, 0.5, 0.5, 0.5,0,0,0, holographicShader)
rend.models.append(modeloBarco)

#tortuga
turtle = "models/pearlturtle.obj"; turtleTextura = "textures/pearlturtle.bmp"
modeloTurtle  = Modelo(turtle, turtleTextura,-8, -3, -15, 0.4, 0.4, 0.4,90,180,180, WaterShader) 
rend.models.append(modeloTurtle)

#sea diver
SeaDiver = "models/SeaDiver.obj"; SeaDiverTextura = "textures/SeaDiver.bmp"
modeloSeaDiver = Modelo(SeaDiver, SeaDiverTextura,4, -2, -12, 0.3, 0.3, 0.3,300,0,360, ToonShaderOP) 
rend.models.append(modeloSeaDiver)



isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE or event.key == pygame.K_s:
                rend.glGenerateFrameBuffer("output.bmp")
                
            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 10
                
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 10
                
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 10
                
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 10
                
            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
                
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES
                

    rend.glClear()
    rend.glClearBackground()
    
    rend.glRender()
   
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()