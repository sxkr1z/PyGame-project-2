import os
import sys
import random
from threading import Timer
import pygame as pg

pg.init()
pg.font.init()
running = True

score = 0
clock = pg.time.Clock()

BACKGROUND = pg.Color('#7fc7ff')
SIZE = WIDTH, HEIGHT = 780, 500
FPS = 60
SPEED = 200

screen = pg.display.set_mode(SIZE)
pg.display.set_caption('Aim Training')


def load_image(name: str,
               colorkey: None | pg.Color | str | int = None) -> pg.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Grass(pg.sprite.Sprite):
    image = load_image("grass.png")
    mask = pg.mask.from_surface(image)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Grass.image
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT


all_sprites = pg.sprite.Group()
grass = Grass()


class Star(pg.sprite.Sprite):
    global score
    image = load_image("star.png")
    image_bboom = load_image("bbom.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = random.randrange(WIDTH - 45)
        self.rect.y = random.randint(-300, 100)

    def update(self, *args):
        global score
        if not pg.sprite.collide_mask(self, grass):
            self.rect = self.rect.move(0, 1)
        else:
            self.kill()
        if args and args[0].type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_bboom
            score += 1


def time_star():
    Star()
    Timer(1, time_star).start()


time_star()

while running:
    font = pg.font.Font("data/impact2.ttf", 30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            all_sprites.update(event)
    screen.fill(BACKGROUND)
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    all_sprites.update()
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
