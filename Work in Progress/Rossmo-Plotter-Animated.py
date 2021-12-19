import os, sys, math, csv, glob, random, shutil
from numpy import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.bmp")]
    frame_one = frames[0]
    frame_one.save("Final Result.gif", format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)


def Rossmo(i2,c1,RES_PREFIX,Dist,B,f,g):
    
    BLEND_PERCENTAGE=0.5
    font = ImageFont.truetype('Comfortaa.ttf', size=18)
    fontmain = ImageFont.truetype('Comfortaa.ttf', size=20)
    color = 'rgb(255, 255, 255)'
    final_image=RES_PREFIX+".bmp"
    c = open(c1, 'r')

    crimesx=[]
    crimesy=[]
    weight=[]

    with open(c1, 'rt') as fcsv:
      reader = csv.reader(fcsv)
      for row in reader:
       num, a, b, c= row
       crimesx.append(a)
       crimesy.append(b)
       weight.append(c)

    NB_CRIMES=len(crimesx)
    NB_CRIMESbis = len(crimesy)
    if NB_CRIMES != NB_CRIMESbis:
     print('The number of x coordinates is different from the number of y coordinates!! Please check the data')

    crime_x=[]
    crime_y=[]
    pesi=[]

    for it in range (NB_CRIMES):
      crime_x.append(float(crimesx[it]))
      crime_y.append(float(crimesy[it]))
      pesi.append((float(weight[it])/100))  

    im2 = Image.open(i2)
    WIDTH, HEIGHT = im2.size
    uscita = 0

    i=0
    for i in range (NB_CRIMES):	

      if (crime_x[i] > (WIDTH-3)):
        uscita = 1
      if (crime_y[i] > (HEIGHT-3)):
        uscita = 1
      if (crime_x[i] < 3):
        uscita = 1
      if (crime_y[i] < 3):
        uscita = 1

    if (uscita > 0):
      print(" one or more points are OUT of the image OR are too near the image border (less 3 pixels)- check input data - exiting!")
      sys.exit (0)

    i1=Image.new("RGB",(WIDTH,HEIGHT), "white")
    i1.save("Base.bmp")
    i1 = "Base.bmp"
    i4 = RES_PREFIX+"-blank.bmp"
    im1 = Image.open(i1)
    im1.save(i4)
    immagine= zeros( (WIDTH,HEIGHT) )
    print(' Image dimensions in pixel:',WIDTH,HEIGHT)
    im4 = Image.open(i4)
    if Dist == "M" :
     for i in range (WIDTH):
      for j in range (HEIGHT):
       result = 0
       for n in range (NB_CRIMES):
         distance = (math.fabs(i - crime_x[n])+math.fabs(j-crime_y[n]))
         if distance > B:
           term1 = 1 / math.pow(distance,f)
           result = result + pesi[n]*term1
         else:
           term2=(math.pow(B,(g-f)))/math.pow((2*B-distance),g)
           result = result + pesi[n]*term2
       immagine[i][j]=result
       
       if(i==0 and j==0):
         biggest_p = result;
         smallest_p = result;
       if(result > biggest_p):
         biggest_p = result; 
       if(smallest_p > result):
         smallest_p = result;
    else:
     for i in range (WIDTH):
      for j in range (HEIGHT):
       result = 0
       for n in range (NB_CRIMES):
         distance = math.sqrt(math.pow((math.fabs(i - crime_x[n])), 2) + math.pow((math.fabs(j-crime_y[n])),2))
         if distance > B:
           term1 = 1 / math.pow(distance,f)
           result = result + pesi[n]*term1
         else:
           term2=(math.pow(B,(g-f)))/math.pow((2*B-distance),g)
           result = result + pesi[n]*term2
       immagine[i][j]=result
       
       if(i==0 and j==0):
         biggest_p = result;
         smallest_p = result;
       if(result > biggest_p):
         biggest_p = result; 
       if(smallest_p > result):
         smallest_p = result;
    #print(" Calculation completed. Plotting.. ")
    draw = ImageDraw.Draw(im4)
    for i in range (WIDTH):
      for j in range (HEIGHT):
       result = immagine[i][j]
       resultrel = ((result-smallest_p)*255/(biggest_p-smallest_p))
       fracres, intres = math.modf(resultrel) 
       intintres = int(intres)
       if (intintres <= 219):
        im4.putpixel((i,j),(0, intintres, 255-intintres))
       elif ((intintres > 219)and (intintres <= 231)):
        im4.putpixel((i,j),(0, intintres, 0))
       elif ((intintres>231)and(intintres <=243)):
        im4.putpixel((i,j),(255, 255, 0)) 
       else:
        im4.putpixel((i,j),(255, 0, 0))
    #print(" Drawing points.. ", end=' ')
    
    for cross in range (NB_CRIMES):
      draw.ellipse((crime_x[cross]-1, crime_y[cross]-1, crime_x[cross]+1, crime_y[cross]+1), fill=(255,255,255))
      txt="n."+str(int(cross+1))+" ("+str(crime_x[cross])[:-2]+","+str(crime_y[cross])[:-2]+")"
      lentest=len(txt)
      draw.text((crime_x[cross]-int(5*lentest/2), crime_y[cross]-13),txt, fill=color, font=font)
      draw.text((25,25),"Created using Rossmoss-Plotter v0.2 by Amlan Saha Kundu, 2021", fill=color, font=fontmain)
      param = " B: "+str(B)+"\n f : "+str(f)+"\n g: "+str(g)
      draw.text((25,75),param, fill=color, font=font)
    #print(" Saving image and deleting temporary files")
    im4.save(i4)
    im1=Image.open(i2)
    im2=Image.open(i4)
    im3=Image.blend(im1, im2, BLEND_PERCENTAGE)
    im3.save(final_image)
    os.remove(i1)
    os.remove(i4) #-blank

    



