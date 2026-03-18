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

notifications = []

# -------------------------
# TKINTER SCROLLABLE
# -------------------------

window = Tk()
window.geometry("500x400")
window.title("City management")

canvas = Canvas(window)
scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

title = Label(scrollable_frame, text="City management \n")
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
    end_time = pygame.time.get_ticks() + duration
    notifications.append((text, end_time))

def draw_notifications():
    current_time = pygame.time.get_ticks()
    y_offset = 20
    for text, end_time in notifications[:]:
        if current_time > end_time:
            notifications.remove((text, end_time))
        else:
            notif_text = font.render(text, True, (255, 255, 255))
            screen.blit(notif_text, (20, y_offset))
            y_offset += 30

# -------------------------
# INFOS BUILDINGS
# -------------------------

def building_info():

    return
    building_info = Toplevel(window)
    Label(building_info, text=f"maisons/hlm: {NUM_HOUSES}").pack()
    Label(building_info, text=f"factories: {NUM_FACTORIES}").pack()
    Label(building_info, text=f"parcs: {NUM_PARC}").pack()
    Label(building_info, text=f"cirques: {NUM_CIRCUS}").pack()
    Label(building_info, text=f"rafineries: {NUM_RAF}").pack()
    Label(building_info, text=f"banques: {NUM_BANK}").pack()
    building_info.mainloop()

# -------------------------
# ACHATS
# -------------------------

def buy_house():
    global NUM_HOUSES, village_money
    if village_money < 10:
        add_notification("Pas assez d'argent")
        return
    houses.append(generate_building(*VILLAGE_CENTER, (0,0,200)))
    NUM_HOUSES += 1
    village_money -= 10
    add_notification("Maison construite")

def buy_factory():
    global NUM_FACTORIES, village_money
    if village_money < 100:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (200,0,0)))
    NUM_FACTORIES += 1
    village_money -= 100
    add_notification("Factory construite")

def buy_hlm():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy
    if village_money < 95:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (120,0,255)))
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
    factories.append(generate_building(*VILLAGE_CENTER, (200,255,200)))
    add_notification("Parc construit")

def buy_circus():
    global NUM_CIRCUS,village_money
    if village_money < 150:
        add_notification("Pas assez d'argent")
        return
    NUM_CIRCUS += 1
    village_money -= 150
    factories.append(generate_building(*VILLAGE_CENTER,(100,200,250)))
    add_notification("Cirque construit")

def buy_raf():
    global NUM_RAF,village_money
    if village_money < 180:
        add_notification("Pas assez d'argent")
        return
    NUM_RAF += 1
    village_money -= 180
    factories.append(generate_building(*VILLAGE_CENTER,(20,20,20)))
    add_notification("Rafinerie construite")

def buy_bank():
    global NUM_BANK,village_money
    if village_money < 200:
        add_notification("Pas assez d'argent")
        return
    NUM_BANK+=1
    village_money -= 200
    factories.append(generate_building(*VILLAGE_CENTER,(0,255,0)))
    add_notification("Banque construite")

# -------------------------
# BOUTONS SCROLLABLE
# -------------------------

Button(scrollable_frame, text="Acheter maison $10", command=buy_house).pack()
Label(scrollable_frame, text="Main d'oeuvre").pack()

Button(scrollable_frame, text="Acheter factory $100", command=buy_factory).pack()
Label(scrollable_frame, text="Produit de l'argent").pack()

Button(scrollable_frame, text="Acheter HLM $90", command=buy_hlm).pack()
Label(scrollable_frame, text="+10 maisons mais - bonheur").pack()

Button(scrollable_frame, text="Acheter parc $70", command=buy_parc).pack()
Label(scrollable_frame, text="+ bonheur").pack()

Button(scrollable_frame, text="Acheter Cirque $150", command=buy_circus).pack()
Label(scrollable_frame, text="bonus bonheur").pack()

Button(scrollable_frame, text="Rafinerie $180", command=buy_raf).pack()
Label(scrollable_frame, text="- bonheur + argent").pack()

Button(scrollable_frame, text="Banque $200", command=buy_bank).pack()
Label(scrollable_frame, text="revenu aléatoire").pack()

Button(scrollable_frame, text="Infos", command=building_info).pack()

# -------------------------
# MAP INIT
# -------------------------

pixel_map = generate_map()
houses = [generate_building(*VILLAGE_CENTER, (0,0,200)) for _ in range(NUM_HOUSES)]
factories = [generate_building(*VILLAGE_CENTER, (200,0,0)) for _ in range(NUM_FACTORIES)]

# -------------------------
# TIMER
# -------------------------

TWO_SEC_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TWO_SEC_EVENT, 1000)

clock = pygame.time.Clock()
running = True

event_taxes=0
event_circus=0
event_bank=0

# -------------------------
# GAME LOOP
# -------------------------

while running:
    if village_money < 0:
        quit()
    if villagers_happy < 50:
        quit()





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == TWO_SEC_EVENT:
            event_taxes+=1
            event_circus+=1
            event_bank+=1

            if event_taxes==10:
                village_money += (NUM_HOUSES//5)
                villagers_happy -= 3
                event_taxes=0

            if event_circus==5:
                villagers_happy += 2 * NUM_CIRCUS
                villagers_happy -= 5 * NUM_RAF
                village_money += 15 * NUM_RAF
                event_circus=0

            if event_bank==15:
                village_money += random.randint(-20,20)*NUM_BANK
                event_bank=0

            village_money = factories_money(NUM_FACTORIES, NUM_HOUSES, village_money)

    screen.fill((0,0,0))
    draw_map(pixel_map, houses + factories)

    money_text = font.render(f"$ : {village_money}", True, (255,255,255))
    happiness_text = font.render(f":) : {villagers_happy}", True, (255,255,255))

    screen.blit(money_text, (WIDTH - 200, HEIGHT - 40))
    screen.blit(happiness_text, (WIDTH - 200, HEIGHT - 80))

    draw_notifications()
    pygame.display.flip()
    
    window.update()

        


    clock.tick(60)

pygame.quit()
