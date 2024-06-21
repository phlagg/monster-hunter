import pygame.freetype
from settings import *
from random import choice
from support import draw_bar

class MonsterIndex():
    """Creates an index to manage and store Monsters"""
    def __init__(self, monsters, fonts, frames) -> None:
        self.display_surface = pygame.display.get_surface()
        self.monsters = monsters
        self.frame_index = 0
        self.fonts:dict[pygame.Font] = fonts
        # frames
        self.icon_frames = frames['icons']
        self.monster_frames = frames['monsters']
        # tint surf
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)
        # dimensions
        self.main_rect = pygame.FRect(0, 0, WINDOW_WIDTH* 0.6, WINDOW_HEIGHT * 0.8).move_to(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        # list
        self.visible_items = 6
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visible_items
        self.index = 0
        self.selected_index = None

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 1
            self.frame_index = 0
        if keys[pygame.K_DOWN]:
            self.index += 1
            self.frame_index = 0
        if keys[pygame.K_SPACE]:
            if self.selected_index != None:
                selected_monster = self.monsters[self.selected_index]
                current_monster = self.monsters[self.index]
                self.monsters[self.index] = selected_monster
                self.monsters[self.selected_index] = current_monster
                self.selected_index = None
            else:
                self.selected_index = self.index
                
        self.index = self.index % len(self.monsters)


    def display_list(self) -> None:
        v_offset = 0 if self.index < self.visible_items else -1*(self.index - self.visible_items+1) * self.item_height
        scale_factor = 1.2
        # items
        for index, monster in self.monsters.items():
            highlighted = self.index == index
            # colors
            bg_color = COLORS['gray'] if not highlighted else COLORS['light']
            text_color = COLORS['white'] if self.selected_index != index else COLORS['gold']
            top = self.main_rect.top + index * self.item_height + v_offset
            
            item_rect = pygame.FRect(self.main_rect.left,top,self.list_width, self.item_height)
            # item_rect = item_rect if not highlighted else item_rect.inflate(10,0)
            item_rect.left = self.main_rect.left

            
            text_surf = self.fonts['regular'].render(monster.name, False, text_color)
            text_surf = text_surf if not highlighted else pygame.transform.scale_by(text_surf,scale_factor) 
            text_rect = text_surf.get_frect(midleft = item_rect.midleft + vector(90, 0))

            icon_surf = self.icon_frames[monster.name]
            icon_surf = icon_surf if not highlighted else pygame.transform.scale_by(icon_surf,scale_factor)
            icon_rect = icon_surf.get_frect(center = item_rect.midleft + vector(45,0))
            
            if item_rect.colliderect(self.main_rect):
                # check corners
                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0,0,12)
                elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1,-1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0,0,0,0,12,0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)
        
        # lines
        for i in range(min(self.visible_items - 1, len(self.monsters) -1)):
            y = (i + 1) * self.item_height + self.main_rect.top
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, COLORS['light-gray'], (left, y), (right, y))    

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width-4, self.main_rect.top))
    
    def display_main(self,dt) -> None:
        # data
        monster = self.monsters[self.index]
        
        # main bg
        rect = pygame.FRect(self.main_rect.left + self.list_width, self.main_rect.top, \
                            self.main_rect.width - self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12, 0, 12, 0)
        # monster display
        top_rect = pygame.FRect(rect.topleft,(rect.width, rect.width* 0.4))
        pygame.draw.rect(self.display_surface, COLORS[monster.element], top_rect, 0,0,0,12)
        # monster animation
        self.frame_index += ANIMATION_SPEED * dt
        frames = self.monster_frames[monster.name]
        state = 'attack' if self.frame_index <= len(frames['attack']) else 'idle'
        monster_surf = frames[state][int(self.frame_index)%len(frames[state])]
        monster_rect = monster_surf.get_frect(center = top_rect.center)
        self.display_surface.blit(monster_surf, monster_rect)
        # name
        name_surf: pygame.Surface = self.fonts['bold'].render(monster.name, False, COLORS['white'])
        name_rect = name_surf.get_frect(topleft = top_rect.topleft + vector(10,10))
        self.display_surface.blit(name_surf, name_rect)
        # level
        level_surf: pygame.Surface = self.fonts['regular'].render(f'Lvl: {monster.level}', False, COLORS['white'])
        level_rect = level_surf.get_frect(bottomleft = top_rect.bottomleft + vector(10,-10))
        self.display_surface.blit(level_surf, level_rect)
        # XP bar
        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(level_rect.bottomleft, (100, 4)),
            value= monster.xp, 
            max_value= monster.level_up, 
            color= COLORS['white'], 
            bg_color= COLORS['dark'], 
            radius= 1)
        # element
        element_surf: pygame.Surface = self.fonts['regular'].render(monster.element, False, COLORS['white'])
        element_rect = element_surf.get_frect(bottomright = top_rect.bottomright + vector(-10,-10))
        self.display_surface.blit(element_surf, element_rect)
    def update(self, dt) -> None:
        self.input()
        self.display_surface.blit(self.tint_surf, (0,0))
        # pygame.draw.rect(self.display_surface, 'black', self.main_rect)
        self.display_list()
        self.display_main(dt)
        # display the main section
        