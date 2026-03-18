import pygame
import random
from tkinter import *
import math
# -------------------------
# VARIABLES
# -------------------------

villagers_happy = random.randint(60, 75)
pygame.init()
font = pygame.font.SysFont(None, 40)

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Village Pixel Art")

PIXEL_SIZE = 10
GRID_WIDTH = WIDTH // PIXEL_SIZE
GRID_HEIGHT = HEIGHT // PIXEL_SIZE

VILLAGE_CENTER = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

NUM_HOUSES = WIDTH // 15
NUM_FACTORIES = NUM_HOUSES // 10
NUM_HLM = 0
NUM_PARC = 0
NUM_CIRCUS = 0
NUM_RAF = 0
NUM_BANK=0
village_money = 0

notifications = []  # liste pour notifications

# -------------------------
# TKINTER (UNE SEULE FOIS)
# -------------------------

window = Tk()
window.geometry("500x400")
window.title("City management")

title = Label(window, text="City management")
title.pack(side=TOP)

# -------------------------
# FONCTIONS
# -------------------------

def factories_money(NUM_FACTORIES, NUM_HOUSES, village_money):
    workers_needed = NUM_FACTORIES * 10
    if NUM_HOUSES < workers_needed:
        missing_workers = workers_needed - NUM_HOUSES * 1.5
        village_money += (NUM_HOUSES // 10) + (NUM_FACTORIES//2)
        village_money -= missing_workers
    else:
        village_money += int(((NUM_FACTORIES * (1+(villagers_happy//100)))//1))
    return village_money

def generate_map():
    return [[(34,139,34) for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

def generate_building(center_x, center_y, color):
    dx = int(random.gauss(0, 7))
    dy = int(random.gauss(0, 7))
    x = max(0, min(GRID_WIDTH-1, center_x + dx))
    y = max(0, min(GRID_HEIGHT-1, center_y + dy))
    return (x, y, color)

def draw_map(map_grid, buildings):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(screen, map_grid[x][y], rect)
    for b in buildings:
        x, y, color = b
        rect = (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(screen, color, rect)

# -------------------------
# NOTIFICATIONS
# -------------------------

def add_notification(text, duration=2000):
    """Ajoute un message temporaire"""
    end_time = pygame.time.get_ticks() + duration
    notifications.append((text, end_time))

def draw_notifications():
    """Affiche les notifications"""
    current_time = pygame.time.get_ticks()
    y_offset = 20
    for text, end_time in notifications[:]:
        if current_time > end_time:
            notifications.remove((text, end_time))
        else:
            notif_text = font.render(text, True, (255, 255, 255))
            screen.blit(notif_text, (20, y_offset))
            y_offset += 30

#--------------------------
# CREATION DE DEUXIEME FENETRE
#--------------------------

def building_info():
    building_info = Tk()
    NUM_HOUSES_label = Label(building_info, text=f"nombre de maisons/hlm: {NUM_HOUSES}").pack()
    NUM_FACTORIES_label = Label(building_info, text=f"nombre de factories: {NUM_FACTORIES}").pack()
    
    NUM_PARC_label = Label(building_info, text=f"nombre de parc: {NUM_PARC}").pack()
    NUM_CIRCUS_label = Label(building_info, text=f"nombre de cirques: {NUM_CIRCUS}").pack()
    NUM_RAF_label = Label(building_info, text=f"nombre de rafineries: {NUM_RAF}").pack()
    NUM_BANK_label=Label(building_info, text=f"nombre de banques: {NUM_BANK}").pack()
    building_info.mainloop




# -------------------------
# ACHATS
# -------------------------

def buy_house():
    global NUM_HOUSES, village_money
    if village_money < 10:
        add_notification("Pas assez d'argent")
        return
    houses.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (0,0,200)))
    NUM_HOUSES += 1
    village_money -= 10
    add_notification("Maison construite")

def buy_factory():
    global NUM_FACTORIES, village_money
    if village_money < 100:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200,0,0)))
    NUM_FACTORIES += 1
    village_money -= 100
    add_notification("Factory construite")

def buy_hlm():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy
    if village_money < 95:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (120,0,255)))
    NUM_HLM += 1
    village_money -= 95
    NUM_HOUSES += 10
    villagers_happy -= 1
    add_notification("HLM construit")

def buy_parc():
    global NUM_PARC, village_money, villagers_happy
    if village_money < 70:
        add_notification("Pas assez d'argent")
        return
    NUM_PARC += 1
    villagers_happy += 4
    village_money -= 70
    factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200,255,200)))
    add_notification("Parc construit")
def buy_circus():
    global NUM_CIRCUS,village_money
    if village_money <  150:
        add_notification("Pas assez d'argent")
        return
    NUM_CIRCUS += 1
    village_money -= 150
    factories.append(generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1],(100,200,250)))
    add_notification("Cirque construit")
