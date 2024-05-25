import pygame
import pygame.sprite
from random import *
pygame.init()

pygame.font.init()
font1 = pygame.font.Font("Toon Around df.otf", 30)
font3 = pygame.font.Font("Toon Around df.otf", 80)
font2 = pygame.font.Font("BaiJamjuree-Bold.ttf", 100)
font4 = pygame.font.Font("BaiJamjuree-Bold.ttf", 25)
font5 = pygame.font.Font("BaiJamjuree-Bold.ttf", 22)

win_x = 800
win_y = 600
# imagenes
img_ship = "shooter.png"
img_bullet = "rock.png"
img_trash1 = "trash_0.png"
img_trash2 = "trash_1.png"
img_trash3 = "trash_2.png"
img_trash4 = "trash_3.png"
img_power = "superpower.png"

#vidas para el modo hardcore
hardcore = False
life = 10

rules = pygame.transform.scale(pygame.image.load("Bulletshot2.png"), (554, 452))
warn = pygame.transform.scale(pygame.image.load("warn.png"), (550, 355))

no_clicked_conf = pygame.transform.scale(pygame.image.load("config 1.png"), (62,62))
menu_1 = pygame.transform.scale(pygame.image.load("menu_1.png"), (62,68))


scoreboard2 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68)) #para el speedrun
scoreboard3 = pygame.transform.scale(pygame.image.load("scoreboard 2.png"), (134, 68))# para salir del juego
scoreboard4 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68)) # para el hardcore
scoreboard5 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68)) # para ir al menu principal

background = pygame.transform.scale(pygame.image.load("bg.png"), (800,600))
scoreboard = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68))
line = pygame.transform.scale(pygame.image.load("line.png"), (800, 7))
key = pygame.transform.scale(pygame.image.load("key.png"), (360, 195))

#music
pygame.mixer.init()
songs = ["sleigh_ride.ogg", "here_comes_santa.ogg", "merry_christmas.ogg"]
current_song_index = 0

# Reproducir la primera canción en bucle
pygame.mixer.music.load(songs[current_song_index])
pygame.mixer.music.play()

#sfx
audio1 = pygame.mixer.Sound("chop.wav")

explosion = pygame.mixer.Sound("explosion.ogg")

global deleted_trash
deleted_trash = 0

max_score = 100
score = 0
misses = 0


pygame.display.set_caption("Bulletshot")
window = pygame.display.set_mode((win_x, win_y))
# Cargar la imagen como un objeto Surface
icono = pygame.image.load("kp.ico")
# Establecer el icono de la ventana
pygame.display.set_icon(icono)


class GameSprite(pygame.sprite.Sprite):
 #constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Se llama al constructor de la clase (Sprite):
        pygame.sprite.Sprite.__init__(self)


       #cada objeto debe almacenar la propiedad image
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed


       #cada objeto debe tener la propiedad rect que representa el rectángulo en el que se encuentra
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #método de dibujo del personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#clase del jugador principal
class Player(GameSprite):
   #método para controlar el objeto con las flechas del teclado
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_x - 80:
            self.rect.x += self.speed
 #método para “disparar” (usar la posición del jugador para crear una bala)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 15, self.rect.top, 29, 25, -4)
        bullets.add(bullet)

#clase para el adorno de la piedra
class Rock(GameSprite):
   #método para controlar el objeto con las flechas del teclado
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 25:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_x - 60:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.collisions = 0  # Contador de colisiones

    def update(self):
        global misses
        self.rect.y += self.speed
        #si llega a la parte de arriba se elimina la bala
        if self.rect.y < 0:
            global life
            misses += 1
            self.kill()

            #para que no muestre -1 en la pantalla
            life -= 1
            if life <= 0:
                life = 0

class RandomObject(GameSprite):
    def __init__(self, random_image, size_x, size_y):
        # Crear un objeto aleatorio en una posición aleatoria en la parte superior de la pantalla
        random_x = randint(0, win_x - size_x)
        random_y = randint(0, 1)
        super().__init__(random_image, random_x, random_y, size_x, size_y, 1)
    def update(self):
        global misses
        # Mover el objeto aleatorio hacia abajo
        self.rect.y += self.speed
        if self.rect.y > win_y - 170:
            # Si el objeto sale de la pantalla, reiniciar su posición en la parte superior
            self.rect.y = 0
            self.rect.x = randint(0, win_x - self.rect.width)
            misses += 1
            if hardcore:
                global life
                life -= 1
                if life <= 0:
                    life = 0

def update_game():
    pygame.display.update()

is_executing = True

random_images_list = [img_trash1, img_trash2, img_trash3, img_trash4]

random_objects = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(0,6):
    test4 = RandomObject(choice(random_images_list), 64, 64)
    random_objects.add(test4)


#font
score_font = font1.render("scoreboard:", True, (0,0,0))
misses_font = font1.render("misses:", True, (0,0,0))
speedrun_font = font4.render("speedrun", True, (0,0,0))
hardcore_font = font4.render("hardcore", True, (0,0,0))
exit_font = font4.render("exit game", True, (0,0,0))
main_menu_font = font5.render("main menu", True, (0,0,0))


