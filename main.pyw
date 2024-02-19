import glm
import pygame

import PhEngineV2
# engine
from PhEngineV2.app import App, mainloop
from PhEngineV2.data import config
from PhEngineV2.space.scene import Scene

# other
from random import randint
import time
from copy import deepcopy
from glm import vec2

from GameData import data
# app modules
from core.source import Loading
from core.soundmanager import OST, MUSIC_END


class Simulation(App):
    def __init__(self):
        """ Init gravity simulation """
        pygame.init()
        self.clock = pygame.time.Clock()
        config.File.apply()
        
        PhEngineV2.init()
        
        """ loading screen """
        loading = Loading(screen=PhEngineV2.window.screen)
        loading.draw_progress(randint(5, 15))
        
        """ Load save """
        self.sol = Scene(f'{config.APPLICATION_PATH}/{config.SAVES_path}/solar system.gs')
        
        PhEngineV2.scene = deepcopy(self.sol)
        PhEngineV2.scene.load()
        
        loading.draw_progress(randint(15, 35))
        
        """ Loading core dependency """
        self.music = OST()
        loading.draw_progress(randint(50, 60))
        
        """ Additional variable """
        self.attach_body = 'Sun'
        # fonts
        self.pause_font = pygame.font.SysFont('Arial', 15, bold=True)
        self.t_speed_font = pygame.font.SysFont('Arial', 15, bold=True)
        self.fps_font = pygame.font.SysFont('Arial', 15, bold=True)
        self.bodies_font = pygame.font.SysFont('Arial', 15, bold=True)
        self.aperture_font = pygame.font.SysFont('Arial', 15, bold=True)
        self.maxlen_font = pygame.font.SysFont('Arial', 15, bold=True)
        # rendered fonts
        self.application_version_font = pygame.font.SysFont(
            'Arial', 15
        ).render(f'{config.APPLICATION_VERSION}', True, 'white')
        self.menu_font = pygame.font.SysFont('arial', 200, bold=True).render(
            'MainMenu', True, 'white'
        )
        self.gs_menu_font = pygame.font.SysFont('arial', 100, bold=True).render(
            'Gravity Simulation 2', True, (20, 200, 30)
        )
        self.start_b_font = pygame.font.SysFont('Arial', 30).render(
            'to start, press Enter', True, 'white'
        )
    
    def attach_at_body(self, name):
        self.attach_body = name
        PhEngineV2.window.camera.position = deepcopy(self.sol.data['data']['camera'].position)
    
    @staticmethod
    def change_t_speed(speed):
        PhEngineV2.time.roster['speed'] = speed
        print(f'time speed - set {speed}')
    
    def events(self) -> None:
        """ Event handling """
        for event in pygame.event.get():
            """ Exit of App to button "close" """
            if event.type == pygame.QUIT:
                App.running = False
            
            elif event.type == pygame.KEYDOWN:
                """ key pressed """
                if event.key == pygame.K_q:
                    App.running = False
                
                elif data.game_status[0] == 'in game':
                    """ in game events """
                    
                    # Перезапуск сцены
                    if event.key == pygame.K_r:
                        PhEngineV2.scene = deepcopy(self.sol)
                        PhEngineV2.scene.load()
                        self.change_t_speed(PhEngineV2.time.roster['speed'])
                    
                    # игра -> пауза
                    elif event.key == pygame.K_p and data.game_status[0] not in {'start', 'loading'}:
                        PhEngineV2.scene.time.start_pause = time.time()
                        data.game_status[0], data.game_status[1] = 'pause', 'in game'
                        self.music.change_sound()
                    
                    # Изменение времени
                    elif event.key == pygame.K_RIGHT:
                        self.change_t_speed(PhEngineV2.time.roster['speed']*2)
                    elif event.key == pygame.K_LEFT:
                        self.change_t_speed(PhEngineV2.time.roster['speed']/2)
                    
                    # Ячейки быстрой смены времени
                    elif event.key == pygame.K_1:
                        self.change_t_speed(512)
                    elif event.key == pygame.K_2:
                        self.change_t_speed(1024)
                    elif event.key == pygame.K_0:
                        self.change_t_speed(1)
                
                elif data.game_status[0] == 'pause':
                    """ pause events """
                    # пауза -> игра
                    if event.key == pygame.K_p and data.game_status[0] not in {'start', 'loading'}:
                        data.game_status[1], data.game_status[0] = 'pause', 'in game'
                        self.music.change_sound()
                    
                    # пауза -> меню
                    elif event.key == pygame.K_RETURN:
                        data.game_status[0], data.game_status[1] = 'menu', None
                        self.music.change_sound()
                        
                        PhEngineV2.window.camera = deepcopy(self.sol.data['data']['camera'])
                        PhEngineV2.time.roster = deepcopy(self.sol.data['time'])
                        
                        self.attach_at_body('Sun')
                
                elif data.game_status[0] == 'menu':
                    if event.key == pygame.K_q:
                        App.running = False
                    # меню -> игра
                    elif event.key == pygame.K_RETURN:
                        data.game_status[0], data.game_status[1] = 'in game', None
                        self.music.change_sound()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if data.game_status[0] != 'menu':
                    if event.button == 5:
                        dist_vec = PhEngineV2.window.camera.distance**.8
                        if dist_vec < 150000000000:
                            PhEngineV2.window.camera.distance += dist_vec
                        else:
                            PhEngineV2.window.camera.distance = 150000000000
                    
                    elif event.button == 4:
                        dist_vec = PhEngineV2.window.camera.distance**.8
                        if dist_vec > 650:
                            PhEngineV2.window.camera.distance -= dist_vec
                        else:
                            PhEngineV2.window.camera.distance = 650
                    
                    elif event.button == 1:
                        for body in PhEngineV2.scene.entities.values():
                            if glm.distance(pygame.mouse.get_pos(), body.render_pos) < 5:
                                self.attach_at_body(body.id)
                                break
                        else:
                            PhEngineV2.scene.events.mouse_rel = True
                    elif event.button == 3:
                        self.attach_at_body('Sun')
                        PhEngineV2.window.camera.distance = deepcopy(self.sol.data['data']['camera'].distance)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    PhEngineV2.scene.events.mouse_rel = False
            
            """ custom events """
            if event.type == MUSIC_END and data.game_status[0] not in {'pause'}:
                # last OST ended => add in queue new track
                self.music.play_new_soundtrack()
    
    def update(self) -> None:
        if data.game_status[0] != 'pause':
            PhEngineV2.scene.__update__()
            
            PhEngineV2.window.camera.attach_pos = PhEngineV2.scene.entities['Sun'].position
        
        if data.game_status[0] != 'menu':
            if PhEngineV2.scene.events.mouse_rel:
                PhEngineV2.window.camera.position -= vec2(pygame.mouse.get_rel())
            else:
                _ = pygame.mouse.get_rel()
            
            PhEngineV2.window.camera.attach_pos = PhEngineV2.scene.entities[self.attach_body].position
    
    def render(self) -> None:
        """ Render images of the game """
        window = PhEngineV2.window.screen
        
        window.fill((0, 0, 0))  # standard screen fill (no floor textures yet)
        
        PhEngineV2.scene.__render__()  # main scene render
        
        """ other render """
        if data.game_status[0] == 'in game':
            fin_font = self.fps_font.render(f'FPS: {int(self.clock.get_fps())}', True, 'white')
            window.blit(fin_font, (5, 5))
            fin_text = self.t_speed_font.render(f'time speed: {PhEngineV2.time.roster["speed"]}', True, 'white')
            window.blit(
                fin_text,
                (config.Screen.size[0] - fin_text.get_width() - 5, 5)
            )
        elif data.game_status[0] == 'pause':
            window.blit(
                self.bodies_font.render(f'bodies count: {len(PhEngineV2.scene.entities)}', True, 'white'), (5, 10)
            )
            window.blit(
                self.aperture_font.render(f'{round(PhEngineV2.window.camera.distance)} points', True, 'white'), (5, 30)
            )
            fin_text = self.pause_font.render(
                f'pause: {int(time.time() - PhEngineV2.scene.time.start_pause)}', True, 'white'
            )
            window.blit(fin_text, (config.Screen.half_size[0] - fin_text.get_width()//2, 0))
            fin_text = self.maxlen_font.render(
                f"orbit len: {PhEngineV2.scene.entities['Sun'].orbit.maxlen}", True, 'white'
            )
            window.blit(fin_text, (5, 50))
        elif data.game_status[0] == 'menu':
            window.blit(self.menu_font, (config.Screen.half_size - vec2(self.menu_font.get_width()//2, 450)))
            window.blit(self.gs_menu_font, (config.Screen.half_size - vec2(self.gs_menu_font.get_width()//2, 250)))
            window.blit(self.start_b_font, (config.Screen.half_size + vec2(-600, 100)))
            window.blit(
                self.application_version_font, (1, config.Screen.size[1] - self.application_version_font.get_height())
            )
        
        pygame.display.flip()  # mandatory screen update
        PhEngineV2.time.dt = self.clock.tick(config.Screen.fps)


if __name__ == '__main__':
    mainloop(Simulation)
