import pygame
import random
import villagers_emotions
from tkinter import *
import math
#initialisation du module villagers_emotions
paused = False
villagers_happy=random.randint(50,79)
print(villagers_happy)
# Initialisation Pygame
pygame.init()
font = pygame.font.SysFont(None, 40)
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Village Pixel Art avec événement toutes les 2 secondes")
PIXEL_SIZE = 5
GRID_WIDTH = WIDTH // PIXEL_SIZE
GRID_HEIGHT = HEIGHT // PIXEL_SIZE
# Paramètres du village
#données pour le vilage tels que l argent
VILLAGE_CENTER = (GRID_WIDTH//2, GRID_HEIGHT//2)

#nombres de building hlm etc
NUM_HOUSES = WIDTH//15
NUM_FACTORIES = NUM_HOUSES // 10
NUM_HLM=0
NUM_PARC=0

village_money=0

#fonction pour trouver combien d argent on peut avoir
def factories_money(NUM_FACTORIES, NUM_HOUSES, village_money):

    workers_needed = NUM_FACTORIES * 10

    if NUM_HOUSES < workers_needed:

        print("pas assez de travailleurs pour les factories")

        missing_workers = workers_needed - NUM_HOUSES
        print("missing_workers:", missing_workers)
        village_money += NUM_HOUSES // 10
        village_money -= missing_workers
    else:
        village_money += NUM_FACTORIES

    return village_money
# Générer map verte
def generate_map():
    return [[(34,139,34) for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

# Générer bâtiments avec densité centrée
def generate_building(center_x, center_y, color):
    dx = int(random.gauss(0, 5))
    dy = int(random.gauss(0, 5))
    x = max(0, min(GRID_WIDTH-1, center_x + dx))
    y = max(0, min(GRID_HEIGHT-1, center_y + dy))
    return (x, y, color)


# Dessiner map + bâtiments
def draw_map(map_grid, buildings):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(screen, map_grid[x][y], rect)
    for b in buildings:
        x, y, color = b
        rect = (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(screen, color, rect)

# Initialisation map et bâtiments
pixel_map = generate_map()
houses = [generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (0,0,200)) for _ in range(NUM_HOUSES)]
factories = [generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200,0,0)) for _ in range(NUM_FACTORIES)]
# Événement toutes les 2 secondes
TWO_SEC_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TWO_SEC_EVENT, 2000)  # 2000 ms = 2 secondes

clock = pygame.time.Clock()
running = True



#--------------------------
#fonction tkinter
#------------------------------
#initialisation de la fenetre de city managment
#-----------------------------------------------

#initialier une fenetre tkinter pour la mainloop apres




#-----------------------------------
#fonction pour run le pygame
#-----------------------------------

while running:
    #----
    #fonctions pour cheter des buildings et des factories
    #----
    def buy_house():
        global NUM_HOUSES
        global village_money
        
        houses.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (0,0,200)))
        NUM_HOUSES = NUM_HOUSES+1
        village_money=village_money-10
       
       
       
    #fonction pour faire spawn une usine
    def buy_factory():
        global NUM_FACTORIES
        global village_money
        
        factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200,0,0)))
        NUM_FACTORIES=NUM_FACTORIES+1
        village_money=village_money - 100
    
    def buy_hlm():
        global NUM_HLM
        global village_money
        global NUM_HOUSES
        global villagers_happy
        factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (120, 0, 255)))
        NUM_HLM=NUM_HLM+1
        village_money=village_money - 95
        NUM_HOUSES=NUM_HOUSES+10
        villagers_happy = villagers_happy - 1
    def buy_parc():
        global villagers_happy
        global NUM_PARC
        global village_money
        NUM_PARC=NUM_PARC+1
        villagers_happy = villagers_happy + 2
        village_money=village_money - 120
        factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200, 255, 200)))
        
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == TWO_SEC_EVENT:
            print(2)  # ici, on print toutes les 2 secondes
            village_money=factories_money(NUM_FACTORIES,NUM_HOUSES,village_money)
            print(village_money)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #event click il faut proposer des options
            print("event click")
            #ici il faut faire pour que quand on clicke une autre fenetre se ouvre pour coisir certaines choses utuliser tkinter ?
            window=Tk()
            window.geometry("500x400")
            window.resizable(False, False)
            
            #initialiser les texts de tkinter etc
            title=Label(window,text="City managment")
            title.pack(side=TOP)
            
            #boutton pr acheter un building
            
            bouton_buy_building=Button(window, text="acheter un building $10", command=buy_house)
            bouton_buy_building.pack()
            
            #boutton pour acheter une factory
            bouton_buy_factory=Button(window, text="acheter un factory $100", command=buy_factory)
            bouton_buy_factory.pack()
            
            #bouton pour achetter un hlm
            bouton_buy_hlm=Button(window, text="acheter un hlm $95", command=buy_hlm)
            bouton_buy_hlm.pack()
            #boutton pour acheter un parc
            bouton_buy_parc=Button(window, text="acheter un parc $120", command=buy_parc)
            bouton_buy_parc.pack()
            
            window.mainloop()
            
    
    # créer le texte
    money_text = font.render(f"$ : {village_money}", True, (255,255,255))
    # position bas droite
    text_rect = money_text.get_rect()
    text_rect.bottomright = (WIDTH - 90, HEIGHT - 10)
    #creer le texte pr le hapiness
    happiness_text = font.render(f":) : {villagers_happy}", True, (255,255,255))
    # position bas droite
    happiness_text_rect = money_text.get_rect()
    happiness_text_rect.bottomright = (WIDTH - 90, HEIGHT - 40)
    
    draw_map(pixel_map, houses + factories)
    screen.blit(money_text, text_rect)
    screen.blit(happiness_text, happiness_text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()