# variable bullet para adorno de la bala
bullet = Rock(img_bullet, 390, win_y - 210, 29,25,2)

#deco
ship = Player(img_ship, 370, win_y - 200, 70, 67, 2)
clock = pygame.time.Clock()
run = True
finish = True
show_rules = False
rules_opened = False

show_warn = False
warn_opened = False

button_rect = pygame.Rect(730, 10, 61, 67) # boton para la configuracion
button_rect2 = pygame.Rect(230, 430, 134, 68) # boton para el speedrun
button_rect3 = pygame.Rect(230, 330, 134, 68) # boton para salir
button_rect4 = pygame.Rect(430, 430, 134, 68) # boton para modo hardcore
button_rect5 = pygame.Rect(430, 330, 134, 68) # boton para ir al menu principal
button_rect6 = pygame.Rect(668, 10, 62, 68) # boton para ir al menu principal en el juego

speedrun = False
stopwatch_started = False
stopwatch_time = 0
can_exit = False

while run:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                ship.fire()
                audio1.play()
            elif e.key == pygame.K_ESCAPE and show_rules == False and show_warn == False:
                run = False

            elif e.key == pygame.K_ESCAPE:
                show_rules = False
                show_warn = False

            elif e.key != pygame.QUIT:
                finish = False
    #animacion
        elif e.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            #configuracion
            if button_rect.collidepoint(pos):
                no_clicked_conf = pygame.transform.scale(pygame.image.load("config 2.png"), (62,62))           
            else:
                no_clicked_conf = pygame.transform.scale(pygame.image.load("config 1.png"), (62,62))
            # para ir al menu principal
            if button_rect6.collidepoint(pos):
                menu_1 = pygame.transform.scale(pygame.image.load("menu_2.png"), (62, 68))       
            else:
                menu_1 = pygame.transform.scale(pygame.image.load("menu_1.png"), (62, 68))
            #speedrun
            if button_rect2.collidepoint(pos):
                scoreboard2 = pygame.transform.scale(pygame.image.load("scoreboard 2.png"), (134, 68))          
            else:
                scoreboard2 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68))
            #para salir
            if button_rect3.collidepoint(pos):
                scoreboard3 = pygame.transform.scale(pygame.image.load("scoreboard 2.png"), (134, 68))       
            else:
                scoreboard3 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68))
            #modo hardcore
            if button_rect4.collidepoint(pos):
                scoreboard4 = pygame.transform.scale(pygame.image.load("scoreboard 2.png"), (134, 68))       
            else:
                scoreboard4 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68))
            #para ir al menu principal
            if button_rect5.collidepoint(pos):
                scoreboard5 = pygame.transform.scale(pygame.image.load("scoreboard 2.png"), (134, 68))       
            else:
                scoreboard5 = pygame.transform.scale(pygame.image.load("scoreboard.png"), (134, 68))


        elif e.type == pygame.MOUSEBUTTONDOWN:
            #las reglas
            if button_rect.collidepoint(pos):# and rules_opened == False:
                show_rules = True
                rules_opened = True
#            if button_rect.collidepoint(pos) and rules_opened == True:
#                show_rules = False
#                rules_opened = False

            #modo speedrun
            if button_rect2.collidepoint(pos) and finish == True:
                finish = False
                stopwatch_started = True
                stopwatch_time = 0  # Reiniciar el contador
                speedrun = True
            #para salir del juego
            if button_rect3.collidepoint(pos) and score >= max_score and can_exit == True:
                run = False
            #activar modo hardcore
            if button_rect4.collidepoint(pos) and finish == True:
                finish = False
                hardcore = True
                stopwatch_started = True
                stopwatch_time = 0  # Reiniciar el contador
            #ir al menu principal
            if button_rect5.collidepoint(pos) and can_exit == True:
                finish = True
                score = 0
                life = 10
                misses = 0
                misses_font = font1.render("misses:", True, (0,0,0))
                hardcore = False
                speedrun = False
                stopwatch_time = 0
                stopwatch_started = False
                can_exit = False
                
                for t in random_objects:
                    t.kill()
                for b in bullets:
                    b.kill()                
                for i in range(0,6):
                    test4 = RandomObject(choice(random_images_list), 64, 64)
                    random_objects.add(test4)
            #ir al menu principal dentro del juego
            if button_rect6.collidepoint(pos) and finish == False:
                finish = True
                score = 0
                life = 10
                misses = 0
                misses_font = font1.render("misses:", True, (0,0,0))
                hardcore = False
                speedrun = False
                stopwatch_time = 0
                stopwatch_started = False
                can_exit = False
                
                for t in random_objects:
                    t.kill()
                for b in bullets:
                    b.kill()                
                for i in range(0,6):
                    test4 = RandomObject(choice(random_images_list), 64, 64)
                    random_objects.add(test4)
            # clickear el boton para abrir y cerrar
            elif button_rect6.collidepoint(pos) and finish == True and warn_opened == False:
                show_warn = True
                warn_opened = True
            elif button_rect6.collidepoint(pos) and finish == True and warn_opened == True:
                show_warn = False
                warn_opened = False

            #al perder en el modo hardcore dar click y salir del juego
            if button_rect3.collidepoint(pos) and hardcore == True and can_exit == True:
                run = False
    if stopwatch_started:
        stopwatch_time += clock.get_time()  # Actualizar el tiempo transcurrido
    
