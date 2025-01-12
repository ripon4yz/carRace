import pygame
import random

pygame.init()

# Screen dimensions
dis_width = 800
dis_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Car Racing")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Car properties
car_width = 50
car_height = 80
car_speed = 10

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)

# Game variables
x1 = dis_width / 2 - car_width / 2
y1 = dis_height - car_height - 10
x1_change = 0

# Function to display text
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Function to draw the car
def car(x, y):
    pygame.draw.rect(dis, blue, [x, y, car_width, car_height])

# Main game loop
def gameLoop():
    global x1, y1, x1_change

    game_over = False

    # Obstacles
    obstacles = []
    obstacle_speed = 7
    obstacle_width = 50
    obstacle_height = 80
    spawn_rate = 30

    def spawn_obstacle():
        x = random.randrange(100, dis_width - 100)
        y = -obstacle_height
        obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -car_speed
                elif event.key == pygame.K_RIGHT:
                    x1_change = car_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x1_change = 0

        x1 += x1_change

        # Prevent the car from going off the screen
        if x1 > dis_width - car_width:
            x1 = dis_width - car_width
        if x1 < 0:
            x1 = 0

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > dis_height:
                obstacles.remove(obstacle)

        # Collision detection
        for obstacle in obstacles:
            if pygame.Rect(x1, y1, car_width, car_height).colliderect(obstacle):
                message("You Crashed! Press Q-Quit or C-Play Again", red)
                pygame.display.update()

                # Wait for user input to quit or restart
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = True
                                break
                            elif event.key == pygame.K_c:
                                gameLoop()
                    if game_over:
                        break

        # Spawn new obstacles
        if random.randint(1, spawn_rate) == 1:
            spawn_obstacle()

        # Draw everything
        dis.fill(white)
        car(x1, y1)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(dis, red, obstacle)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()
    quit()

# Run the game
gameLoop()
