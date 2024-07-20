def vertexShader(vertex, **kwargs): #** = argumentos
    #se lleva a cabo por cada vertice
    #se va a encargar de transformar los vertices
    modelMatrix = kwargs["modelMatrix"]
    
    vt = [vertex[0], vertex[1], vertex[2], 1]
    
    vt = modelMatrix @ vt

    vt = vt.tolist()[0]
    
    vt = [vt[0]/vt[3], vt[1]/vt[3], vt[2]/vt[3]]
    
    return vt