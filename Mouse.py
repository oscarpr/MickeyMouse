from PIL import Image, ImageDraw, ImageChops
import random
import numpy as np
import itertools
from  math import exp
import copy
import math, operator

pmax = 20
elipses = 55

def normal():
    normal = random.gauss(0,0.1)
    return normal

GEN_OUTPUT_STEP = 500
imagenOriginal = Image.open("mickey.png")

#Obtenemos el ancho de la imagen original
ancho = imagenOriginal.size[0]
alto = imagenOriginal.size[1]


#Nueva funcion para comparar las imagenes

def rmsd(img2):
    diff = ImageChops.difference(imagenOriginal,img2).histogram()
    return math.sqrt(reduce(operator.add,
    map(lambda h, i: h*(i**2), diff, range(256))) / (float(imagenOriginal.size[0]) * imagenOriginal.size[1]))


#Funcion para conventir una imagen a np.array
def np_INT16(image):
    l=list(image.getdata())
    arr=np.array([item for sublist in l for item in sublist], np.int16)
    return arr
    

#caja que contiene la elipse (4-tupla) (x0,y0,x1,y1) (x0y0-topLeft, x1y1 botRigth)
def bbox():
    yo = int(random.uniform(0,alto))
    y1 = int(random.uniform(0,alto))
    if (yo>y1):
        tem = y1
        y1 = yo
        yo = tem
    xo = int(random.uniform(0,ancho))
    x1 = int(random.uniform(0,ancho))
    if(xo>x1):
        tem = x1
        x1 = xo
        xo = tem
    caja=[xo,yo,x1,y1]
    return caja
    

# Se crea una imagen fondo blanco
global blankimage
blankimage = Image.new('L',[ancho,alto])
for x,y in itertools.product(*tuple(map(range,(ancho,alto)))):
    blankimage.putpixel((x,y),255)
blankimage = blankimage.getdata()

def gris():
    gris = int(random.uniform(0,255))
    return gris
    
#crea una imagen con elipses
def create_image(obra):
    global blankimage
    image = Image.new('L',[ancho,alto])
    image.putdata(blankimage)
    for i in range(0,elipses*5,5):
        draw = ImageDraw.Draw(image)
        draw.ellipse((obra[i],obra[i+1],obra[i+2],obra[i+3]),obra[i+4])
    return image 

#Funcion para perturbar el vector
def perturbado(obra):
    for i in range(50):
        pos = obra.index(random.choice(obra))
        muestra = obra[pos]
        muestra = muestra+pmax*normal()
        if muestra > ancho or muestra > alto or muestra > 255 or muestra < 0:
            if muestra % 4 == 0:
                if muestra > 255:
                    muestra = 255
                elif muestra < 0:
                    muestra = 0
            if muestra % 3 == 0:
                muestra = alto
            if muestra % 2 == 0:
                muestra = ancho
        else:                  
            obra[pos]=muestra     
    return obra    
    

obra=[0 for i in range(elipses*5)]
for i in range(0,elipses*5,5):
    obra[i]=bbox()[0]
    obra[i+1]=bbox()[1]
    obra[i+2]=bbox()[2]    
    obra[i+3]=bbox()[3]    
    obra[i+4]=gris() 


temperatura = 1000000.0
tc=0.99995

primeraImagen = create_image(obra)

costoInicial = rmsd(primeraImagen)
xPrima = 0
i = 0
while temperatura>0.0000000000001:
    print i
    solucionParcial = copy.deepcopy(obra)
    solucionParcial = perturbado(solucionParcial)
    imagenParcial = create_image(solucionParcial)
    xPrima = rmsd(imagenParcial)
    
    if xPrima<costoInicial:
        obra = solucionParcial
        costoInicial = xPrima
    else:
        u = random.uniform(0,1)
        dz = xPrima-costoInicial
        p = (exp(dz)/temperatura*(-1))
        if u < p:
            obra = solucionParcial
            costoInicial = xPrima
    if i % GEN_OUTPUT_STEP == 0:
        img = Image.new('L',(ancho,alto))
        img = create_image(obra)
        img.save(str(i)+".jpeg","JPEG")
    i = i+1    
    print xPrima
    print temperatura
    temperatura = temperatura*tc