import pygame

import glm
import time
from dataclasses import dataclass
from abc import abstractmethod

import PhEngineV2
from PhEngineV2.space import phisic


@dataclass
class Camera:
    """ The camera is a class for storing data on the positioning of all bodies in the scene,
    needed for use and self-creation of algorithms """
    position: tuple[int]
    distance: float
    attach_pos: glm.vec2 = glm.vec2(0)
    
    def __post_init__(self):
        self.position = glm.vec2(self.position)
    
    @property
    def pos(self) -> glm.vec2: return self.position
    
    @pos.setter
    def pos(self, value: glm.vec2 | tuple) -> None: self.position = glm.vec2(value)


class Body:
    """ A commonplace scene, designed for inheritance """
    def __init__(self, body_id,
                 pos: tuple[float], angle: int, velocity: tuple[float] = (0, 0),
                 mass: float = None, size: tuple[float] = None
                 ) -> None:
        self.id = body_id
        # orientation in space
        self.position = glm.vec2(pos)
        self.angle = glm.radians(angle)
        # velocity
        self.V_vector = glm.vec2(velocity)
        # forces
        self.F_total = glm.vec2(0.0)
        # other physical parameter
        self.mass: float = mass
        self.size = glm.vec2(size)
        
        PhEngineV2.scene.entities[self.id] = self
    
    @abstractmethod
    def __on_init__(self): ...
    
    @abstractmethod
    def __in_pickles__(self): ...
    
    @property
    def pos(self) -> tuple: return tuple(self.position)
    
    @pos.setter
    def pos(self, value: glm.vec2 | tuple) -> None: self.position = glm.vec2(value)
    
    @property
    def tilt(self) -> float: return glm.degrees(self.angle)
    
    @tilt.setter
    def tilt(self, value: float) -> None: self.angle = glm.radians(value)
    
    @property
    def speed(self) -> tuple: return tuple(self.V_vector)
    
    @speed.setter
    def speed(self, value: glm.vec2 | tuple) -> None: self.V_vector = glm.vec2(value)
    
    def change_force(self) -> None:
        F_gravity = glm.vec2(0, 0)
        
        for entity in PhEngineV2.scene.entities.values():
            F_gravity += phisic.calculate_gravitational_force(
                self.position, entity.position,
                self.mass, entity.mass
            )
        
        self.F_total = F_gravity
    
    def use_gravity(self) -> None:
        self.change_force()
        
        a = self.F_total/self.mass
        
        self.V_vector += a*PhEngineV2.time.dt*PhEngineV2.time.roster['speed']
        
        self.position += self.V_vector*PhEngineV2.time.dt*PhEngineV2.time.roster['speed']
    
    def event(self, event) -> None: ...
    
    def update(self) -> None: ...
    
    def render(self) -> None: ...


class Button:
    roster = list()
    
    def __init__(self, *,
                 # WINDOW
                 size: tuple[int, int] = (100, 100),
                 pos: tuple[int, int] = (0, 0),
                 source: str = None,
                 image_pos: tuple = (0, 0),
                 # TEXT
                 text: str = '',
                 text_size: int = 20,
                 text_pos: tuple = (0, 0),
                 text_center: bool = False,
                 text_clor: tuple[int, int, int] = (220, 220, 220),
                 text_bold: bool = True,
                 # COLORS
                 font: str = 'Arial',
                 bgcolor_on_press: tuple[int, int, int] = (100, 150, 250),
                 bgcolor_not_press: tuple[int, int, int] = (120, 120, 120),
                 # FUNCTIONAL
                 on_press=lambda: None,
                 on_clamping=lambda: None,
                 on_release=lambda: None,
                 release_long: float = 1
                 ) -> None:
        """ INIT a button class and assigning values. """
        
        """ RECT """
        self.pos: tuple = pos
        self.size: tuple = size
        
        """ IMAGE """
        self.image = pygame.transform.scale(pygame.image.load(source), size) if source is not None else None
        self.image_pos = image_pos
        
        """ TEXT """
        self.text: str = text
        self.text_size: tuple = text_size
        self.text_clor: tuple = text_clor
        self.font = pygame.font.SysFont(font, self.text_size, bold=text_bold).render(self.text, True, self.text_clor)
        self.font_size: tuple = self.font.get_size()
        self.text_pos: tuple = (
            text_pos[0] - self.font.get_width()//2, text_pos[1] - self.font.get_height()//2
        ) if text_center else text_pos
        
        """ SURFACE """
        self.surf = pygame.Surface(size)
        self.bgcolor_on_press: tuple = bgcolor_on_press
        self.bgcolor_not_press: tuple = bgcolor_not_press
        self.surf_color: tuple = bgcolor_not_press
        self.surf.set_colorkey(self.surf_color) if self.image is not None else Ellipsis
        
        """ FUNCTION """
        self.release_start = None
        self.release_long = release_long
        
        self.on_press = on_press
        self.on_clamping = on_clamping
        self.on_release = on_release
        self.roster.append(self)
    
    def on_init(self):
        """ CREATING a button using data """
    
    def event(self, event: pygame.event.Event) -> None:
        """ События кнопки, нажатие (короткое/долгое) и реализация функционала """
        if self.release_start is not None:
            if self.release_start + self.release_long <= time.time():
                """ Долгое удержание """
                self.on_clamping()  # долгое нажатие
                
                self.release_start = None  # сброс значений нажатия
                return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            """ Нажатие """
            if pygame.rect.Rect(*self.pos, *self.size).collidepoint(pygame.mouse.get_pos()):
                # изменение цвета на активное
                self.surf_color = self.bgcolor_not_press if self.image is not None else self.bgcolor_on_press
                
                if self.release_start is None:  # ставлю значение нажатия
                    self.release_start = time.time()
            
            else:
                self.surf_color = self.bgcolor_not_press
        
        elif event.type == pygame.MOUSEBUTTONUP:
            """ Отжатие """
            self.surf_color = self.bgcolor_not_press  # изменение цвета на не активное
            
            if self.release_start is not None:
                if self.release_start + self.release_long >= time.time():
                    """ Недолгое удержание """
                    self.on_press()  # недолгое нажатие
                
                self.release_start = None  # сброс значений нажатия
    
    def render(self, win) -> None:
        """ Render button.   всегда один подход   """
        self.surf.fill(self.surf_color)
        
        self.surf.blit(self.image, self.image_pos) if self.image is not None else Ellipsis
        self.surf.blit(self.font, self.text_pos)  # отображение текста и изображения кнопки
        
        win.blit(self.surf, self.pos)
    
    def relies(self):
        self.roster.remove(self)
    
    @staticmethod
    def roster_event(event):
        for btn in Button.roster:
            btn.event(event)
    
    @staticmethod
    def roster_render(win):
        for btn in Button.roster:
            btn.render(win)
    
    @staticmethod
    def roster_relies():
        for btn in Button.roster:
            btn.relies()