#todo lo que se imprime en el menu
    if show_rules == True:
        show_warn = False
    elif show_warn == True:
        show_rules = False
    #detecta si la cancion ya termino
    if not pygame.mixer.music.get_busy():
        # Cambiar a la siguiente canción
        current_song_index = (current_song_index + 1) % len(songs)
        pygame.mixer.music.load(songs[current_song_index])
        pygame.mixer.music.play()

    score_num = font1.render(f"{score}", True, (0,0,0))
    misses_num = font1.render(f"{misses}", True, (0,0,0))
    start_font = font2.render("Bulletshot", True, (0,0,0))
    start_font2 = font2.render("Bulletshot", True, (103,213,253))
    window.blit(background, (0,0))
    window.blit(key,(215,320))
    window.blit(start_font2,(160,210))
    window.blit(start_font,(170,200))
    window.blit(scoreboard2,(230,430)) #speedrun
    window.blit(scoreboard4,(430,430)) #hardcore
    window.blit(speedrun_font, (243,443))
    window.blit(hardcore_font, (445,443))
    window.blit(menu_1,(668,8))
    window.blit(no_clicked_conf,(730,10))
    if show_rules:
        window.blit(rules, (130, 70))
    if show_warn:
        window.blit(warn,(130,100))

#todo lo que se imprime dentro del juego
    if not finish:
        #imprimir las vidas antes de que se imprima los misses
        if hardcore:
            misses_font = font1.render("life left:", True, (0,0,0))
            misses_num = font1.render(f"{life}", True, (0,0,0))                  
        window.blit(background, (0,0))
        window.blit(line, (0, win_y - 110))
        window.blit(scoreboard, (200,510))
        window.blit(score_font, (50,525))
        window.blit(scoreboard,(630,510))
        window.blit(misses_font, (530,525))
        window.blit(misses_num, (650, 525))
        window.blit(score_num, (220, 525))
        window.blit(no_clicked_conf,(730,10))
        window.blit(menu_1,(668,10))
        if hardcore:
            stopwatch_display = font1.render(f"Time: {stopwatch_time // 1000}.{stopwatch_time % 1000}", True, (0, 0, 0))
            window.blit(stopwatch_display, (50, 550))  # Ajusta la posición según sea necesario
            #si todas las vidas se perdieron
            if life <= 0:
                life = 0
                window.blit(scoreboard3,(230,330)) 
                window.blit(exit_font,(241,345))
                window.blit(scoreboard5,(420, 330))
                window.blit(main_menu_font,(430, 345))
                stopwatch_started = False  # Detener el contador
                stopwatch_display = font3.render(f"Best time: {stopwatch_time // 1000}.{stopwatch_time % 1000}", True, (0, 0, 0))
                window.blit(stopwatch_display, (160, 210))  # Ajusta la posición según sea necesario
                can_exit = True
                for t in random_objects:
                    t.kill()
        if speedrun:
            stopwatch_display = font1.render(f"Time: {stopwatch_time // 1000}.{stopwatch_time % 1000}", True, (0, 0, 0))
            stopwatch_text = font1.render("Mission: Destroy 100 enemies!", True, (0, 0, 0))
            window.blit(stopwatch_display, (50, 550))  # Ajusta la posición según sea necesario
            window.blit(stopwatch_text, (10, 10))  # Ajusta la posición según sea necesario

            if score >= max_score:
                can_exit = True
                stopwatch_started = False  # Detener el contador
                stopwatch_display = font3.render(f"Best time: {stopwatch_time // 1000}.{stopwatch_time % 1000}", True, (0, 0, 0))
                window.blit(stopwatch_display, (160, 210))  # Ajusta la posición según sea necesario
                for t in random_objects:
                    t.kill()
                window.blit(scoreboard3,(230,330)) 
                window.blit(exit_font,(241,345))
                window.blit(scoreboard5,(420, 330))
                window.blit(main_menu_font,(430, 345))      
        # Verificar colisiones con objetos aleatorios
        collides = pygame.sprite.groupcollide(bullets, random_objects, True, True)
        random_objects.update()
        bullets.update()

        random_objects.draw(window) 
        bullets.draw(window) # Dibujar los objetos aleatorios en la pantalla
        bullet.update()
        bullet.reset()

        ship.update()
        ship.reset()
        if show_rules:
            window.blit(rules, (130, 70))
        #por cada colision vuelve a aparecer en su misma posicion
        for c in collides:
            test4 = RandomObject(choice(random_images_list), 64, 64)
            random_objects.add(test4)
            score += 1
            explosion.play()

    if is_executing == True:
        update_game()
        clock.tick(120)
    else:
        pass
    