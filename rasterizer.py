
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import  vertexShader, unlitShader, gouradShader, flatShader, toonShader, blueToonShader,glowShader, WaterShader, holographicShader, iridescentShader, LineShader

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

# width = 960
# height = 960
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

# modelo1  = Modelo(0, 0, -10, 1.5, 1.5, 1.5,0,0,0, unlitShader)
# modelo2  = Modelo(3, 0, -10, 1.5, 1.5, 1.5,0,0,0, gouradShader)
# modelo3  = Modelo(0, 0, -8, 1.5, 1.5, 1.5,0,0,0, toonShader)
# modelo4  = Modelo(-3, 0, -10, 1.5, 1.5, 1.5,0,0,0, flatShader)
# modelo5  = Modelo(0, 0, -10, 1.5, 1.5, 1.5,0,0,0, blueToonShader)
# modelo6  = Modelo(0, 0, -10, 1.5, 1.5, 1.5,0,0,0, glowShader)
# modelo7  = Modelo(3, 0, -10, 1.5, 1.5, 1.5,0,0,0, WaterShader)
# modelo8  = Modelo(-3, 0, -10, 1.5, 1.5, 1.5,0,0,0, holographicShader)
# modelo9  = Modelo(0, 0, -8, 1.5, 1.5, 1.5,0,0,0, iridescentShader)
# modelo10  = Modelo(0, 0, -8, 1.5, 1.5, 1.5,0,0,0, LineShader)
# modelo22  = Modelo(0, 0, -5, 1.5, 1.5, 1.5,0,0,0, gouradShader)

# #Pez tilapia
# pez = "models/Tilapia.obj"; pezTextura = "textures/Tilapia.bmp"
# modeloPez  = Modelo(pez, pezTextura,8, -3, -11, 0.5, 0.5, 0.5,0,90,0, WaterShader)
# rend.models.append(modeloPez)

# #delfin
# dolphin = "models/dolphin.obj"; dolphinTextura = "textures/dolphin.bmp"
# modeloDolphin  = Modelo(dolphin, dolphinTextura,0, 0, -11, 0.5, 0.5, 0.5,0,90,0, unlitShader)
# rend.models.append(modeloDolphin)

#barco 
# barco = "models/barco.obj"; barcoTextura = "textures/barco.bmp"
# modeloBarco  = Modelo(barco, barcoTextura,-1, -3, -11, 0.5, 0.5, 0.5,0,0,0, WaterShader)
# rend.models.append(modeloBarco)

#tortuga
turtle = "models/turtle.obj"; turtleTextura = "textures/turtle.bmp"
modeloTurtle  = Modelo(turtle, turtleTextura,8, -3, -11, 0.5, 0.5, 0.5,0,90,0, unlitShader)
rend.models.append(modeloTurtle)

#sirena
sirena = "models/sirena.obj"; sirenaTextura = "textures/sirena.bmp"
modeloSirena  = Modelo(sirena, sirenaTextura,0, 0, -11, 0.5, 0.5, 0.5,0,90,0, unlitShader)
rend.models.append(modeloSirena)




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
                rend.camara.translate[0] += 10
                
            elif event.key == pygame.K_LEFT:
                rend.camara.translate[0] -= 10
                
            elif event.key == pygame.K_UP:
                rend.camara.translate[1] += 10
                
            elif event.key == pygame.K_DOWN:
                rend.camara.translate[1] -= 10
                
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