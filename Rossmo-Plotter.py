import os
import sys
import math
import csv
import glob
import random
import shutil
from numpy import *
from PIL import Image, ImageDraw, ImageFont

def Rossmo(i2, c1, RES_PREFIX, Dist, B, f, g):
    BLEND_PERCENTAGE = 0.5
    font = ImageFont.truetype('Comfortaa.ttf', size=18)
    fontmain = ImageFont.truetype('Comfortaa.ttf', size=20)
    color = 'rgb(255, 255, 255)'
    final_image = RES_PREFIX + ".bmp"
    
    c = open(c1, 'r')
    crimesx = []
    crimesy = []
    weight = []

    with open(c1, 'rt') as fcsv:
        reader = csv.reader(fcsv)
        for row in reader:
            num, a, b, c = row
            crimesx.append(a)
            crimesy.append(b)
            weight.append(c)

    NB_CRIMES = len(crimesx)
    NB_CRIMESbis = len(crimesy)
    if NB_CRIMES != NB_CRIMESbis:
        print('The number of x coordinates is different from the number of y coordinates!! Please check the data')

    crime_x = []
    crime_y = []
    pesi = []

    for it in range(NB_CRIMES):
        crime_x.append(float(crimesx[it]))
        crime_y.append(float(crimesy[it]))
        pesi.append((float(weight[it]) / 100))

    im2 = Image.open(i2)
    WIDTH, HEIGHT = im2.size
    uscita = 0

    for i in range(NB_CRIMES):
        if (crime_x[i] > (WIDTH - 3)):
            uscita = 1
        if (crime_y[i] > (HEIGHT - 3)):
            uscita = 1
        if (crime_x[i] < 3):
            uscita = 1
        if (crime_y[i] < 3):
            uscita = 1

    if (uscita > 0):
        print("One or more points are out of the image or too near the image border (less than 3 pixels). "
              "Please check the input data.")
        #sys.exit(0)

    i1 = Image.new("RGB", (WIDTH, HEIGHT), "white")
    i1.save("Base.bmp")
    i1 = "Base.bmp"
    i4 = RES_PREFIX + "-blank.bmp"
    im1 = Image.open(i1)
    im1.save(i4)
    immagine = zeros((WIDTH, HEIGHT))
    print('Image dimensions in pixel:', WIDTH, HEIGHT)
    im4 = Image.open(i4)
    
    if Dist == "M":
        for i in range(WIDTH):
            for j in range(HEIGHT):
                result = 0
                for n in range(NB_CRIMES):
                    distance = (math.fabs(i - crime_x[n]) + math.fabs(j - crime_y[n]))
                    if distance > B:
                        term1 = 1 / math.pow(distance, f)
                        result = result + pesi[n] * term1
                    else:
                        term2 = (math.pow(B, (g - f))) / math.pow((2 * B - distance), g)
                        result = result + pesi[n] * term2
                immagine[i][j] = result

                if (i == 0 and j == 0):
                    biggest_p = result
                    smallest_p = result
                if (result > biggest_p):
                    biggest_p = result
                if (smallest_p > result):
                    smallest_p = result
    else:
        for i in range(WIDTH):
            for j in range(HEIGHT):
                result = 0
                for n in range(NB_CRIMES):
                    distance = math.sqrt(math.pow((math.fabs(i - crime_x[n])), 2) + math.pow((math.fabs(j - crime_y[n])), 2))
                    if distance > B:
                        term1 = 1 / math.pow(distance, f)
                        result = result + pesi[n] * term1
                    else:
                        term2 = (math.pow(B, (g - f))) / math.pow((2 * B - distance), g)
                        result = result + pesi[n] * term2
                immagine[i][j] = result

                if (i == 0 and j == 0):
                    biggest_p = result
                    smallest_p = result
                if (result > biggest_p):
                    biggest_p = result
                if (smallest_p > result):
                    smallest_p = result
    
    print("Calculation completed. Plotting..")
    draw = ImageDraw.Draw(im4)
    
    for i in range(WIDTH):
        for j in range(HEIGHT):
            result = immagine[i][j]
            resultrel = ((result - smallest_p) * 255 / (biggest_p - smallest_p))
            fracres, intres = math.modf(resultrel)
            intintres = int(intres)
            if (intintres <= 219):
                im4.putpixel((i, j), (0, intintres, 255 - intintres))
            elif ((intintres > 219) and (intintres <= 231)):
                im4.putpixel((i, j), (0, intintres, 0))
            elif ((intintres > 231) and (intintres <= 243)):
                im4.putpixel((i, j), (255, 255, 0))
            else:
                im4.putpixel((i, j), (255, 0, 0))
    
    print("Drawing points.. ", end=' ')
    for cross in range(NB_CRIMES):
        draw.ellipse((crime_x[cross] - 1, crime_y[cross] - 1, crime_x[cross] + 1, crime_y[cross] + 1), fill=(255, 255, 255))
        txt = "n." + str(int(cross + 1)) + " (" + str(crime_x[cross])[:-2] + "," + str(crime_y[cross])[:-2] + ")"
        lentest = len(txt)
        draw.text((crime_x[cross] - int(5 * lentest / 2), crime_y[cross] - 13), txt, fill=color, font=font)
        draw.text((25, 25), "Created using Rossmoss-Plotter v0.3 by Amlan Saha Kundu, 2023", fill=color, font=fontmain)
        param = " B: " + str(B) + "\n f : " + str(f) + "\n g: " + str(g)
        draw.text((25, 75), param, fill=color, font=font)
    
    print("Saving image and deleting temporary files")
    im4.save(i4)
    im1 = Image.open(i2)
    im2 = Image.open(i4)
    im3 = Image.blend(im1, im2, BLEND_PERCENTAGE)
    im3.save(final_image)
    os.remove(i1)
    os.remove(i4)  # -blank
    print("Image saved as...", final_image)

