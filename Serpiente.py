import turtle
import time
import random

posponer = 0.1

#Marcador
score = 0
high_score = 0

#Ventana
ventana = turtle.Screen()
ventana.title('Serpiente')
ventana.bgcolor('green')
ventana.setup(width = 600, height = 600)
ventana.tracer(0)

#Cabeza serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape('square')
cabeza.color('orange')
cabeza.penup()
cabeza.goto(0,0)
cabeza.direction = 'stop'

#Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape('circle')
comida.color('black')
comida.penup()
comida.goto(100,100)

#Cuerpo serpiente
segmentos = []

#Texto de puntuaciones
texto = turtle.Turtle()
texto.speed(0)
texto.color('black')
texto.penup()
texto.hideturtle()
texto.goto(0,260)
texto.write('Score: 0      High Score: 0', align = 'center', font = ('Courier', 24, 'normal'))

#Funciones
def arriba():
    cabeza.direction = 'up'
def abajo():
    cabeza.direction = 'down'
def izquierda():
    cabeza.direction = 'left'
def derecha():
    cabeza.direction = 'right'

def movimiento():
    if cabeza.direction == 'up':
        y = cabeza.ycor()
        cabeza.sety(y + 20)
    if cabeza.direction == 'down':
        y = cabeza.ycor()
        cabeza.sety(y - 20)
    if cabeza.direction == 'left':
        x = cabeza.xcor()
        cabeza.setx(x - 20)
    if cabeza.direction == 'right':
        x = cabeza.xcor()
        cabeza.setx(x + 20)

#Teclado
ventana.listen()
ventana.onkeypress(arriba, 'Up')
ventana.onkeypress(abajo, 'Down')
ventana.onkeypress(izquierda, 'Left')
ventana.onkeypress(derecha, 'Right')

while True:
    ventana.update()

    #Colisiones bordes
    if cabeza.xcor() > 280 or cabeza.xcor() < -280 or cabeza.ycor() > 280 or cabeza.ycor() < -280:
        time.sleep(1)
        cabeza.goto(0,0)
        cabeza.direction = 'stop'

        #Borrar segmentos
        for segmento in segmentos:
            segmento.hideturtle()
        
        #Limpiar lista de segmentos
        segmentos.clear()

        #Resetear marcador
        score = 0
        texto.clear()
        texto.write('Score: {}      High Score: {}'.format(score, high_score), align = 'center', 
        font = ('Courier', 24, 'normal'))

    #Serpiente se come la comida
    if cabeza.distance(comida) < 20:
        x = random.randint(-280,280)
        y = random.randint(-280,280)
        comida.goto(x,y)

        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape('square')
        nuevo_segmento.color('orange')
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)

        #Aumentar marcador
        score += 1

        if score > high_score:
            high_score = score

        texto.clear()
        texto.write('Score: {}      High Score: {}'.format(score, high_score), align = 'center', 
        font = ('Courier', 24, 'normal'))

    #Mover el cuerpo de la serpiente
    total_seg = len(segmentos)
    for index in range(total_seg-1, 0, -1):
        x = segmentos[index-1].xcor()
        y = segmentos[index-1].ycor()
        segmentos[index].goto(x,y)

    if total_seg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x,y) 


    movimiento()

    #Colisiones con el cuerpo
    for segmento in segmentos:
        if segmento.distance(cabeza) < 20:
            time.sleep(1)
            cabeza.goto(0,0)
            cabeza.direction = 'stop'

            #Borrar segmentos
            for segmento in segmentos:
                segmento.hideturtle()

            segmentos.clear()

            #Resetear marcador
            score = 0
            texto.clear()
            texto.write('Score: {}      High Score: {}'.format(score, high_score), align = 'center', 
            font = ('Courier', 24, 'normal'))

    time.sleep(posponer)