import math
import pygame
from math import sin, floor
from math import cos
from PIL import Image

GameMap = [[1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,1,1,1,1],
           [1,0,0,1,0,0,1,0,0,0],
           [1,0,0,1,1,0,1,0,0,0],
           [1,0,1,1,0,0,1,0,0,0],
           [1,0,0,0,0,0,1,0,0,0],
           [1,0,0,0,0,0,1,0,0,0],
           [1,1,1,1,1,1,1,0,0,0]]
question = input("Установить специальные настройки?(Yes/No):")
if question == "Yes" or question == "yes":
    imageSizeM = int(input("Разрешение картинки(1/2/4) СИЛЬНО УМЕНЬШАЕТ FPS! :"))
    detailRanderQuality = int(input("Качество рендера(1/2/3/4) СИЛЬНО УМЕНЬШАЕТ FPS! :"))
    renderSky = input("Рендерить небо?(Yes/No):")
    renderTraceLines = input("Показать лучи трассировки?(Yes/No) СЛАБО УМЕНЬШАЕТ FPS! :")
    renderMap = input("Показать стены?(Yes/No) СЛАБО УМЕНЬШАЕТ FPS! :")
    texturing = input("Текстурировать стены?(Yes/No) СИЛЬНО УМЕНЬШАЕТ FPS! :")
else:
    imageSizeM = 4
    detailRanderQuality = 3
    renderSky = "Yes"
    renderTraceLines = "Yes"
    renderMap = "Yes"
    texturing = "Yes"
TextureSize = int(8 * imageSizeM)
BlockSize = 32
WIDTH = 32 * 10
HEIGHT = 32 * 10
player_x = 48
player_y = 48
player_a = 1.523
fov = 3.14/3.
start3DPix = HEIGHT + 1
WALL = (136, 69, 53)
SKY = (127, 199, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)
clock = pygame.time.Clock()
if renderTraceLines != "Yes" and renderMap != "Yes":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start3DPix = 0
else:
    screen = pygame.display.set_mode((WIDTH * 2, HEIGHT))
texture = Image.open("wall.png")
texture.draft('RGB',(32,32))
texturePixels = texture.load()
def RenderMap():
    x = 0
    y = 0
    for fy in GameMap:
        for fx in GameMap:
            if GameMap[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * BlockSize, y * BlockSize, BlockSize, BlockSize), 1)
            x = x + 1
        x = 0
        y = y + 1
running = True
while running:
    screen.fill(BLACK)
    if renderSky == "Yes":
        pygame.draw.rect(screen, SKY, (start3DPix + 1, 0, HEIGHT, WIDTH / 2))
    if renderMap == "Yes":
        RenderMap()
    RayTraceNumber = 0
    while RayTraceNumber < WIDTH:
        angle = player_a - fov / 2 + fov * RayTraceNumber / float(WIDTH)
        RayTraceNumber = RayTraceNumber + 1
        c = 0
        while c < 10:
            cx = player_x / BlockSize + c * cos(angle)
            cy = player_y / BlockSize + c * sin(angle)
            if GameMap[int(cy)][int(cx)] == 1:
                if renderTraceLines == "Yes":
                    pygame.draw.line(screen, WHITE, [player_x, player_y], [cx * BlockSize, cy * BlockSize], 1)
                column_height = HEIGHT/(c * cos(angle - player_a))
                if texturing == "Yes":
                    hitx = cx - floor(cx + .5)
                    hity = cy - floor(cy + .5)
                    x_texcoord = hitx * TextureSize
                    if abs(hity) > abs(hitx):
                        x_texcoord = hity * TextureSize
                    if x_texcoord < 0:
                        x_texcoord += TextureSize
                    pix_x = start3DPix + RayTraceNumber
                    i = 0
                    while i < int(column_height):
                        pix_y = i + HEIGHT / 2 - column_height / 2
                        textureResized = texture.resize((TextureSize, int(column_height)), Image.NEAREST)
                        textureResizedpix = textureResized.load()
                        screen.set_at((pix_x,int(pix_y)),textureResizedpix[x_texcoord,i])
                        i = i + 1
                else:
                    pygame.draw.rect(screen, GREEN,(start3DPix + RayTraceNumber, HEIGHT / 2 - column_height / 2, 1, column_height))
                break
            c = c + 0.1 / detailRanderQuality
    clock.tick(60)
    fps = clock.get_fps()
    text_surface = my_font.render("FPS " + str(int(fps)), False, WHITE)
    screen.blit(text_surface, (0, -5))
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_a = player_a - 0.03
    elif keys[pygame.K_RIGHT]:
        player_a = player_a + 0.03
    elif keys[pygame.K_UP]:
        player_x = player_x + (2*math.cos(player_a))
        player_y = player_y + (2*math.sin(player_a))
pygame.quit()