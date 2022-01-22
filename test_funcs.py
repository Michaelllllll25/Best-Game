from funcs import sort
from funcs import Soldier
from funcs import sort_leaderboard
from funcs import create_profiles 
from funcs import Profile
import funcs

def test_sort():
    assert sort([2,3,1]) == [1,2,3]
    assert sort([2,2,2,3,1]) == [1,2,2,2,3]
    assert sort([2,3,1,1]) == [1,1,2,3]
    assert sort([2,3,3,1]) == [1,2,3,3]

def test_sort_leaderboard():
    assert sort_leaderboard([100,50,25]) == [25,50,100]
    assert sort_leaderboard([99,50,60]) == [50,60,99]
    assert sort_leaderboard([1,40,25]) == [1,25,40]
    assert sort_leaderboard([3,3,50,25]) == [3,3,25,50]


def test_create_profiles():
    profile_dict = funcs.create_profiles(name="Michael",
                                          last_name="Moser",
                                          username="Drops")

    assert profile_dict["name"] == "Michael"
    assert profile_dict["last_name"] == "Moser"
    assert profile_dict["username"] == "Drops"


def test_soldier_attributes():
    p = Soldier('Enemy', 200, 200, 3, 3, 20, 0, 0)
    assert p.char_type == 'Enemy'
    assert p.health == 100
    assert p.max_health == p.health
    assert p.shoot_cooldown == 0
    assert p.direction == 1  
    assert p.vel_y == 0      
    assert p.jump == False
    assert p.in_air == True
    assert p.flip == False
    assert p.animation_list == []
    assert p.frame_index == 0
    assert p.action == 0
    assert p.speed == 3
    assert p.ammo == 20
    assert p.grenades == 0
    assert p.potions == 0

    a = Soldier('Player', 300, 400, 3, 3, 25, 5, 3)
    assert a.char_type == 'Player'
    assert a.health == 100
    assert a.max_health == p.health
    assert a.shoot_cooldown == 0
    assert a.direction == 1  
    assert a.vel_y == 0      
    assert a.jump == False
    assert a.in_air == True
    assert a.flip == False
    assert a.animation_list == []
    assert a.frame_index == 0
    assert a.action == 0
    assert a.speed == 3
    assert a.ammo == 25
    assert a.grenades == 5
    assert a.potions == 3

def test_get_name():
    n = Profile('Michael', 'Moser', 'Drops')
    assert n.get_name() == 'Michael'

def test_get_last_name():
    n = Profile('Michael', 'Moser', 'Drops')
    assert n.get_last_name() == 'Moser'    

def test_get_username():
    n = Profile('Michael', 'Moser', 'Drops')
    assert n.get_username() == 'Drops'   

