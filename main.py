import pygame
import random
import os   # Helps me see how many files are in a folder
import csv   # backgrounds
import button
import button_potion
import json

pygame.init()

profile = {
    "Name": "",
    "Last name": "",
    "Username": "",
    "High score": 0
}

# Game window
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8 + BOTTOM_PANEL
# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Title
pygame.display.set_caption('Shooter')

# Set frame rate
clock = pygame.time.Clock() 
FPS = 60

# Game variables
GRAVITY = 0.75         # Capital becuase I don't want it to change, constant variable
SCROLL_THRESH = 200    # distace player get to end of screen before it starts to scroll
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 25
MAX_LEVELS = 2
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
potion = False
potion_effect = 25
score = 0

# define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Load Images
# Button images
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
restart_img = pygame.image.load('restart_btn.png').convert_alpha()

# Background images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# Load potion
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()

# Load Panel
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))   # both ar TILE_SIZE because it is a square tile
    img_list.append(img)

# Bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# Grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

#Pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()

# Pick up coins
gold_img = pygame.image.load('img/icons/gold.png').convert_alpha()
silver_img = pygame.image.load('img/icons/silver.png').convert_alpha()
bronze_img = pygame.image.load('img/icons/bronze.png').convert_alpha()

item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      : ammo_box_img,
    'Grenade'   : grenade_box_img
}

coins = {
    'Gold'      : gold_img,
    'Silver'      : silver_img,
    'Bronze'      : bronze_img
}

c = {
    'gold': 1,
    'silver': 2,
    'bronze': 3
}
GOLD = 1
SILVER = 2
BRONZE = 3
coins_collected = []

# Define colours
BG = (144, 201, 120)  # RGB values
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.SysFont('Futura', 30)

def sort(coins_collected):
    indexing_length = len(coins_collected) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(0, indexing_length):
            if coins_collected[i] > coins_collected[i+1]:   # if item in list is greater than item to it's right
                sorted = False
                coins_collected[i], coins_collected[i+1] = coins_collected[i+1], coins_collected[i]
                
    print()
    print("Sorted Medals:")
    return coins_collected
 

