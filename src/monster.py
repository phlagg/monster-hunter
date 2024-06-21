from game_data import MONSTER_DATA
from random import randint

class Monster():
    """Data class for monster"""
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level
        # stats
        self.element = MONSTER_DATA[name]['stats']['element']
        self.base_stats = MONSTER_DATA[name]['stats']
        # experience
        self.xp = randint(0,1000)
        self.level_up = self.level * 150