try:
    os.mkdir("OUTPUT")
except:
    pass

os.chdir("./")
print("="*60+"\nDemo: Rossmoss-Plotter - Multi v0.3")
print("Author: Amlan Saha Kundu\n"+"="*60)

flist = []
types = ["*.jpg","*.png","*.bmp","*.webp"]
for i in range(len(types)):
    for file in glob.glob(types[i]):
        flist.append(file)
#print(flist)
print("\nPlease select the Map from the following:\n ")
for i in range(len(flist)):
    print("\t"+str(i+1)+". "+flist[i])
    
print("\n")
flag_qsi = 0

while flag_qsi == 0:
    qsi = int(input("Enter File Index: "))
    try:
        file = flist[qsi-1]
        flag_qsi = 1
    except:
        print("\nPlease select Correct Index from the above list.")
        flag_qsi = 0

print("\n"+"="*35+"\nYou have selected : "+file+"\n"+"="*35+"\n")


image = Image.open(file)
width, height = image.size



val = int(input("Enter number of Crimes (max 10): "))
x_cor = []
y_cor = []

for i in range(val):
    x_cor.append(random.randint(100,height-100))
    y_cor.append(random.randint(100,width-100))

#print(x_cor, y_cor)
weight = 100//val 
    
coor_file = "Co-ordinate-"+str(random.randint(10000,99999))+".csv"

print("\nGenerating random crime co-ordinates...")
for i in range(val):
    f = open(coor_file,"a")
    f.write(str(i+1)+","+str(x_cor[i])+","+str(y_cor[i])+","+ str(weight)+"\n")
    f.close()
    
print("Random co-ordinates are generated and saved in ",coor_file)

print("\nNow, please enter calculating parameters...\n")
B = input("Enter B (Buffer radius): ")
#f = input("Enter f (0<f<1): ")
#g = input("Enter g (0<f<1): ")

output_name = input("Enter name of the output Folder: ")
print("\nCalculating...\n")
os.mkdir("./OUTPUT/"+output_name)
shutil.move(coor_file,"./OUTPUT/"+output_name+"/"+coor_file)

for i in range(1,10):
    for j in range(1,10):
        f = 0.1*i
        f = round(f,1)
        g = 0.1*j
        g = round(g,1)
        i2 = file
        c1 = "./OUTPUT/"+output_name+"/"+coor_file
        RES_PREFIX = "./OUTPUT/"+output_name+"/Prediction-"+str(B)+"-"+str(f)+"-"+str(g)
        Dist = "E"
        B = int(B)
        f = float(f)
        g = float(g)
        print("Generating map for f =",f," g=",g)
        Rossmo(i2,c1,RES_PREFIX,Dist,B,f,g)

        make_gif("./OUTPUT/"+output_name)


