from settings import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from os.path import join
import os
from pyinstrument import Profiler

from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree
from support import *
from game_data import CHARACTER_DATA, MONSTER_DATA
from debug import debug

class Game:
    def __init__(self) -> None:
        working_dir = os.path.dirname(__file__)
        os.chdir(working_dir)
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Hunter')
        self.clock = pygame.time.Clock()
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()

        self.import_assets()
        # self.setup(self.tmx_maps['hospital'], 'world')
        self.setup(self.tmx_maps['world'], 'house')
        self.dialog_tree = None

    def import_assets(self) -> None:
        self.tmx_maps: dict[TiledMap] = {
            'world': load_pygame(join('..','data','maps','world.tmx')),
            'hospital': load_pygame(join('..','data','maps','hospital.tmx'))
            }
        
        self.overworld_frames = {
            'water': import_folder('..','graphics','tilesets','water'),
            'coast': coast_importer(24, 12, '..','graphics','tilesets','coast'),
            'characters': all_character_import('..','graphics','characters')}
        # print(self.overworld_frames['characters']['blond'])

        self.fonts = {
            'dialog': pygame.font.Font(join('..','graphics', 'fonts', 'PixeloidSans.ttf'), 30)
            }

    def setup(self, tmx_map:TiledMap, player_start_pos) -> None:
        # Terrain Tiles
        for layer in ['Terrain', 'Terrain Top']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x*TILE_SIZE,y*TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
        # Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name =='top': 
                Sprite((obj.x,obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
            else:
                CollidableSprite((obj.x,obj.y), obj.image, [self.all_sprites, self.collision_sprites]) 
        # Collision Objects
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x,obj.y), pygame.Surface((obj.width, obj.height)), [self.collision_sprites])

        # Grass Patches
        for obj in tmx_map.get_layer_by_name('Monsters'):
            MonsterPatchSprite((obj.x,obj.y), obj.image, self.all_sprites, obj.properties['biome'])
        # Water
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])
        # Coast
        for obj in tmx_map.get_layer_by_name('Coast'):
            side = obj.properties['side']
            terrain = obj.properties['terrain']
            AnimatedSprite((obj.x,obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'])

        # Entities
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    pos= (obj.x, obj.y), 
                    facing_direction= obj.properties['direction'],
                    frames= self.overworld_frames['characters']['player'],
                    groups= self.all_sprites,
                    collision_sprites = self.collision_sprites)
            
            elif obj.name == 'Character' :
                Character(
                    pos= (obj.x, obj.y),
                    facing_direction= obj.properties['direction'],
                    frames= self.overworld_frames['characters'][obj.properties['graphic']],
                    groups= [self.all_sprites, self.collision_sprites, self.character_sprites], 
                    character_data= CHARACTER_DATA[obj.properties['character_id']])

    def input(self) -> None:
        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE]:
                for character in self.character_sprites:
                    if check_connections(100, self.player, character):
                        self.player.block()
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)

    def create_dialog(self, character) -> None:
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

    def end_dialog(self, character):
        self.dialog_tree = None
        self.player.unblock()

    def run(self) -> None:
        # profiler = Profiler()
        # profiler.start()
        while True:
            dt = self.clock.tick() / 1000
            # limit the size of dt to prevent issues when moving the window
            max_dt = 0.1
            dt = min(dt, max_dt)
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # profiler.stop()
                    # profiler.print()
                    pygame.quit()
                    exit()

            # game logic
            self.input()
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            # overlays
            if self.dialog_tree: self.dialog_tree.update()
            debug(f'{self.clock.get_fps():.2f}')
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()