def buy_raf():
    global NUM_RAF,village_money

    if village_money < 180:
        add_notification ("Pas assez d'argent")
        return
    NUM_RAF += 1
    village_money -= 180
    factories.append(generate_building(VILLAGE_CENTER[0],VILLAGE_CENTER[1],(20,20,20)))
    add_notification("Rafinerie construite")
def buy_bank():
    global NUM_BANK,village_money
    if village_money < 200:
        add_notification("Pas assey d argent")
        return
    NUM_BANK+=1
    village_money -= 200
    factories.append(generate_building(VILLAGE_CENTER[0],VILLAGE_CENTER[1],(0,255,0)))
    add_notification("Banque construite")


# -------------------------
# BOUTONS TKINTER
# -------------------------

Button(window, text="Acheter maison $10", command=buy_house).pack()
Label(window, text="Permet d avoir de la main d oeuvre pour les factory\n").pack()
Button(window, text="Acheter factory $100", command=buy_factory).pack()
Label(window, text="Permet de produire de l argent toutes les secondes si il y a assez de mains d oeuvre\n").pack()
Button(window, text="Acheter HLM $90", command=buy_hlm).pack()
Label(window, text="Permet d avoir de la main d oeuvre pour la factory mais diminue la joie de habitants (1 hlm = 10 maisons)\n").pack()
Button(window, text="Acheter parc $70", command=buy_parc).pack()
Label(window, text="Permet d avoir de la joie \n").pack()
Button(window, text= "Acheter Cirque $150", command=buy_circus).pack()
Label(window, text="Permet d avoir un revenu passif de joie \n").pack()
Button(window,text="acheter une rafinerie $180", command=buy_raf).pack()
Label(window, text="Diminue la joie des habitants mais genere un revenu passif \n").pack()
Button(window, text="Acheter une baque $200", command=buy_bank).pack()
Label(window, text="Permet d avoir un revenu passif aleatoire compris entre -20 et 20 \n").pack()
Button(window, text="info sur les buildings", command=building_info).pack()

# -------------------------
# MAP INIT
# -------------------------

pixel_map = generate_map()
houses = [generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (0,0,200)) for _ in range(NUM_HOUSES)]
factories = [generate_building(VILLAGE_CENTER[0], VILLAGE_CENTER[1], (200,0,0)) for _ in range(NUM_FACTORIES)]

# -------------------------
# TIMER
# -------------------------

TWO_SEC_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TWO_SEC_EVENT, 1000)

clock = pygame.time.Clock()
running = True

# -------------------------
# GAME LOOP
# -------------------------
event_taxes=0
event_circus=0
event_raf=0
event_bank=0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == TWO_SEC_EVENT:
            event_taxes=event_taxes+1
            event_circus=event_circus+1
            event_bank=event_bank+1
            #faire un event ou on reçoit de l argent selon le nombre de personnes et leurs happiness mais apres leurs hapinness va desendre
            
            if event_taxes==10:
                village_money=village_money + (NUM_HOUSES//5)
                villagers_happy = villagers_happy - 3
                event_taxes=0
                add_notification("impots +", village_money)
                
                malus=NUM_BANK * 4 + NUM_RAF * 5 + NUM_CIRCUS * 2 + NUM_PARC*2
                malus += villagers_happy //20
                if malus > 0:
                    add_notification(f"Malus : entretiens - {malus}")
                village_money -= malus
            if event_circus==5:
                #event cirque
                if villagers_happy < 100:
                    villagers_happy=villagers_happy + 2 *NUM_CIRCUS
                event_circus=0
                if NUM_RAF > 0:
                    villagers_happy=villagers_happy - 5 * NUM_RAF
                    village_money=village_money + 15 * NUM_RAF
                village_money=village_money+(villagers_happy // 10)
            if event_bank == 15:
                
                if NUM_BANK > 0:

                    oldvillage_money=village_money + (random.randint(-20,20))*NUM_BANK
                    print("banque donnée argent")
                    print("votre balance va etre de + ",oldvillage_money - village_money)
                    village_money=oldvillage_money


                event_bank=0


            elif villagers_happy < 50:
                print("fin du jeu la")

                quit()
            
            village_money = factories_money(NUM_FACTORIES, NUM_HOUSES, village_money)
            
    if village_money < 0:
        print("plus d argent")
        quit()
    # Dessin
    screen.fill((0,0,0))
    draw_map(pixel_map, houses + factories)
    # Texte argent et bonheur
    money_text = font.render(f"$ : {village_money}", True, (255,255,255))
    happiness_text = font.render(f":) : {villagers_happy}", True, (255,255,255))
    screen.blit(money_text, (WIDTH - 200, HEIGHT - 40))
    screen.blit(happiness_text, (WIDTH - 200, HEIGHT - 80))
    # Notifications
    draw_notifications()
    pygame.display.flip()
    # Update Tkinter
    window.update()
    clock.tick(60)
pygame.quit()
