import os
import sys
import random
from threading import Timer
import pygame as pg

pg.init()
clock = pg.time.Clock()
SIZE = WIDTH, HEIGHT = 789, 500
screen = pg.display.set_mode(SIZE)
pg.display.set_caption('Aim Training')
BACKGROUND = pg.Color('#7fc7ff')
FPS = 60
SPEED = 200

running = True


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


class Mountain(pg.sprite.Sprite):
    image = load_image("grass.png")
    mask = pg.mask.from_surface(image)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT


all_sprites = pg.sprite.Group()
mountain = Mountain()


class Landing(pg.sprite.Sprite):
    image = load_image("pt.png")
    image_boom = load_image("bbom.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()

        self.mask = pg.mask.from_surface(self.image)

        self.rect.x = random.randrange(WIDTH - 45)
        self.rect.y = random.randint(-300, 100)

    def update(self, *args):
        if not pg.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)
        else:
            self.kill()
        if args and args[0].type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


def time_land():
    Landing()
    Timer(1, time_land).start()


time_land()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            all_sprites.update(event)

    screen.fill(BACKGROUND)
    all_sprites.update()
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
