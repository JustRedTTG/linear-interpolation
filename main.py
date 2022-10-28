import time

import PIL.Image
import pygameextra as pe
from linearinterpolator import *
pe.init()
pe.display.make((500, 500), "Linear interpolation")
qal = 4
matrix = [
    #i   #j
    [0, -1], # X
    [-1, 1]   # Y
]
image = PIL.Image.open("image.png")
grid = (-500, -500, 500, 500, 50, 50)

def draw_grid(interpolator=no_interpolation, percent=50, color=pe.colors.gray, offset=(250,250)):
    global matrix, grid
    #pe.Layer[0][1] = offset
    for x in range(grid[0], grid[2]+1, grid[4]):
        for y in range(grid[1], grid[3]+1, grid[5]):
            if x<grid[2] and y<grid[3]:
                startpoint = interpolator(matrix, x, y, percent)
                endpoint = interpolator(matrix, x+grid[4], y+grid[5], percent)
                points = (
                    interpolator(matrix, x, y, percent),
                    interpolator(matrix, x+grid[4], y, percent),
                    interpolator(matrix, x+grid[4], y+grid[5], percent),
                    interpolator(matrix, x, y+grid[5], percent),
                )
                points = [(p[0] + offset[0], p[1] + offset[1]) for p in points]
                pe.draw.line(color, points[0], points[1], 1)
                pe.draw.line(color, points[1], points[2], 1)
                pe.draw.line(color, points[2], points[3], 1)
                pe.draw.line(color, points[3], points[0], 1)
    #pe.Layer[0][1] = (250, 250)
def draw_image(interpolator=no_interpolation, percent=50, image:PIL.Image.Image=None, offset=(250,250)):
    size = max(1, percent/75)
    #pe.Layer[0][1] = offset
    for x in range(0, image.width, qal):
        for y in range(0, image.height, qal):
            pos = interpolator(matrix, x-500, y-500, percent)
            if -250 <= pos[0] <= 250 and -250 <= pos[1] <= 250:
                pos = int(pos[0]+offset[0]), int(pos[1]+offset[1])
                pe.draw.rect((*image.getpixel((x, y)), 10),(*pos, 7*size, 7*size),0)
    #pe.Layer[0][1] = (250, 250)

pro = 0
proi = 2
going = False
direction = 1
delta_time = 0
pre_delta_time = 0
last_go = time.time()
while True:
    t = pe.pygame.time.get_ticks()
    for pe.event.c in pe.event.get():
        pe.event.quitCheckAuto()
        if pe.event.key_DOWN(1073741903):
            going = True
            direction = 1
        elif pe.event.key_UP(1073741903):
            going = False
        if pe.event.key_DOWN(1073741904):
            going = True
            direction = -1
        elif pe.event.key_UP(1073741904):
            going = False
    if going:
        last_go = time.time()
        qal = max(10, min(25, qal + 3))
    elif .1 < time.time()-last_go < .2:
        qal = max(1, qal - 4)
    elif delta_time > 0.3:
        qal = min(20, qal + 1)
    else:
        qal = max(2, qal - 1)
    #pe.fill.full(pe.colors.black)
    if going:
        pro += proi*direction
        pe.fill.transparency(pe.colors.black, 10)
    pro = max(0, min(100, pro))
    if not going:
        draw_grid()
    if not time.time()-last_go > 1.3:
        draw_image(interpolate, pro, image)
    if not going:
        draw_grid(interpolate, pro, pe.colors.white)
    if pro <= 10 or pro >= 90:
        pos = pe.mouse.pos()
        pos = (pos[0]-250, pos[1]-250)
        x, y = reverse_interpolate(matrix, *pos, pro)
        if x<0:
            x = int(x/grid[4] - 1) * grid[4]
        else:
            x = int(x/grid[4]) * grid[4]
        if y<0:
            y = int(y/grid[5] - 1) * grid[5]
        else:
            y = int(y/grid[5]) * grid[5]
        points = (
            interpolate(matrix, x, y, pro),
            interpolate(matrix, x + grid[4], y, pro),
            interpolate(matrix, x + grid[4], y + grid[5], pro),
            interpolate(matrix, x, y + grid[5], pro),
        )
        pe.draw.line(pe.colors.red, points[0], points[1], 3)
        pe.draw.line(pe.colors.red, points[1], points[2], 3)
        pe.draw.line(pe.colors.red, points[2], points[3], 3)
        pe.draw.line(pe.colors.red, points[3], points[0], 3)
    delta_time = (t - pre_delta_time) / 1000
    pe.display.update()
    pre_delta_time = t
