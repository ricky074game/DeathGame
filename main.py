import pygame
import platform

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Platformer")
platforms = []
fps = 60

playerx = 400
playery = 400
accelerationy = 0.5
velocityy = 0
accelerationx = 0
velocityx = 0
touch = False


class platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_coords(self):
        return (self.x, self.y)

platforms.append(platform(200, 500, 400, 40))

def player_control():
    global velocityx, playerx, accelerationx, velocityy, playery, accelerationy,touch
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        accelerationx = -0.15
    if keys[pygame.K_d]:
        accelerationx = 0.15
    if keys[pygame.K_SPACE]:
        if touch:
            velocityy = -10
    
    #Moving Control on velocity
    velocityx = velocityx + accelerationx
    playerx = playerx + velocityx
    accelerationx -= 0.05
    event_list = pygame.event.get(pygame.KEYDOWN)
    touch = False
    if len(event_list) == 0:
        if(accelerationx < 0):
            accelerationx = 0

    #Gravity and collision!
    velocityy += accelerationy
    playery += velocityy
    # Collision detection between player and platforms
    for plat in platforms:
        if plat.get_rect().colliderect(pygame.Rect(playerx, playery, 50, 20)):
            # Collision detected, handle it here
            # For example, stop player's vertical movement and adjust player's position
            velocityy = 0
            playery = plat.y - 20
            touch = True
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill((0, 0, 0))
    for plat in platforms:
        plat.draw(screen)
    player_control()
    pygame.draw.circle(screen, (255, 0, 0), (playerx, playery), 20)
    pygame.display.flip()
    pygame.time.Clock().tick(fps)