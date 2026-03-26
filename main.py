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
village_money = 50
NUM_WORK=0
NUM_GENERATOR = 2
electricity = 50
max_electricity = 50
industrial_bonus=1
polution = True




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
    global electricity
    if electricity > 0:
        workers_needed = NUM_HOUSES * 3
        if NUM_WORK < workers_needed:
            missing_workers = workers_needed - NUM_WORK
            village_money += ((NUM_HOUSES // 10) + (NUM_FACTORIES//2)*industrial_bonus)//1
            village_money -= missing_workers
        else:
            village_money += int((((NUM_FACTORIES * (1+(villagers_happy//100)))//1))*industrial_bonus)//1
        return village_money


def generate_map():
    return [[(87, 171, 97) for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]


def generate_building(center_x, center_y, color):
    dx = int(random.gauss(0, 8))
    dy = int(random.gauss(0, 8))
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
    global NUM_HOUSES, village_money,NUM_WORK
    if village_money < 10:
        add_notification("Pas assez d'argent")
        return
    houses.append(generate_building(*VILLAGE_CENTER, (65, 71, 145)))
    NUM_HOUSES += 1
    village_money -= 10
    NUM_WORK = NUM_WORK + (random.randint(2,4))
    add_notification("Maison construite")

def buy_factory():
    global NUM_FACTORIES, village_money
    if village_money < 100:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (196, 71, 71)))
    NUM_FACTORIES += 1
    village_money -= 100
    add_notification("Factory construite")

def buy_hlm():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy,NUM_WORK
    if village_money < 95:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (71, 181, 196)))
    NUM_HLM += 1
    village_money -= 95
    NUM_HOUSES += 10
    villagers_happy -= 1
    NUM_WORK = NUM_WORK + (random.randint(20,40))
    add_notification("HLM construit")

def buy_parc():
    global NUM_PARC, village_money, villagers_happy
    if village_money < 70:
        add_notification("Pas assez d'argent")
        return
    NUM_PARC += 1
    villagers_happy += 4
    village_money -= 70
    factories.append(generate_building(*VILLAGE_CENTER, (68, 194, 106)))
    add_notification("Parc construit")

def buy_circus():
    global NUM_CIRCUS,village_money
    if village_money < 150:
        add_notification("Pas assez d'argent")
        return
    NUM_CIRCUS += 1
    village_money -= 150
    factories.append(generate_building(*VILLAGE_CENTER,(224, 164, 167)))
    add_notification("Cirque construit")

def buy_raf():
    global NUM_RAF,village_money
    if village_money < 180:
        add_notification("Pas assez d'argent")
        return
    if polution == True:
        NUM_RAF += 1
        village_money -= 180
        factories.append(generate_building(*VILLAGE_CENTER,(173, 131, 106)))
        add_notification("Rafinerie construite")
    else:
        add_notification("Cette entreprise est beaucoup trop poluante")
        return
def buy_bank():
    global NUM_BANK,village_money
    if village_money < 200:
        add_notification("Pas assez d'argent")
        return
    NUM_BANK+=1
    village_money -= 200
    factories.append(generate_building(*VILLAGE_CENTER,(51, 130, 101)))
    add_notification("Banque construite")
def buy_sfactory():
        global NUM_FACTORIES, village_money, villagers_happy
        if village_money < 500:
            add_notification("Pas assez d argent")
            return
        NUM_FACTORIES += 10
        villagers_happy -= 3
        village_money=village_money - 500
        factories.append(generate_building(*VILLAGE_CENTER,(130, 51, 55)))


def buy_building():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy,NUM_WORK
    if village_money < 600:
        add_notification("Pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (51, 54, 130)))
    NUM_HLM += 1
    village_money -= 600
    NUM_HOUSES += 100
    villagers_happy -= 1
    NUM_WORK = NUM_WORK + (random.randint(200,400))
    add_notification("Building construit")

def buy_generator():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy,NUM_WORK,NUM_GENERATOR
    if village_money < 50:
        add_notification("pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (225, 227, 93)))
    
    village_money=village_money-50
    NUM_GENERATOR+=1
    add_notification("Building construit")

    
def buy_capacitor():
    global NUM_HLM, village_money, NUM_HOUSES, villagers_happy,NUM_WORK,max_electricity
    if village_money < 70:
        add_notification("pas assez d'argent")
        return
    factories.append(generate_building(*VILLAGE_CENTER, (91, 222, 176)))
    
    village_money=village_money-70
    max_electricity = max_electricity + 50
    add_notification("Building construit")

    


#fonction pour choisir son parti politique
party = None
def polp_chose():
    global parti_actuel

    def set_parti(name):
        global parti_actuel
        party=name

    
    
    
    polp_chose_window = Toplevel(window)  # 👈 IMPORTANT
    polp_chose_window.geometry("300x200")
    polp_chose_window.title("Politique")
    
    
    
    Label(polp_chose_window, text="Choix politique").pack()
    Button(polp_chose_window, text="Parti communiste",command=lambda: set_parti("pc")).pack()
    Button(polp_chose_window, text="Parti socialiste",command=lambda: set_parti("ps")).pack()
    Button(polp_chose_window, text="Parti ecologiste",command=lambda: set_parti("pe")).pack()
    Button(polp_chose_window, text="Parti Cente",command=lambda: set_parti("pce")).pack()
    Button(polp_chose_window, text="Parti libertarien",command=lambda: set_parti("pl")).pack()
    Button(polp_chose_window, text="Parti nationaliste",command=lambda: set_parti("pn")).pack()
    
# -------------------------
# BOUTONS SCROLLABLE
# -------------------------
Label(scrollable_frame, text="").pack()
Label(scrollable_frame, text="-Politique-").pack()

spin_value = IntVar()

spin = Spinbox(scrollable_frame, from_=0, to=50, textvariable=spin_value)
spin.pack()
Button(scrollable_frame, text="Choisis ton bord politique", command=polp_chose).pack()





Label(scrollable_frame, text="-Infrastructure-").pack()
Label(scrollable_frame, text="").pack()
Button(scrollable_frame, text="Acheter maison $10", command=buy_house).pack()
Label(scrollable_frame, text="Main d'oeuvre").pack()
Button(scrollable_frame, text="Acheter generateur $50", command=buy_generator).pack()
Label(scrollable_frame, text="+5 electricity/s").pack()
Button(scrollable_frame, text="Acheter capacitor $70", command=buy_capacitor).pack()
Label(scrollable_frame, text="+5 electricity/s").pack()
Button(scrollable_frame, text="Acheter parc $70", command=buy_parc).pack()
Label(scrollable_frame, text="+ bonheur").pack()
Button(scrollable_frame, text="Acheter HLM $90", command=buy_hlm).pack()
Label(scrollable_frame, text="+10 maisons mais - bonheur").pack()
Button(scrollable_frame, text="Acheter factory $100", command=buy_factory).pack()
Label(scrollable_frame, text="Produit de l'argent").pack()
Button(scrollable_frame, text="Acheter Cirque $150", command=buy_circus).pack()
Label(scrollable_frame, text="bonus bonheur").pack()
Button(scrollable_frame, text="Rafinerie $180", command=buy_raf).pack()
Label(scrollable_frame, text="- bonheur + argent").pack()
Button(scrollable_frame, text="Banque $200", command=buy_bank).pack()
Label(scrollable_frame, text="revenu aléatoire").pack()
Button(scrollable_frame, text="super factory $500", command= buy_sfactory).pack()
Label(scrollable_frame, text="super factory pr produire de l argent -5 happiness")
Button(scrollable_frame, text="buy building $600", command=buy_building).pack()
Button(scrollable_frame, text="Infos", command=building_info).pack()


# -------------------------
# MAP INIT
# -------------------------53, 135, 63




pixel_map = generate_map()

textures = [generate_building(*VILLAGE_CENTER, (70, 153, 80)) for _ in range(NUM_HOUSES *10 )]

houses = [generate_building(*VILLAGE_CENTER, (65, 71, 145)) for _ in range(NUM_HOUSES)]
factories = [generate_building(*VILLAGE_CENTER, (196, 71, 71)) for _ in range(NUM_FACTORIES)]



a_numelec=0
while a_numelec !=NUM_GENERATOR:
    factories.append(generate_building(*VILLAGE_CENTER, (225, 227, 93)))
    a_numelec=a_numelec+1



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


#mettre la worforce
i_workforce=0
while i_workforce != NUM_HOUSES:
    NUM_WORK = NUM_WORK + random.randint(2,4)
    i_workforce+=1



# -------------------------
# GAME LOOP
# -------------------------

while running:
    villagers_happy_requirement=50
    advantage=1
    industrial_bonus=1
    if party == "pc":
        villagers_happy_requirement = 45
        advantage=1.5
        industrial_bonus = 0.75
        
    if party == "ps":
        villagers_happy_requirement=55
        industrial_bonus = 0.90
        
    if party == "pe":
        industrial_bonus = 0.60
        villagers_happy_requirement = 45
        
    if party == "pce":
        pass
    
    if party == "pl":
        villagers_happy_requirement=55
        industrial_bonus = 1.5
        
    if party == "pn":
        villagers_happy_requirement=60
        industrial_bonus = 1.1
        
    for event in pygame.event.get():

    
        if village_money < 0:
            
            print("plus d argent")
            quit()
        if villagers_happy < villagers_happy_requirement:
            
            print("plus content")
            NUM_WORK -= random.randint(villagers_happy , villagers_happy*2)

        if event.type == pygame.QUIT:
            running = False

        elif event.type == TWO_SEC_EVENT:
            event_taxes+=1
            event_circus+=1
            event_bank+=1
            malus=(NUM_BANK*5+NUM_PARC*3 + NUM_RAF*3 + NUM_CIRCUS*3) +villagers_happy//10 +NUM_HOUSES//200

            if event_taxes==10:
                imposition = spin_value.get()
                if imposition > 0:
                    print(imposition)
                    imposition = 100 / imposition
                
                    village_money = ((village_money+((NUM_HOUSES//5) * imposition)*advantage)//1)
                    villagers_happy = villagers_happy - ((((3* (imposition*2)))//advantage))
                event_taxes=0
                if malus > 0:
                    village_money -= malus
                    add_notification(f"malus - {malus}",duration=2000)
                if villagers_happy > 80:
                    NUM_HOUSES += 1
            if event_circus==5:
                if electricity > 0:
                    villagers_happy += 2 * NUM_CIRCUS
                    villagers_happy -= (5 * NUM_RAF) * industrial_bonus
                    village_money += 15 * NUM_RAF
                event_circus=0
                #generation d electricité
                
                
                temp_electricity = electricity + NUM_GENERATOR * 5
                electricity_debt = int((NUM_FACTORIES * 1.5 + NUM_RAF * 2.5 + NUM_CIRCUS*2)//1)
                if (temp_electricity-electricity_debt) > max_electricity: 
                    electricity = max_electricity
                else:
                    electricity=temp_electricity
                    electricity=electricity-electricity_debt
                
                

            if event_bank==15:
                village_money += random.randint(-20,20)*NUM_BANK
                event_bank=0

            village_money = factories_money(NUM_FACTORIES, NUM_HOUSES, village_money)

    
    screen.fill((0,0,0))  # fond

    # Afficher la map + bâtiments
    draw_map(pixel_map, textures + factories + houses)

    # Afficher texte
    money_text = font.render(f"$ : {village_money}", True, (255,255,255))
    happiness_text = font.render(f":) : {villagers_happy}", True, (255,255,255))
    #population_text = font.render(f" : {NUM_HOUSES}", True, (255,255,255))
    factories_text = font.render (f"Usines : {NUM_FACTORIES}", True, (255,255,255))
    workforce_text = font.render (f"Pop  : {NUM_WORK}", True, (255,255,255))
    electricity_text = font.render (f"E : {electricity}", True, (255,255,255))
    screen.blit(money_text, (WIDTH - 200, HEIGHT - 40))
    screen.blit(happiness_text, (WIDTH - 200, HEIGHT - 80))
    screen.blit(workforce_text, (WIDTH - 200, HEIGHT - 120))
    #screen.blit(population_text, (WIDTH - 200, HEIGHT - 160))
    screen.blit(factories_text, (WIDTH - 200, HEIGHT - 160))
    screen.blit(electricity_text, (WIDTH - 200, HEIGHT - 200))
    
    
    draw_notifications()
    
    pygame.display.flip()
    window.update()
    clock.tick(60)

pygame.quit()
