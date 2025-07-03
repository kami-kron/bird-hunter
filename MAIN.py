import os
os.environ['SDL_VIDEO_WINDOW_POS'] ="500,200"
import pgzrun
from pgzero.actor import Actor
from records import read_record, ride_record
import random
from pygame import Rect
from time import sleep


# переменные
WIDTH = 900
HEIGHT = 700
TITLE = "ПТИЦEЛОВКА"

run = "menu"    #menu play pause game_over
score = 0
record = read_record()
print(record)

hero = Actor ("bird")
boom = Actor ("bomb",(15,15))
man = Actor ("super", (WIDTH/2, HEIGHT - 100))
plas = Actor ("forest")
over = Actor ("поражение",(WIDTH/2, HEIGHT/2))
grom = Actor ("molnia")
stop = False

width_b = 500
start_button = Rect((WIDTH/2 -width_b/2, 200), (width_b, 90))
exit_button = Rect ((WIDTH/2 -width_b/2, 400),(width_b, 90))

birds = []
bomba = []
groms = []
lives = []

def play_music(run):
    treks = {
        "menu": "start menu",
        "play": "dance",
        "game_over": "game over"}
    music.stop()
    music.play(treks[run])
# список птиц
def respawn_bird():
    bird = Actor ("bird")
    bird.x = random.randint(0,WIDTH)
    bird.y = random.randint (-700,-1)
    bird.speed = random.randint (2,5)
    birds.append(bird)


# список бомб
def respawn_bomb():
    bomb = Actor ("bomb")
    bomb.x = random.randint(0, WIDTH)
    bomb.y = random.randint(-700, -1)
    bomb.speed = random.randint(1, 4)
    bomba.append(bomb)

# список молний
def respawn_grom():
    grom = Actor ("molnia")
    grom.x = random.randint(0,WIDTH)
    grom.y = random.randint(-700,-1)
    grom.speed = random.randint(3,6)
    groms.append(grom)

# жизни
def respawn_live():
    global run
    live = Actor("сердце")
    live.x = WIDTH - 50 - (50 * len(lives))
    live.y = 45
    lives.append(live)


def start_game(stop=False):

    for i in range(9):
        respawn_bird()
    for i in range(4):
        respawn_bomb()
    for i in range(3):
        respawn_grom()
    if not stop:
        for i in range(5):
            respawn_live()


# отрисовка
def draw():
    global run,score
    plas.draw()

    if run == "menu":
       screen.draw.filled_rect(start_button,(255, 77, 54))
       screen.draw.text(f"ИГРАТЬ ", center=start_button.center,color=(57, 191, 71), fontsize=100)

       screen.draw.filled_rect(exit_button,(255, 77, 54))
       screen.draw.text(f"ВЫХОД",center=exit_button.center,color=(57, 191, 71),fontsize=100)

    elif run == "play" or run == "pause":
        man.draw()
        screen.draw.text(f'ОЧКИ:{score}', (20,20),color =(244, 247, 22) )
        screen.draw.text(f'РЕКОРД:{record}',(20,35),color = (244, 247 ,22))
        for bird in birds:
            bird.draw()

        for bomb in bomba:
            bomb.draw()

        for grom in groms:
            grom.draw()

        for live in lives:
            live.draw()
    elif run == "game_over":
        screen.fill('black')
        over.draw()


# действия
def update():
# движение
    global score, run

    if run == "play":
        if keyboard.K_LEFT and man.x > 0:
           man.x -= 15
        if keyboard.K_RIGHT and man.x < WIDTH:
           man.x += 15

    # # респавн птиц

        for bird in birds:
            if bird.y < HEIGHT:
                bird.y+=bird.speed
            else:
                birds.remove(bird)
                respawn_bird()
                if len(lives) > 0:
                    lives.pop()

            if man.colliderect(bird):
                score+= 1
                birds.remove(bird)
                respawn_bird()
    # респав бомб
        for bomb in bomba:
            if bomb .y < HEIGHT:
               bomb.y += bomb.speed
            else:
                bomba.remove(bomb)
                respawn_bomb()
                if len (lives) > 0:
                    lives.pop()
                    if len(lives) > 0:
                        lives.pop()
            if man.colliderect(bomb):
                score += 2
                bomba.remove(bomb)
                respawn_bomb()
    # респавн молний
        for grom in groms:
            if grom .y < HEIGHT:
               grom.y += grom.speed
            else:
                groms.remove(grom)
                respawn_grom()
                if len (lives) > 0:
                    lives.pop()
                    if len(lives) > 0:
                        lives.pop()
            if man.colliderect(grom):
                score += 1
                groms.remove(grom)
                respawn_grom()

# cтоп
        if len(lives) <= 0:

            run = "game_over"
            play_music(run)

        if score > record:
           ride_record(score)

def on_key_down(key):
    global run,score,stop

    if key == keys.SPACE:
        run = 'pause' if run == 'play' else 'play'
    if key == keys.ESCAPE:
        run = "menu"
        play_music(run)
        stop = True
    if key == keys.RETURN:
        birds.clear()
        bomba.clear()
        lives.clear()
        groms.clear()
        score = 0
        man.x = WIDTH/2
        stop = False
        start_game()
        run = 'play'
        play_music(run)




def delay():
    sleep(2)

def on_mouse_down(pos,button):
    global run,stop
    if button == mouse.LEFT and start_button.collidepoint(pos):
        print(run)
        run = "play"
        play_music(run)
        start_game(stop)
        if stop:
            clock.schedule(delay, 0.02)
    if button == mouse.LEFT and exit_button.collidepoint(pos):
        exit()

# выход



pgzrun.go()

