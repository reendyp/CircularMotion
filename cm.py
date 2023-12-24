import pygame
import math
import csv

# Welcome

print(""" ============ Welcome to Our Simulation ============ """)

print("""
      Hei!
      Comment allez-vous?
      Wie geht es dir?
      Kaifa haluk?
      Apa kabar?
      元気ですか？
      Hoe gaat het met je?
      """)


print(""" Please wait ... """)

# Preamble
load2 = input("Press F for Fun :D : ")
if load2 == "F".lower():
    intro = open("intro.txt","r")
    for info in intro:
        print(info)
    intro.close()
    
# input data from user
print("""
      ==================== PORTAL ====================""")
username = input("Masukkan nama Anda : ")
npm = input("Masukkan NPM Anda : ")

# Saving Data User
with open("datauser.csv", mode="a") as save_data:
    
    ket = ["NAMA","NPM"]
    input_data = csv.DictWriter(save_data, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL,fieldnames=ket)
    if save_data.tell() == 0:
        input_data.writeheader()
    
    input_data.writerow({"NAMA": username,"NPM": npm})
print("""
      ====================Data Saved====================""")

# READY
hi = input("Are You Ready Kids?!!! YES / no : ")

pygame.init() 

lebar = 800
tinggi = 800
window = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Planet Simulation")


dict_warna = {
    "putih": (255,255,255),
    "kuning": (255,255,0),
    "biru": (100,149,237),
    "merah": (188,39,50),
    "abu": (80,78,81),
    "coklat": (255,234,91),
    "cream": (255,255,153),
    "cyan": (0,128,255),
    "pale": (153,204,255)
}

font = pygame.font.SysFont("comicsans",16)

class Planet:
    AU=149.6e6*1000
    G=6.67428e-11
    SCALE=250/AU
    TIMESTEP=3600*24

    def __init__(self, x, y, radius, color, mass):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.mass=mass

        self.orbit=[]
        self.sun=False
        self.matahari=False
        self.distance_to_matahari=0

        self.x_vel=0
        self.y_vel=0
        
    def draw(self, window):
        x=self.x*self.SCALE+lebar/2
        y=self.y*self.SCALE+tinggi/2

        if len(self.orbit)>2:
            updated_points=[]
            for point in self.orbit:
                x,y=point
                x=x*self.SCALE+lebar/2  
                y=y*self.SCALE+tinggi/2
                updated_points.append((x,y))

            pygame.draw.lines(window,self.color,False,updated_points,2)

        pygame.draw.circle(window,self.color,(x,y),self.radius)
        if not self.matahari:
            distance_text=font.render(f"{round(self.distance_to_matahari/1000,1)}km",1,dict_warna['putih'])
            window.blit(distance_text,(x - distance_text.get_width()/2,y - distance_text.get_height()/2))

    def attraction(self,other):
        other_x,other_y=other.x,other.y
        distance_x=other_x - self.x
        distance_y=other_y - self.y
        distance=math.sqrt(distance_x**2 + distance_y**2)

        if other.matahari:
            self.distance_to_matahari=distance

        force=self.G*self.mass*other.mass/distance**2
        theta=math.atan2(distance_y,distance_x)
        force_x=math.cos(theta)*force
        force_y=math.sin(theta)*force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))  
        
    def update_position_elips(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
     
def normal(warna, window):
    run=True
    clock=pygame.time.Clock()

    #matahari=Planet(0,0,20,kuning,1.98892*10**30)
    matahari=Planet(0,0,30,warna['kuning'],1.98892*10**30)
    matahari.matahari=True

    #bumi=Planet(-0.6*Planet.AU,0,11,biru,5.9742*10**24)
    bumi=Planet(-1*Planet.AU,0,16,warna['biru'],5.9742*10**24)
    bumi.y_vel=29.783*1000

    #mars=Planet(-0.8*Planet.AU,0,8,merah,6.39*10**23)
    mars=Planet(-1.524*Planet.AU,0,12,warna['merah'],6.39*10**23)
    mars.y_vel=24.077*1000

    #merkurius=Planet(0.2*Planet.AU,0,6,abu,3.30*10**23)
    merkurius=Planet(0.387*Planet.AU,0,8,warna['abu'],3.30*10**23)
    merkurius.y_vel=-47.4*1000

    #venus=Planet(0.4*Planet.AU,0,7,putih,4.8685*10**24)
    venus=Planet(0.723*Planet.AU,0,14,warna['putih'],4.8685*10**24)
    venus.y_vel=-35.02*1000

    #jupiter=Planet(1*Planet.AU,0,16,coklat,1.89813*(10**27))
    jupiter=Planet(5.2*Planet.AU,0,16,warna['coklat'],1.89813*(10**27))
    jupiter.y_vel=-13.06*1000

    #saturnus=Planet(1.2*Planet.AU,0,13,cream,5.683*10**26)
    saturnus=Planet(9.5*Planet.AU,0,13,warna['cream'],5.683*10**26)
    saturnus.y_vel=-9.67*1000

    #uranus=Planet(-1.4*Planet.AU,0,14,pale,8.68103*10**25)
    uranus=Planet(-19.8*Planet.AU,0,14,warna['pale'],8.68103*10**25)
    uranus.y_vel=6.79*1000

    #neptunus=Planet(-1.6*Planet.AU,0,15,cyan,1.024*10**26)
    neptunus=Planet(-30*Planet.AU,0,15,warna['cyan'],1.024*10**26)
    neptunus.y_vel=5.45*1000

    planets=[matahari,bumi,mars,merkurius,venus,jupiter,saturnus,uranus,neptunus]

    while run :
        clock.tick(60)
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        for planet in planets:
            planet.update_position_elips(planets)
            planet.draw(window)

        pygame.display.update()
    pygame.quit() 

def char_mars():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
def char_bumi():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
def char_merkurius():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)

def char_saturnus():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
def char_uranus():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
def char_neptunus():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
def char_jupiter():

    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)

def char_venus():
    
    with open("DataMars.csv",mode="r") as csv_file:
        baca_csv = csv.reader(csv_file, delimiter="\n")
        for row in baca_csv:
            print(row)
            
print("""
             ================= Choose ================= 
             [A] Animasi Planet
             [B] Karakteristik Planet
             """)
var = input("Please Select : ")   
if var == "A".lower():
    normal(dict_warna, window)
elif var != "A".lower():
    print("Selamat mengeksplor planet!")
else:
    print("Terima Kasih")
    
print("""
          [1] Mars
          [2] Bumi
          [3] Merkurius
          [4] Saturnus
          [5] Uranus
          [6] Neptunus
          [7] Jupiter
          [8] Venus
          """)
    
menu_planet = input("Planet apa yang ingin Anda ketahui?")
def planet_option():
    if menu_planet == "1":
        char_mars()
    elif menu_planet == "2":
        char_bumi()
    elif menu_planet =="3":
        char_merkurius
    elif menu_planet == "4":
        char_saturnus()
    elif menu_planet =="5":
        char_uranus()
    elif menu_planet == "6":
        char_neptunus()
    elif menu_planet =="7":
        char_jupiter()    
    elif menu_planet == "8":
        char_venus()
    else:
        print("Please input based on list")
        
planet_option()

if menu_planet != "1" or "2"or "3" or "4" or "5" or "6" or "6" or "7" or "8":
        menu_planet = input("Please input the correct option :")
        
        planet_option()
else:
    print("Thank You")
