from pygame import Surface
from timer import Timer
from settings import *

class DialogTree():
    """Class that creates and manages the dialog between the player and NPCs"""
    def __init__(self, character, player, all_sprites, font, end_dialog) -> None: 
        self.character = character
        self.player = player
        self.all_sprites = all_sprites
        self.font = font

        self.dialog = character.get_dialog()
        self.dialog_num = len(self.dialog)
        self.dialog_index = 0
        self.dialog_timer = Timer(500, autostart=True )
        self.end_dialog = end_dialog
        self.current_dialog = DialogSprite(
                                message=self.dialog[self.dialog_index], 
                                character=self.character, 
                                groups=self.all_sprites,
                                font=self.font)

    def input(self) -> None:
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and not self.dialog_timer.active:
            self.current_dialog.kill()
            self.dialog_index += 1
            if self.dialog_index < self.dialog_num:
                self.dialog_timer.activate()
                self.current_dialog = DialogSprite(
                                        message=self.dialog[self.dialog_index], 
                                        character=self.character, 
                                        groups=self.all_sprites,
                                        font=self.font)
            else:
                self.end_dialog(self.character)
    
    def update(self) -> None:
        self.dialog_timer.update()
        self.input()

class DialogSprite(pygame.sprite.Sprite):
    """Sprites used for displaying character dialog"""
    def __init__(self, message, character, groups, font):
        super().__init__(groups)
        self.z = WORLD_LAYERS['top']

        # text
        text_surf: Surface = font.render(message, False, COLORS['black'])
        padding = 5
        width = max(30,text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2

        # background
        surf:Surface = Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.rect(
            surface=surf, 
            color=COLORS['pure white'], 
            rect=surf.get_frect(topleft = (0,0)), 
            width=0,
            border_radius=4)
        
        surf.blit(text_surf, text_surf.get_frect(center = (width/2, height/2)))
        self.image = surf
        self.rect = self.image.get_frect(midbottom = character.rect.midtop + vector(0, -10))


        