try:
    os.mkdir("OUTPUT")
except FileExistsError:
    print("")

os.chdir("./")
print("=" * 60 + "\nDemo: Rossmoss-Plotter v0.3")
print("Author: Amlan Saha Kundu\n" + "=" * 60)

flist = []
types = ["*.jpg", "*.png", "*.bmp", "*.webp"]
for i in range(len(types)):
    for file in glob.glob(types[i]):
        flist.append(file)

print("\nPlease select the Map from the following:\n ")
for i in range(len(flist)):
    print("\t" + str(i + 1) + ". " + flist[i])

print("\n")
flag_qsi = 0

while flag_qsi == 0:
    qsi = int(input("Enter File Index: "))
    try:
        file = flist[qsi - 1]
        flag_qsi = 1
    except IndexError:
        print("\nPlease select Correct Index from the above list.")
        flag_qsi = 0

print("\n" + "=" * 35 + "\nYou have selected: " + file + "\n" + "=" * 35 + "\n")

image = Image.open(file)
width, height = image.size

val = int(input("Enter number of Crimes (max 10): "))
x_cor = []
y_cor = []

border_range = 50  # Range of pixels to keep away from the image border

for i in range(val):
    x_cor.append(random.randint(border_range, width - border_range))
    y_cor.append(random.randint(border_range, height - border_range))

weight = 100 // val

output_name = input("Enter name of the output Folder: ")
output_directory = "./OUTPUT/" + output_name

try:
    os.mkdir(output_directory)
except FileExistsError:
    print("The output directory already exists.")
    #sys.exit(0)

coor_file = "Co-ordinate-" + str(random.randint(10000, 99999)) + ".csv"
coor_file_path = (output_directory+"/"+coor_file)

print("\nGenerating random crime coordinates...")
for i in range(val):
    with open(coor_file_path, "a") as f:
        f.write(str(i + 1) + "," + str(x_cor[i]) + "," + str(y_cor[i]) + "," + str(weight) + "\n")

print("Random coordinates are generated and saved in", coor_file_path)

print("\nNow, please enter the calculation parameters...\n")
B = input("Enter B (Buffer radius): ")
f = input("Enter f (0 < f < 1): ")
g = input("Enter g (0 < g < 1): ")

print("\nCalculating...\n")
i2 = file
c1 = coor_file_path
RES_PREFIX = (output_directory +"/"+ "Prediction-" + B + "-" + f + "-" + g)
Dist = "E"
B = int(B)
f = float(f)
g = float(g)

Rossmo(i2, c1, RES_PREFIX, Dist, B, f, g)
