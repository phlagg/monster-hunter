from game_data import MONSTER_DATA

class Monster():
    """Data class for monster"""
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level
        # stats
        self.element = MONSTER_DATA[name]['stats']['element']
        self.base_stats = MONSTER_DATA[name]['stats']
    