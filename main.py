import PIL.Image
import pgerom as pe
from PIL import Image
from linearinterpolator import *
pe.init()
pe.display.make((500, 500), "Linear interpolation")

matrix = [
    [1, -1],
    [0, 1]
]
image = PIL.Image.open("image.png")
grid = (-500, -500, 500, 500, 50, 50)

def draw_grid(interpolator=no_interpolation, percent=50, color=pe.color.gray, offset=(250,250)):
    global matrix, grid
    pe.Layer[0][1] = offset
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
                pe.draw.line(color, points[0], points[1], 1)
                pe.draw.line(color, points[1], points[2], 1)
                pe.draw.line(color, points[2], points[3], 1)
                pe.draw.line(color, points[3], points[0], 1)
    pe.Layer[0][1] = (250, 250)
def draw_image(interpolator=no_interpolation, percent=50, image:PIL.Image.Image=None, offset=(250,250)):
    size = max(1,percent/75)
    pe.Layer[0][1] = offset
    for x in range(0, image.width, 10):
        for y in range(0, image.height, 10):
            pos = interpolator(matrix, x-500, y-500, percent)
            if pos[0]>=-250 and pos[0]<=250 and pos[1]>=-250 and pos[1]<=250:
                pe.draw.circle(image.getpixel((x, y)),pos,7*size, 0)
    pe.Layer[0][1] = (250, 250)

pro = 0
proi = 2
going = False
direction = 1
while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
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
    pe.fill.full(pe.color.black)
    if going:
        pro += proi*direction
    pro = max(0, min(100, pro))
    draw_grid()
    draw_image(interpolate, pro, image)
    draw_grid(interpolate, pro, pe.color.white)
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
        pe.draw.line(pe.color.red, points[0], points[1], 3)
        pe.draw.line(pe.color.red, points[1], points[2], 3)
        pe.draw.line(pe.color.red, points[2], points[3], 3)
        pe.draw.line(pe.color.red, points[3], points[0], 3)
    pe.display.update()
    pe.time.tick(120)
