import pygame
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

from datetime import datetime, timedelta
from classes.truck import Truck
from classes.plant import Plant
from classes.equipment import Equipment
from classes.system_text import SystemText


from utils_2 import calculate_speed
from utils_2 import read_data
from utils_2 import get_unique
from utils_2 import create_trip_list
from utils_2 import get_start_datetime
from utils_2 import get_finish_datetime

# Read csv data
imported_data = read_data('truck_test_data_2.csv')
#print(imported_data)
unique_trucks = get_unique(imported_data, 'truck')
#print(unique_trucks)
unique_equipment = get_unique(imported_data, 'equipment')
#print(unique_equipment)
start_datetime = get_start_datetime(imported_data)
#print(type(start_datetime))
end_datetime = get_finish_datetime(imported_data)

# Plot information
mpl.use("Agg")

#Plot settings
fig = plt.figure(figsize=[4,2])
ax = fig.add_subplot(111)
ax.set_title('Total Volume vs time')
ax.legend()
canvas = agg.FigureCanvasAgg(fig)

# Numpy array for plot
#array_data  = np.array()
plot_volume = []
plot_time = []

#Actual lift
lift = "H4C-4B-F02"

def plot(data):
    
    #print(data)
    ax.plot(data[0],data[1],color='blue')
    ax.set(xlabel='time (min)',ylabel='vol (m3)')
    if max(data[0]) == 0:
        ax.set_xlim(0,5)
    else:
        ax.set_xlim(0,max(data[0])+5)
    if max(data[1]) == 0:
        ax.set_ylim(0,5)
    else:
        ax.set_ylim(0,max(data[1])+5)
    canvas.draw()
    renderer = canvas.get_renderer()

    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()

    return pygame.image.fromstring(raw_data, size, "RGB") 


duration = end_datetime - start_datetime
duration = duration.total_seconds() // 60
actual_datetime = start_datetime 

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


# initialize pygame
pygame.init()

#Window Size
WINDOW_WIDTH = 1000
WINDOW_HEIGTH = 660
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
pygame.display.set_caption("Concrete Truck Simulation")

# System Font
system_font = pygame.font.SysFont("calibri", 34)
system_font_1 = pygame.font.SysFont("calibri",18)
system_font_2 = pygame.font.SysFont("calibri", 12)


FPS = 2
clock = pygame.time.Clock()
t = 0

simulation_state = "start_menu"

def draw_start_menu():
    display_surface.fill((0,0,0))
    font_title = pygame.font.SysFont('arial',40)
    title = font_title.render("Concrete Truck Simulation", True,(255,255,255))
    start_button = font_title.render("Start",True,(255,255,255))
    display_surface.blit(title,(WINDOW_WIDTH/2-title.get_width()/2,
                                WINDOW_HEIGTH/2-title.get_height()/2))
    display_surface.blit(start_button,(WINDOW_WIDTH/2-start_button.get_width()/2,
                                       WINDOW_HEIGTH/2+start_button.get_height()/2))
    pygame.display.update()

# Main Batch Plant
main_batch_plant = Plant(1,'main_plant',36,320)

#List of text for render in screen
text_render = []

# Placing Equipment
equipment_info = []
equipment_counter = 0
equipment_start_y = 320
for unique in unique_equipment:
    equipment_info.append(Equipment(equipment_counter, unique, 836,equipment_counter*160+equipment_start_y))
    equipment_counter += 1
#telebelt_1 = Equipment(1,unique_equipment,860,320)

# Total concrete volume
total_volume = 0

#Instantiate unique trucks and their text name
trucks_info = []
for unique in unique_trucks:
    trucks_info.append(Truck(unique,"truck.png",system_font_2, BLACK))

#print(trucks_info)
#set truck image in all trucks
# for truck in trucks_info:
#     #truck.set_image("truck.png")
#     truck.set_system_font(SystemText(system_font_2,truck.id,BLUE,True,(0,0)))
# container for truck pouring concrete
truck_in_equipment_dict = {}
truck_in_equipment = []
# Waiting trucks is dict with several placing equipment
waiting_trucks_dict = {}
for equip in unique_equipment:
    waiting_trucks_dict[equip] = []
    truck_in_equipment_dict[equip] = []

waiting_trucks = []

