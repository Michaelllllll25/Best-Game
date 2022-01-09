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
shoot = False

# Load Images
# Bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# Define colours
BG = (144, 201, 120)  # RGB values
RED = (255, 0, 0)

def draw_bg():          # over rides anything that leaves a trail
    screen.fill(BG)   
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        # Inheret functionality from the sprite class
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
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
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:   # for loop will iterate through list ^
            # Reset temporary list of images
            temp_list = []
            # Count number of files in folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):      
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                # Scale Image
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        # Create boundary box
        self.rect = self.image.get_rect()
        # Position rect
        self.rect.center = (x, y)
    
    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
        
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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else: 
                self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                print(enemy.health)
                self.kill()

# Create sprite groups
bullet_group = pygame.sprite.Group()



# create instance of player
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)

run = True
while run: 

    clock.tick(FPS)
    
    draw_bg() 

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    # Update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)


    # Update player actions
    if player.alive:
        # Shoot bullets
        if shoot:
            player.shoot()
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
            if event.key == pygame.K_SPACE:
                shoot = True                
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:        # close game
                run = False
        # Keyboard released
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False   


    # Update game window
    pygame.display.update()

pygame.quit()


