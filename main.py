import random
import pygame
import win32gui, win32con
from pygame._sdl2 import Window, Texture, Image, Renderer, get_drivers, messagebox

pygame.display.set_caption("Platformer")
platforms = []
fps = 60

playerx = 100
playery = 100
accelerationy = 0.5
velocityy = 0
accelerationx = 0
velocityx = 0
touch = False
right = True
num_plat = 0
num_plif = 0

screen = pygame.display.set_mode((600 + velocityx, 600 + velocityy))

class platform:
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        renderer = Renderer(self.window)
        renderer.clear()
        renderer.present()
        renderer.draw_color = (0, 0, 0, 255)
        renderer.draw_color = (255,255,255,255)
        renderer.fill_rect((50, 100, self.width, self.height))
        renderer.present()
        platform_window = win32gui.FindWindow(None, "Platform " + str(num_plif))
        win32gui.SetWindowPos(platform_window, win32con.HWND_TOPMOST, self.x + 50, self.y + 60, 150, 150, 0)
        win32gui.SetForegroundWindow(platform_window)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_coords(self):
        return (self.x, self.y)
    def get_window(self):
        return self.window
    
    def destroy(self):
        self.window.destroy()

platform_window = Window("Platform " + str(num_plif), size=(200, 200), always_on_top=True)
platforms.append(platform(0, 500, 100, 20, window=platform_window))
num_plif += 1

hwnd = win32gui.FindWindow(None, "Platformer") 

def player_control():
    global velocityx, playerx, accelerationx, velocityy, playery, accelerationy,touch, right, num_plat, num_plif 
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
    
    if len(event_list) == 0:
        accelerationx = 0
        if(touch):
            velocityx /= 1.0
    touch = False
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
            #If the player touch the last platform, reset the platforms except the last one, and generate a new one leftwards
            if plat == platforms[-1]:
                if(num_plat > 3):
                    if(right):
                        right = False
                    else:
                        right = True
                if(right):
                    generate_platforms(True)
                    platforms[0].destroy()
                    platforms.pop(0)
                    num_plat += 1
                else:
                    generate_platforms(False)
                    platforms.pop(0)
                    num_plat += 1
       
        
    #Check "death"
    if playery > 600 or playerx > 1920 or playerx < 0:
        playerx = 0
        playery = 0
        velocityy = 0
        velocityx = 0
        accelerationx = 0
        touch = False

def generate_platforms(right):
    global platforms, num_plif, num_plat
    lastx = 0
    lasty = 0
    if(right):
        lastx = platforms[-1].get_coords()[0]
        lasty = platforms[-1].get_coords()[1]
        randomx = random.randint(100, 400)
        randomy = random.randint(-100, 100)
        if(lasty + randomy > 600):
            randomy = 0
        platform_window = Window("Platform " + str(num_plif), size=(200, 200), always_on_top=True)
        platforms.append(platform(lastx + randomx, lasty + randomy, 100, 20, window=platform_window))
        num_plif += 1
        num_plat += 1
        return
    else:
        lastx = platforms[-1].get_coords()[0]
        lasty = platforms[-1].get_coords()[1]
        randomx = random.randint(100, 400)
        randomy = random.randint(-100, 100)
        if(lasty + randomy > 600):
            randomy = 0
        platform_window = Window("Platform " + str(num_plif), size=(200, 200), always_on_top=True)
        platforms.append(platform(lastx + randomx, lasty + randomy, 100, 20, window=platform_window))
        num_plif += 1
        num_plat += 1
        return

                

generate_platforms(True)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        for plat in platforms:
            if getattr(event, 'window', None) == plat.get_window():
                if(
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.WINDOWCLOSE
                ):
                    platforms.remove(plat)
    screen.fill((0, 0, 0))
    player_control()
    pygame.draw.circle(screen, (255, 0, 0), (300, 300), 20)
    pygame.display.flip()
    hwnd = win32gui.FindWindow(None, "Platformer")
    win32gui.MoveWindow(hwnd, int(playerx - 150), int(playery - 150), 300, 300, True)
    pygame.time.Clock().tick(fps)