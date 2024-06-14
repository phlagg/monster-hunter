from settings import *

class Sprite(pygame.sprite.Sprite):
    """Generic Sprite"""
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()

class MonsterPatchSprite(Sprite):
    """Monster Grass Patch Sprite"""
    def __init__(self, pos, surf, groups, biome) -> None:
        self.biome = biome 
        super().__init__(pos, surf, groups, WORLD_LAYERS['main' if biome != 'sand' else 'bg'])
        self.y_sort -= 40

class AnimatedSprite(Sprite):
    """Animated sprite"""
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']) -> None:
        self.frame_index, self.frames = 0, frames   
        super().__init__(pos, frames[self.frame_index], groups, z)

    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self, dt) -> None:
        self.animate(dt)

class BorderSprite(Sprite):
    """Sprite for border collision areas"""
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class CollidableSprite(Sprite):
    """Sprite for collidable objects"""
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(self.rect.width *-0.1,self.rect.height * -0.6)


    