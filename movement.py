import pygame
from datetime import datetime, timedelta

def calculate_distance(points):
    total_distance = 0
    for i in range(1,len(points)):
        total_distance += ((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2)**0.5
    return total_distance

def calculate_times(duration, points ,total_distance):
    times = [0]
    for i in range(1,len(points)):
        distance = ((points[i][0] - points[i-1][0])**2 + (points[i][1] - points[i-1][1])**2)**0.5
        percentage = distance / total_distance
        times.append(percentage * duration)
    return times

def calculate_speed_x(duration, point_1, point_2):
    distance_x = point_2[0] - point_1[0]
    speed_x = distance_x / duration
    return speed_x

def calculate_speed_y(duration,point_1, point_2):
    distance_y = point_2[1] - point_1[1]
    speed_y  = distance_y / duration
    return speed_y

EQUIPMENT = 1

start_date = datetime(2012,10,17,8,23)
end_date = datetime(2012,10,17,8,40)

    
path = [[(100,300),(300,300),(600,300)],#path 1
        [(100,300),(300,300),(300,100),(600,100)], # path 2
        [(100,300),(300,300),(300,500),(600,500)], # path 3
        ]
duration = 10
path_distance = calculate_distance(path)
times = calculate_times(duration, path, path_distance)
print(times)






#Initialize pygame
pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGTH = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
pygame.display.set_caption("Movimiento Programado")
FPS = 1
clock = pygame.time.Clock()

path = [(100,100),(400,100),(400,300)]
start_point = path[0]
end_point = path[1]


truck_image = pygame.image.load("truck.png")
truck_rect = truck_image.get_rect()
truck_rect.topleft = path[0]

t = 0
speed_y = calculate_speed_y(10, path[0], path[1])
speed_x = calculate_speed_x(10, path[0], path[1])
print(speed_x, speed_y)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    truck_rect.x += speed_x
    truck_rect.y -= speed_y

    # Fill the screen
    display_surface.fill((0,0,0))

    # Blit assets
    display_surface.blit(truck_image, truck_rect)

    # Update screen
    pygame.display.update()

    clock.tick(FPS)
    t = t + 1
    print(t)
    print(truck_rect.x)

# End Game
pygame.quit()