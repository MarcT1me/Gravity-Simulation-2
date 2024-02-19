import pygame

import glm
from collections import deque
from copy import deepcopy

import PhEngineV2
from PhEngineV2.space.entities import Body
from GameData.data import *


class Planet(Body):
    # variables are a toggle switch for rendering certain things
    show_V_vector = True
    show_V_value = True
    show_name = True
    show_orbit = True
    
    def __init__(self, body_id: str,  # main variables
                 pos: tuple[float], velocity: tuple[float],  # orientation in space
                 mass: float, size: tuple[float],  # transform
                 color: tuple[int] = None, texture: pygame.Surface = None  # albedo
                 ) -> None:
        super().__init__(body_id, pos, 0, velocity, mass, size)

        self.albedo = texture if texture is not None else color
        self.render_pos = glm.vec2(0)
        
        self.V_v_font = None
        self.name_font = None
        self.orbit = None
        
        print('p init', self.id, self.speed, self.pos, self.render_pos)
    
    def __on_init__(self):
        self.time_list = PhEngineV2.space.scene.AttributesKeeper(default=0.0)
        self.orbit = deque(maxlen=int(100_000/PhEngineV2.time.roster['speed']))
        
        self.font_relationship = 15/(PhEngineV2.window.camera.distance/250_000_000)
        self.font_size = int(self.font_relationship**2) if 15 < int(self.font_relationship**2) < 50 \
            else 15 if 15 > int(self.font_relationship**2) else 50
        
        # fonts
        self.V_v_font = pygame.font.SysFont(
            'Arial',
            int(self.font_size*.75)
        )
        self.name_font = pygame.font.SysFont(
            'Arial',
            self.font_size
        ).render(f'{self.id}', True, 'white')
    
    def __in_pickles__(self): del self.V_v_font, self.name_font
    
    def update(self) -> None:
        if PhEngineV2.time.timer(self.time_list, 'orbit_write', 0.2/PhEngineV2.time.roster['speed']):
            self.orbit.append(deepcopy(self.position))
        if PhEngineV2.time.timer(self.time_list, 'change_t_speed', 0.1):
            self.orbit = deque(self.orbit, maxlen=int(100_000/PhEngineV2.time.roster['speed']))
        
        self.use_gravity()
    
    @staticmethod
    def normalize_pos(pos):
        vec = pos - PhEngineV2.window.camera.attach_pos
        return vec/PhEngineV2.window.camera.distance - PhEngineV2.window.camera.position
    
    def draw_v_vector(self) -> None:
        V_line_end = self.render_pos + self.V_vector/line_relationship
        
        pygame.draw.line(
            PhEngineV2.window.screen, (255, 0, 0), self.render_pos,
            V_line_end
        )
        
        if self.show_V_value:
            PhEngineV2.window.screen.blit(
                self.V_v_font.render(f'V: {round(self.V_vector.x)}, {round(self.V_vector.y)}', True, 'white'),
                V_line_end
            )
    
    def draw_name(self):
        PhEngineV2.window.screen.blit(self.name_font, self.render_pos)
    
    def draw_orbit(self):
        len_orbit = len(self.orbit)
        for i in range(len(self.orbit) - 1):
            color = glm.vec3(10, glm.vec2(255*(i/len_orbit)))
            pygame.draw.line(
                PhEngineV2.window.screen, color,
                self.normalize_pos(self.orbit[i]),
                self.normalize_pos(self.orbit[i + 1])
            )
    
    def render(self) -> None:
        self.draw_orbit() if self.show_orbit else Ellipsis
            
        self.render_pos = self.normalize_pos(self.position)
        
        render_size = self.size[0]/(PhEngineV2.window.camera.distance**2)
        
        pygame.draw.line(
            PhEngineV2.window.screen, (50, 50, 50),
            (PhEngineV2.config.Screen.half_size + self.render_pos)*0.5,
            self.render_pos
        )  # line from window center to Body center
        
        pygame.draw.circle(
            PhEngineV2.window.screen, self.albedo, self.render_pos,
            render_size
        )  # The body itself
        
        # other render
        self.draw_name() if self.show_name else Ellipsis
        self.draw_v_vector() if self.show_V_vector else Ellipsis


class Satellite(Planet):
    show_pos = True
    
    def __init__(self, *args, offset: tuple = (0, 0), **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.offset = glm.vec2(offset)
        self.show_V_value = False
    
    def __on_init__(self):
        super().__on_init__()
        self.name_font = pygame.font.SysFont(
            'Arial',
            int(self.font_relationship**2) if 10 < int(self.font_relationship**2) < 50
            else 10 if 10 > int(self.font_relationship**2) else 50
        ).render(f'{self.id}', True, 'white')
    
    def draw_name(self):
        font_pos_relationship = self.font_size/20
        font_pos = self.render_pos + self.offset*glm.vec2(font_pos_relationship)
        PhEngineV2.window.screen.blit(
            self.name_font,
            font_pos
        )
        
        if self.show_pos:
            pygame.draw.line(
                PhEngineV2.window.screen, (200, 200, 200),
                self.render_pos, font_pos
            )
