import pygame
import os   # Helps me see how many files are in a folder

pygame.init()

# Game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Title
pygame.display.set_caption('Shooter')

# Set frame rate
clock = pygame.time.Clock() 
FPS = 60

# Game variables
GRAVITY = 0.75         # Capital becuase I don't want it to change, constant variable


# define player action variables
moving_left = False
moving_right = False

# Define colours
BG = (144, 201, 120)  # RGB values
RED = (255, 0, 0)

def draw_bg():          # over rides anything that leaves a trail
    screen.fill(BG)   
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        # Inheret functionality from the sprite class
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1  # 1 means looking right, -1 means looking left
        self.vel_y = 0      # y velocity for jump
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0   # 0- IDEL, 1- RUN
        self.update_time = pygame.time.get_ticks()
        
        # Load all images for the players
        animation_types = ['Idle', 'Run', 'Jump']
        
        for animation in animation_types:
            # Reset temporary list of images
            temp_list = []
            # Count number of files in folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):      
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                # Scale Image
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        # Create boundary box
        self.rect = self.image.get_rect()
        # Position rect
        self.rect.center = (x, y)
    
    def move(self, moving_left, moving_right):
        # Reset movement varriables
        dx = 0  # change in x (delta)
        dy = 0  # change in y (delta)

        # Assign movement varriables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        
        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11   # How high player jumps
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()   # reset the timer
            self.frame_index += 1
        # If animation runs out, reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# create instance of player
player = Soldier('player', 200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 5)

run = True
while run: 

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    enemy.draw()

    # Update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)        # 2: JUMP
        elif moving_left or moving_right:
            player.update_action(1)        # 1: RUN
        else:
            player.update_action(0)        # 0: Idle
    player.move(moving_left, moving_right)



    for event in pygame.event.get():  # Gives all the events that are happening
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        # Keyboard Presses
        if event.type == pygame.KEYDOWN:    # means that you have pressed a key on the keyboard
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
        # Keyboard released
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_ESCAPE:        # close game
                run = False


    # Update game window
    pygame.display.update()

pygame.quit()


