# use PIL to draw simultaneuosly to memory and then save to file
# PIL allows .png .jpg .gif or .bmp file formats
from PIL import Image, ImageDraw, ImageFont
# some color constants for PIL
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0,128,0)
width = 800
height = 480
# create empty PIL image and draw objects to draw on
# PIL draws in memory only, but the image can be saved
image = Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)
# draw horizontal lines
x1 = 0
x2 = 450
for k in range(0, 500, 50):
    y1 = k
    y2 = k
    # PIL (to memory for saving to file)
    draw.line((x1, y1, x2, y2), black)    
# draw vertical lines
y1 = 0
y2 = 450
for k in range(0, 500, 50):
    x1 = k
    x2 = k
    # PIL
    draw.line((x1, y1, x2, y2), black)
# Draw text
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
draw.text((20,20), "Hello World!", fill=(255, 0, 0, 128), font=fnt)
# PIL image can be saved as .png .jpg .gif or .bmp file
filename = "../mylines.jpg"
image.save(filename)