def draw_text(text: str, font: str, text_col: str, x: int, y: int) -> None:
    """Renders the fonts on screen
    Args:
        text: text being drawn on screen
        font: font of text
        text_col: colour of text
        x: x corordinate
        y: y corordinate
    Returns:
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg() -> None:          # over rides anything that leaves a trail
    """Draws a background to over ride any trails left by player"""
    screen.fill(BG) 
    width = sky_img.get_width()  
    # pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
    for x in range(5):    # re-prints background for when scroll
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_panel():   #
	#draw panel rectangle
	screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))

def draw_gold():
	screen.blit(gold_img, (150, 680))

def draw_silver():
	screen.blit(silver_img, (210, 680))

def draw_bronze():
	screen.blit(bronze_img, (270, 680))

# Function to reset level
def reset_level() -> list:
    """Resets all groups once player is dead
    Args:
        None
    Returns:
        A list of data 
    """
    
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    coin_box_group.empty()
    coins_collected_group.empty()
    mini_coin_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    
    return data

class Profile():
    def __init__(self, name, last_name, username):
        self._name = name
        self._last_name = last_name
        self._username = username

    def __str__(self) -> str:
            return f"Hello {self._name} {self._last_name} aka {self._username}"

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        if len(name) > 50:
            raise ValueError("Names can't exceed 50 characters")
        self._name = name

    def get_last_name(self) -> int:
        return self._last_name

    def set_last_name(self, last_name: str) -> None:
        if last_name > 50:
            raise ValueError("Must be positive")
        self._last_name = last_name

    def get_username(self) -> int:
        return self._contents

    def set_username(self, username: int) -> None:
        if username > self._username:
            raise ValueError("Names can't exceed 50 characters")
        elif username < 1:
            raise ValueError("Names must be greater than 1 characters")
        self._username = username

leader_board_username = []
leader_board_highscore = []

with open("accounts.json", "r") as f:
    profs = json.load(f)

    for user in profs:
        leader_board_username.append(user['Username'])
        leader_board_highscore.append(user['High score'])
        
print()
print("Usernames: ", leader_board_username)
print("Scores: ", leader_board_highscore)


def sort_leaderboard(leader_board_highscore):
    indexing_length = len(leader_board_highscore) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(0, indexing_length):
            if leader_board_highscore[i] > leader_board_highscore[i+1]:   # if item in list is greater than item to it's right
                sorted = False
                leader_board_highscore[i], leader_board_highscore[i+1] = leader_board_highscore[i+1], leader_board_highscore[i]
                
    print()
    return leader_board_highscore

sort_leaderboard(leader_board_highscore)
print("Sorted Scores: ", leader_board_highscore)
print()
print("Leaderboard:")

for i in range(len(profs)):
    if profs[i]['High score'] == leader_board_highscore[-1]:
        print("First:", profs[i]['Username'], "-------->", profs[i]['High score'])
for i in range(len(profs)):
    if profs[i]['High score'] == leader_board_highscore[-2]:
        print("Second:", profs[i]['Username'], "-------->", profs[i]['High score'])
for i in range(len(profs)):
    if profs[i]['High score'] == leader_board_highscore[-3]:
        print("Third:", profs[i]['Username'], "-------->", profs[i]['High score'])
print()



with open("accounts.json", "r") as f:
    profs = json.load(f)


print("[1] Login")
print("[2] Sign-up")
choice = int(input(">>>> "))
if choice == 1:
    user = input("Username: ")
    for i in range(len(profs)):
        if profs[i]['Username'] == user:
            high_score = profs[i]['High score']
            print(f"Current High Score: {high_score}")
        # else:
            # print("False")

elif choice == 2:
    name = input("Name: ")
    profile["Name"] = name
    last_name = input("Last name: ")
    profile["Last name"] = last_name
    username = input("Username: ")
    profile["Username"] = username  
    pp = Profile(name, last_name, username)
    print(pp)
    print(f"Hello {username} and welcome to _________")

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale: int, speed: int, ammo: int, grenades: int, potions: int) -> None:
        # Inheret functionality from the sprite class
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_potions = potions
        self.potions = potions
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
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
        # Ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20) # x, y, w, h   rectangle created as the vision space
        self.idling = False
        self.idling_counter = 0

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self) -> None:
        """Updates player attributes"""
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left: int, moving_right: int) -> int:
        """Determines player's position
        Args:
            moving_left: position if player moved left
            moving_right: position if player moved left
        Returns:
            When screen should scroll and when level is complete
        """
        # Reset movement varriables
        screen_scroll = 0
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

        # Check for collision 
        for tile in world.obstacal_list:
            # Check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if ai has hit wall, make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # Check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below the group, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0 
                    dy = tile[1].bottom - self.rect.top
                # Check if above the ground, i.e. falling 
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Check for colision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            draw_text(f"Coins Collected: {coins_collected}", font, WHITE, 430,  SCREEN_HEIGHT - BOTTOM_PANEL + 30)
            level_complete = True        

        # Check if fell off map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        # Check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                or self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx):
                    self.rect.x -= dx
                    screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self) -> None:
        """Player shooting"""    
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
        
    def ai(self) -> None:
        """Enemy ai"""
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0) #0: Idle
                self.idling = True
                self.idling_counter = 50
            # Check if the ai is near the player
            if self.vision.colliderect(player.rect):
                # Stop running and face player
                self.update_action(0)  # 0: Idle
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right     # always opposite
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1: Run
                    self.move_counter += 1
                    # Update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    # pygame.draw.rect(screen, RED, self.vision)    # draws the rect

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # Scroll
        self.rect.x += screen_scroll

    def update_animation(self) -> None:
        """Updates animations"""
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

    def update_action(self, new_action: int) -> None:
        """Updates actions
        Args:
            new_action: player's action
        Returns:
        """
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self) -> None:
        """Checks if player is alive"""
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self) -> None:
        """Draws soldier"""
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, RED, self.rect, 1)          # draws rect boarder

class World():
    def __init__(self) -> None:
        self.obstacal_list = []

    def draw_gold():
        screen.blit(gold_img, (150, 680))

    def process_data(self, data: list) -> int:
        """Processes the data that loads the world
        Args:
            data: list of items to load into world
        Returns:
            The player and it's health bar
        """
        self.level_length = len(data[0])     #how wide/low level is
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]     # tile is a number that coresponds to particular image in folder
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)    # stores everything about the tile
                    if tile >= 0 and tile <= 8:
                        self.obstacal_list.append(tile_data)      # obstacal list filles with dirt boxes
                    elif tile >= 9 and tile <= 10:  # Water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water) 
                    elif tile >= 11 and tile <= 14: # Decoration
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration) 
                    elif tile == 15:      # Create player
                        # create instance of player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5, 3)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:    # Create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:   #  Create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:   #  Create grenades box
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:   #  Create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:   #  Create Bronze coin
                        coin_box = Coins('Bronze', x * TILE_SIZE, y * TILE_SIZE)
                        coin_box_group.add(coin_box)
                    elif tile == 21:   #  Create Silver coin
                        coin_box = Coins('Silver', x * TILE_SIZE, y * TILE_SIZE)
                        coin_box_group.add(coin_box)
                    elif tile == 22:   #  Create Gold coin
                        coin_box = Coins('Gold', x * TILE_SIZE, y * TILE_SIZE)
                        coin_box_group.add(coin_box)
                    elif tile == 23:   #  Create Gold coin
                        mini_coin = MiniCoin(x * TILE_SIZE, y * TILE_SIZE)
                        mini_coin_group.add(mini_coin)
                    elif tile == 24:   # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit) 
                    
        return player, health_bar

    def draw(self) -> None:
        """Draws obstacals in the world"""
        for tile in self.obstacal_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
#                        img      img_rect

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img: str, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self) -> None:
        """Updates decoration"""
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img: str, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self) -> None:
        """Updates water"""
        self.rect.x += screen_scroll
        
class Exit(pygame.sprite.Sprite):
    def __init__(self, img: int, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self) -> None:
        """Updates exit sign"""
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type: str, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self) -> None:
        """Updates item boxes"""
        # Scroll
        self.rect.x += screen_scroll
        # Check if player has picked up box
        if pygame.sprite.collide_rect(self, player):
            # Check which kind of box was picked up
            if self.item_type == 'Health':
                print(player.health)
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                print(player.health)
            elif self.item_type == 'Ammo':
                print(player.ammo)
                player.ammo += 15
            if self.item_type == 'Grenade':
                player.grenades += 3
            # Delete item box
            self.kill()

class MiniCoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Icons/coin.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)   

    def update(self) -> None:
        """Updates item boxes"""
        # Scroll
        self.rect.x += screen_scroll
        # Check if player has picked up box
        if pygame.sprite.collide_rect(self, player):
            self.kill()

class Coins(pygame.sprite.Sprite):
    def __init__(self, coin_type: str,x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.coin_type = coin_type
        self.image = coins[self.coin_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self) -> None:
        """Updates item boxes"""
        # Scroll
        self.rect.x += screen_scroll
        # Check if player has picked up box
        if pygame.sprite.collide_rect(self, player):
            # Check which kind of box was picked up
            if self.coin_type == 'Bronze':
                coins_collected.append(BRONZE)
                print(sort(coins_collected))
            elif self.coin_type == 'Silver':
                coins_collected.append(SILVER)
                print(sort(coins_collected))
            if self.coin_type == 'Gold':
                coins_collected.append(GOLD)
                print(sort(coins_collected))
            # Delete coin
            self.kill()


  
    def draw(self):
        pygame.draw.rect(screen, gold_img, (self.x - 2, self.y - 2, 154, 22))

class HealthBar():
    def __init__(self, x: int, y: int, health: int, max_health: int) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health: int) -> None:
        """Draws health bar
        Args:
            health: player health
        Returns:
        """
        # Update with new health
        self.health = health
        # Calcuate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))      # Boarder
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self) -> None:
        """Updates bullet"""
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacal_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # Check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    print(enemy.health)
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self) -> None:
        """Updates grenade"""
        self.vel_y += GRAVITY # CHANGE Y VEL VARIABLE
        dx = self.direction * self.speed 
        dy = self.vel_y
        # Check for collision with level
        for tile in world.obstacal_list:
            # Check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1    # Flips
                dx = self.direction * self.speed 
            # Check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # Check if below the group, i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0 
                    dy = tile[1].bottom - self.rect.top
                # Check if above the ground, i.e. falling 
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    
        # Update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        # Count timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # Do damage to anyone nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:    # Blast radius is always 2 tiles across           # abs means absolute value
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:    # Blast radius is always 2 tiles across           # abs means absolute value
                    enemy.health -= 50

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0                        # determine which pic is being shown
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0                     # countdown

    def update(self) -> None:
        """Updates explosion"""
        # Scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # Updtae explosion animation
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if animation is complete, delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]



# Create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)
potion_button = button_potion.ButtonPotion(screen, 50, SCREEN_HEIGHT - BOTTOM_PANEL + 50, potion_img, 64, 64)


# Create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group  = pygame.sprite.Group()
decoration_group  = pygame.sprite.Group()
water_group  = pygame.sprite.Group()
exit_group  = pygame.sprite.Group()
coin_box_group = pygame.sprite.Group()
coins_collected_group = pygame.sprite.Group()
mini_coin_group = pygame.sprite.Group()



# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
print(world_data)
# Load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  #delimiter tells where each value changes to another (every comma)
    for x, row in enumerate(reader):  # gives individual row
        for y, tile in enumerate(row):     # as it iterates it keeps a running count of where we are in the iteration
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)


run = True
while run: 

    clock.tick(FPS)

    if start_game == False:
        # Draw menu
        screen.fill(BG)       
        # Draw buttons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False

    else:
        # Update background
        draw_bg() 
        
        # Draw world map
        world.draw()
        #Draw panel
        draw_panel()

        if 1 in coins_collected:
            draw_gold()
        if 2 in coins_collected:
            draw_silver()
        if 3 in coins_collected:
            draw_bronze()
        
        # score
        if pygame.sprite.spritecollide(player, mini_coin_group, True):
            score += 1
        draw_text(str(score), font, WHITE, 590, SCREEN_HEIGHT - BOTTOM_PANEL + 60)


        # Show player health
        health_bar.draw(player.health)

        # Show ammo
        draw_text('Ammo: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        # Show grenades
        draw_text(f'Grenades: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
        potion = False
        if potion_button.draw():
            potion = True
            
        # Draw text
        draw_text(str(player.potions), font, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 50)
        draw_text("Sorted Medals:", font, WHITE, 430, SCREEN_HEIGHT - BOTTOM_PANEL + 30)
        draw_text(str(coins_collected), font, WHITE, 590, SCREEN_HEIGHT - BOTTOM_PANEL + 30)

        # Update and draw groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        coin_box_group.update()
        coins_collected_group.update()
        mini_coin_group.update()



        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen) 
        coin_box_group.draw(screen)
        coins_collected_group.draw(screen)
        mini_coin_group.draw(screen)

        # Check score


        # Update player actions
        if player.alive:
            # Shoot bullets
            if shoot:
                player.shoot()
            # Throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), 
                            player.rect.top, player.direction)
                grenade_group.add(grenade)
                # Reduce grenades
                player.grenades -= 1
                grenade_thrown = True
            # potion
            if potion == True:
                if player.potions > 0:
                    #check if the potion would heal the player beyond max health
                    if player.max_health - player.health > potion_effect:
                        heal_amount = potion_effect
                    else:
                        heal_amount = player.max_health - player.health
                    player.health += heal_amount
                    player.potions -= 1
                    # damage_text = DamageText(player.rect.centerx, player.rect.y, str(heal_amount), green)
                    # damage_text_group.add(damage_text)
                    action_cooldown = 0
            if player.in_air:
                player.update_action(2)        # 2: JUMP
            elif moving_left or moving_right:
                player.update_action(1)        # 1: RUN
            else:
                player.update_action(0)        # 0: Idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            #print(level_complete)
            bg_scroll -= screen_scroll
            # Check if player has completed level
            if level_complete:
                level += 1
                bg_scroll = 0
                world_data = reset_level()   
                if level <= MAX_LEVELS:
                    # Load new level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')  #delimiter tells where each value changes to another (every comma)
                        for x, row in enumerate(reader):  # gives individual row
                            for y, tile in enumerate(row):     # as it iterates it keeps a running count of where we are in the iteration
                                world_data[x][y] = int(tile)   # update world_data with each individual tile
                    world = World()
                    player, health_bar = world.process_data(world_data)

        else:
            screen_scroll = 0
            if restart_button.draw(screen):   # if clicked
                if choice == 1:
                    if score > high_score:
                        for i in range(len(profs)):
                            if profs[i]['Username'] == user:
                                profs[i]['High score'] = score
                    # if score > profile['High score']:
                    #     print("ok")
                elif choice == 2:
                    profile['High score'] = score
                    profs.append(profile)
                with open("accounts.json", "a") as f:      # write in json
                    json.dump(profs, f, indent=4) 
                with open("accounts.json", "w") as f:
                    profs = json.dump(profs, f, indent=4)
                with open("accounts.json", "r") as f:
                    profs = json.load(f)
                score = 0                                    
                bg_scroll = 0                 # reset variables
                world_data = reset_level()    
                # Load new level data and create world
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')  #delimiter tells where each value changes to another (every comma)
                    for x, row in enumerate(reader):  # gives individual row
                        for y, tile in enumerate(row):     # as it iterates it keeps a running count of where we are in the iteration
                            world_data[x][y] = int(tile)   # update world_data with each indivitual tile
                world = World()
                player, health_bar = world.process_data(world_data)

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
            if event.key == pygame.K_q:
                grenade = True                
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
            if event.key == pygame.K_q:
                grenade = False 
                grenade_thrown = False

    # Update game window
    pygame.display.update()

pygame.quit()

