import pygame as py
import sys

py.init()


# Tamaño de la pantalla
w, h = 1000, 600
screen = py.display.set_mode((w, h))

# FPS
FPS = 60
reloj = py.time.Clock()

# Título e icono    
py.display.set_caption("Pruebas_juego")
icono = py.image.load("img/personaje/personaje_quieto.png")
py.display.set_icon(icono)

# Fondo de screen 
fondo = py.image.load("img/1-7e3b1004.png").convert()
x = 0

# Personaje quieto
quieto = py.image.load('img/personaje/personaje_quieto.png')

# Movimiento a la derecha
caminaDerecha = [py.image.load(f'img/personaje/personaje_derecha_{i}.png') for i in range(1, 8)]
derecha = False

# Movimiento a la izquierda
caminaIzquierda = [py.image.load(f'img/personaje/personaje_izquierda_{i}.png') for i in range(1, 8)]
izquierda = False

# Movimiento saltar
salta = [py.image.load(f'img/personaje/personaje_salta_{i}.png') for i in range(1, 9)]
salto = False

# Posición y velocidad
px = 50
poy = 425
velocidad = 8
cuentaPasos = 0

# Salto
cuentaSalto = 5
fuerza_salto = 0.3

# Vidas
vidas = 3
icono_vida = py.image.load("img/d04bd8b33083cb4.png")  # imagen de la vida
icono_vida = py.transform.scale(py.image.load("img/d04bd8b33083cb4.png"), (64, 64))

icono_vida_muerta = py.image.load("img/corazon_negro.png")  # imagen de la vida cuando mueres
icono_vida_muerta = py.transform.scale(py.image.load("img/corazon_negro.png"), (64, 64))

# Obstáculos
obstaculos = []
frecuencia_obstaculo = 40
contador_frames = 0
ancho_obstaculo = 40
alto_obstaculo = 40 
velocidad_obstaculo = 10
contador = 1

def recarga_screen():
    global cuentaPasos, x

    # Fondo en movimiento
    x_relativa = x % fondo.get_rect().width
    screen.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < w:
        screen.blit(fondo, (x_relativa, 0))

    # Velocidad de animación 
    velocidad_animacion = 6
    if cuentaPasos + 1 >= len(caminaDerecha) * velocidad_animacion:
        cuentaPasos = 0

    # Dibujar personaje
    if izquierda:
        frame = caminaIzquierda[cuentaPasos // velocidad_animacion]
        screen.blit(frame, (int(px), int(poy)))
        cuentaPasos += 1
        x += 1
    elif derecha:
        frame = caminaDerecha[cuentaPasos // velocidad_animacion]
        screen.blit(frame, (int(px), int(poy)))
        cuentaPasos += 1
        x -= 1
    elif salto:
        frame = salta[cuentaSalto // velocidad_animacion if cuentaSalto // velocidad_animacion < len(salta) else -1]
        screen.blit(frame, (int(px), int(poy)))
        cuentaPasos += 1
        x -= 1
    else:
        screen.blit(quieto, (int(px), int(poy)))

    # Dibujar obstáculos
    for obs in obstaculos:
        py.draw.rect(screen, (0, 0, 0), obs)

    # Dibujar vidas
    for i in range(3):
        if i < vidas:
            screen.blit(icono_vida, (10 + i * 40, 10))
        else:
            screen.blit(icono_vida_muerta, (10 + i * 40, 10))

    py.display.update()


running = True
while running:
    reloj.tick(FPS)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

    keys = py.key.get_pressed()

    # Movimiento derecha
    izquierda = False
    derecha = True
    if px < (w / 3) - velocidad - 100:
        px += velocidad
    else:
        x -= velocidad  # mover fondo

    # Salto
    if not salto:
        if keys[py.K_SPACE]:
            salto = True
            cuentaSalto = 10
            cuentaPasos = 0
    else:
        derecha = False
        if cuentaSalto >= -10:
            signo = 1 if cuentaSalto > 0 else -1
            poy -= (cuentaSalto ** 2) * fuerza_salto * signo
            cuentaSalto -= 1
        else:
            cuentaSalto = 10
            salto = False

    # Lógica de obstáculos
    contador_frames += 1
    
    if contador_frames % frecuencia_obstaculo == 0:
        nuevo_obstaculo = py.Rect(w, 480, ancho_obstaculo, alto_obstaculo)
        obstaculos.append(nuevo_obstaculo)

    for obs in obstaculos[:]:
        obs.x -= velocidad_obstaculo

        if obs.x + obs.width < 0:
            obstaculos.remove(obs)
            
    # Colisiones
    rect_personaje = py.Rect(px + 25, poy + 25, ancho_obstaculo, alto_obstaculo)  # Ajustás desplazamiento y tamaño real
    for obs in obstaculos[:]:
        if rect_personaje.colliderect(obs):
            vidas -= 1
            obstaculos.remove(obs)
            if vidas <= 0:
                print("GAME OVER")
                running = False

    recarga_screen()
    
    contador += 0.2
    
    if contador > 100 and contador < 150:
        frecuencia_obstaculo = 25