trips_info = create_trip_list(imported_data, trucks_info,equipment_info)

#check_truck_delivering = lambda : f"Truck No.{truck_in_equipment[0].id}" if len(truck_in_equipment)>0 else ""
check_truck_delivering = lambda equip: f"Truck No.{truck_in_equipment_dict[equip][0].id}" if len(truck_in_equipment_dict[equip])>0 else ""


# Game Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if simulation_state == "start_menu":
        draw_start_menu()

    if simulation_state == "start_menu":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            simulation_state="simulation"

    if simulation_state == "simulation":


        # Create Text: Actual Datetime
        system_text = SystemText(system_font,f"DATE: {actual_datetime}",BLACK,True,(10,0))
        text_render.append(system_text)

        # Create Text: Duration
        system_text_duration = SystemText(system_font_1, f"DURATION: {round(t/60,2)} hours", BLACK,True,(250,40))
        text_render.append(system_text_duration)

        # Create Text: Lift
        system_text_lift = SystemText(system_font_1,f"Lift: {lift}",BLACK,True,(10,40))
        text_render.append(system_text_lift)

        # Create Text: concrete truck placing concrete
        counter_placing_equip = 0
        for equipment in equipment_info:
            text_render.append(SystemText(system_font_1,f"{equipment.name}: {check_truck_delivering(equipment.name)}",BLACK,True,(10 + counter_placing_equip*250,60)))
            counter_placing_equip += 1

        # Total Volume Text
        system_text_volume = SystemText(system_font_1,f"Total Volume: {total_volume} m3",BLACK,True,(10,80))
        text_render.append(system_text_volume)

        # Main Batch Plant Text
        system_text_plant = SystemText(system_font_1,"Main Batch Plant",BLACK,True,(10,300))
        text_render.append(system_text_plant)
        counter_placing_equip = 0
        for equipment in equipment_info:
            text_render.append(SystemText(system_font_1,f"{equipment.name}",BLACK,True,(840,300 + 160*counter_placing_equip)))
            counter_placing_equip += 1

        # Fill the display surface to cover old images
        display_surface.fill(WHITE)
        # Draw Batch Plant
        pygame.draw.rect(display_surface, GREEN, (main_batch_plant.x, main_batch_plant.y, 64,40))
        # Draw Placing Equipment 
        for equipment in equipment_info:
            #print(equipment.y)
            if len(truck_in_equipment_dict[equipment.name]) > 0:
                pygame.draw.rect(display_surface, RED, (equipment.x, equipment.y, 64,40))
            else:
                pygame.draw.rect(display_surface, BLUE, (equipment.x, equipment.y, 64,40))

        #Check times for events
        for trip in trips_info:
            
            if actual_datetime == trip.batch_time_1:
                # Set truck destination
                trip.truck.set_destination(trip.equipment.name)
                #Update truck status
                trip.truck.set_status('batch_plant')
                # Update truck position
                trip.truck.set_pos_x(100)

                trip.truck.set_pos_y(trip.equipment.y + 55)
            
                
                #print(f"Truck No.{trip['truck'].id}: {trip['truck'].speed_x} {trip['truck'].status}")

            if actual_datetime == trip.batch_time_2:
                trip.truck.set_status('traveling')
                #Update truck speed
                trip.truck.set_speed_x(calculate_speed(trip.batch_time_2,36,trip.arrive_time,836))
                trip.truck.set_speed_y(calculate_speed(trip.batch_time_2,400,trip.arrive_time,400))
                
                #print(f"Truck No.{trip['truck'].id}: {trip['truck'].speed_x} {trip['truck'].status}")
            if actual_datetime == trip.arrive_time:
                trip.truck.set_status('on_site')
                trip.truck.set_speed_x(0)
                trip.truck.set_speed_y(0)
                trip.equipment.add_waiting_truck(trip.truck)
                waiting_trucks_dict[trip.equipment.name].append(trip.truck)
                #print(f"Truck No.{trip['truck'].id}: {trip['truck'].speed_x} {trip['truck'].status}")
            if actual_datetime == trip.start_time:
                if trip.truck in waiting_trucks_dict[trip.equipment.name]:
                    waiting_trucks_dict[trip.equipment.name].remove(trip.truck)
                    trip.equipment.remove_waiting_truck(trip.truck)
                truck_in_equipment_dict[trip.equipment.name].append(trip.truck)
                trip.truck.set_status('started')
                trip.truck.set_speed_x(0)
                trip.truck.set_speed_y(0)
                
                
                #print(f"Truck No.{trip['truck'].id}: {trip['truck'].speed_x} {trip['truck'].status}")
            if actual_datetime == trip.end_time:
                # Update truck status
                truck_in_equipment_dict[trip.equipment.name].remove(trip.truck)
                trip.truck.set_status('inactive')
                # Update truck position
                trip.truck.set_pos_x(-100)
                trip.truck.set_pos_y(trip.equipment.y + 55)
                trip.truck.set_speed_x(0)
                trip.truck.set_speed_y(0)
                
                # Add truck volume to truck total volume
                trip.truck.set_volume(trip.volume)
                total_volume += trip.truck.volume
                #print(f"Truck No.{trip['truck'].id}: {trip['truck'].speed_x} {trip['truck'].status}")
        plot_time.append(t)
        plot_volume.append(total_volume)
        array_data = np.array([plot_time, plot_volume])
        surf = plot(array_data)
        surf_rect = surf.get_rect()
        surf_rect.topright = (1000,0)

        for truck in trucks_info:
            if truck.status != 'inactive':
                truck.add_text_to_render_list(text_render)
            else:
                truck.remove_text_to_render_list(text_render)

        # Blit assets
        # Blit text
        for text in text_render:
            display_surface.blit(text.get_system_text(),text.get_text_pos())
        # Blit matplotlib figure
        display_surface.blit(surf, surf_rect)
        print(f"Trucks Waiting: {waiting_trucks_dict}")
        for truck in trucks_info:
            print(f"Truck No.{truck.id}: pos_x: {truck.rect.x} and {truck.status}")
        
            if truck.status != 'inactive':
                display_surface.blit(truck.image, truck.rect)
                truck.image.blit(truck.system_font.get_system_text(), truck.rect)
                if (truck.status == 'traveling'):
                    print(truck.speed_x)
                    if len(waiting_trucks_dict[truck.destination]) == 0:
                        
                        truck.set_pos_x(truck.pos_x + truck.speed_x)
                        truck.set_pos_y(truck.pos_y + truck.speed_y)
                        truck.update_rect_pos()
                    else:
                        if truck.pos_x <= (836 - len(waiting_trucks_dict[truck.destination]*64)):
                            difference = (836 - len(waiting_trucks_dict[truck.destination]*64)) - truck.pos_x
                            if difference <= 64:
                            
                                truck.set_pos_x(truck.pos_x + difference)
                                truck.set_pos_y(truck.pos_y + truck.speed_y)
                                truck.update_rect_pos()
                            else:
                                
                                truck.set_pos_x(truck.pos_x + truck.speed_x)
                                truck.set_pos_y(truck.pos_y + truck.speed_y)
                                truck.update_rect_pos()
                        else:
                            truck.set_speed_x(0)
                            truck.set_speed_y(0)
                            truck.update_rect_pos()
                            truck.set_pos_x(truck.pos_x + truck.speed_x)
                            truck.set_pos_y(truck.pos_y + truck.speed_y)

                if (truck.status == 'onsite'):
                    if truck.pos_x <= (836 - len(waiting_trucks_dict[truck.destination]*64)):
                            difference = (836 - len(waiting_trucks_dict[truck.destination]*64)) - truck.pos_x
                            if difference <= 64:
                            
                                truck.set_pos_x(truck.pos_x + difference)
                                truck.set_pos_y(truck.pos_y + truck.speed_y)
                                truck.update_rect_pos()
                    
                if (truck.status == 'started'):
                    truck.set_pos_x(900)
                    #truck.set_pos_y(400)
                    truck.update_rect_pos()
                    

                if truck.status == 'batch_plant':
                    truck.set_pos_x(100)
                    #truck.set_pos_y(400)
                    truck.update_rect_pos()
                    

            else:
                truck.set_pos_x(-100)
                truck.update_rect_pos()
            
            

        # Update Screen
        pygame.display.update()
        text_render = []

        clock.tick(FPS)
        t += 1
        actual_datetime += timedelta(minutes=1)
        if t > duration + 10:
            break

# End game
pygame.quit()




