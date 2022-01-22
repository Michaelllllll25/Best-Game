import pygame
import os
from typing import Dict

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

def create_profiles(name: str, last_name: str, username: str) -> Dict:
    profile_dict = {
        'name': name,
        'last_name': last_name,
        'username': username
    }

    return profile_dict

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
   

    def update(self) -> None:
        """Updates player attributes"""
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        return self.shoot_cooldown



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

        return new_action

    def check_alive(self) -> None:
        """Checks if player is alive"""
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        

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
        return self._username

    def set_username(self, username: int) -> None:
        if username > self._username:
            raise ValueError("Names can't exceed 50 characters")
        elif username < 1:
            raise ValueError("Names must be greater than 1 characters")
        self._username = username