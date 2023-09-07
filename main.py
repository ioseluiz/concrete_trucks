import pygame
from datetime import datetime, timedelta

from utils import check_batch_time, check_trip_ended
# Initialize pygame
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Batch Plant


# Destination Lift - Equipment
EQUIPMENT = 1
if EQUIPMENT == 1:
    placing_equipment = [
        {
            'id':1,
            'name': 'Telebelt 01',
            'x': 550,
            'y': 250,
        }
    ]
    path = [(120,250),(350, 250),(530,250)]
elif EQUIPMENT == 2:
    placing_equipment = [
        {
            'id':1,
            'name': 'Telebelt 01',
            'x': 550,
            'y': 50,
        },
        {
            'id':2,
            'name': 'Telebelt 02',
            'x': 550,
            'y': 550,
        },

    ]
    #path = [(120,270),(350, 270),(),(530,270)]
elif EQUIPMENT == 3:
    placing_equipment = [
        {
            'id':1,
            'name': 'Telebelt 01',
            'x': 550,
            'y': 50,
        },
        {
            'id':2,
            'name': 'Telebelt 02',
            'x': 550,
            'y': 250,
        },
        {
            'id':3,
            'name': 'Telebelt 03',
            'x': 550,
            'y': 550,
        },

    ]



# Truck DATA
truck_trips = [
    {
        'id': 1,
        'second_batch_datetime': datetime(2013,11,14,6,29),
        'arrive_time': datetime(2013,11,14,6,37),
        'start_time': datetime(2013,11,14,6,39),
        'finish_time': datetime(2013,11,14,6,40),
    },
    {
    'id': 2,
        'second_batch_datetime': datetime(2013,11,14,6,33),
        'arrive_time': datetime(2013,11,14,6,40),
        'start_time': datetime(2013,11,14,6,44),
        'finish_time': datetime(2013,11,14,6,49),
    },

]

# Date information
start_datetime = datetime(2013,11,14,6,27)
end_datetime = datetime(2013,11,14,6,55)
duration = end_datetime - start_datetime
duration = duration.total_seconds() // 60
actual_datetime = start_datetime 

# System Font
system_font = pygame.font.SysFont("calibri", 34)

#Window Size
WINDOW_WIDTH = 600
WINDOW_HEIGTH = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
pygame.display.set_caption("Concrete Truck Simulation")

FPS = 1
clock = pygame.time.Clock()
t = 0
started_trips = []

# Define classes
class Truck(pygame.sprite.Sprite):
    """A simple class to represent a Concrete Truck"""
    def __init__(self, id,x, y):
        super().__init__()
        self.id = id
        self.image = pygame.image.load("truck.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.speed_x = 0
        self.speed_y = 0 

    def update(self, speed_x, speed_y):
        "Update and move the truck"
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x += self.speed_x
        self.y += self.speed_y

class Equipment():
    """A simple class to represent concrete placement equipment"""
    def __init__(self, id,name,x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y

class Plant():
    """A simple class to represent Main Batch Plant"""
    def __init__(self, id, name,x,y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        

# Game Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create Text
    system_text = system_font.render(f"DATE: {actual_datetime}", True, BLACK)
    system_text_rect  = system_text.get_rect()
    system_text_rect.topleft = (0,0)

    # Fill the display surface to cover old images
    display_surface.fill(WHITE)

    # Check batch time to create trucks
    started_trips += check_batch_time(truck_trips, actual_datetime)
    check_trip_ended(started_trips, actual_datetime)
    print(started_trips)
   

    # Instantiate Batch Plant class
    plant = Plant(1, 'Main Batch Plant', 50, 250)
    pygame.draw.rect(display_surface, RED, (plant.x, plant.y, 40,40))

    # Instantiate equipment class
    for equip in placing_equipment:
        telebelt = Equipment(equip['id'], equip['name'], equip['x'], equip['y'])
        pygame.draw.rect(display_surface, BLUE,(telebelt.x,telebelt.y, 40,40))

    # Blit assets
    display_surface.blit(system_text, system_text_rect)

    if len(started_trips) > 0:
        for trip in started_trips:
            truck = Truck(trip['id'], path[0][0], path[0][1])
            display_surface.blit(truck.image, truck.rect)

    # Update Screen
    pygame.display.update()

    clock.tick(FPS)
    t += 1
    actual_datetime += timedelta(minutes=1)
    if t > duration:
        break

# End game
pygame.quit()