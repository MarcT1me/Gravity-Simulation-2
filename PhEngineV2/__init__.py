import PhEngineV2.time
import PhEngineV2.data.config as config
import PhEngineV2.space.entities
import PhEngineV2.space.phisic
import PhEngineV2.space.scene

import pygame

window = None  # type: PhEngineV2.__Graphic
scene = None  # type: PhEngineV2.space.scene.Scene


class __Graphic:
    screen = None  # type: pygame.display.set_mode
    camera = None  # type: PhEngineV2.space.entities.Camera
    
    @classmethod
    def __init__(cls, flags):
        # create pygame window
        if config.Screen.full:
            config.SCREEN_SIZE = pygame.display.get_desktop_sizes()[config.Screen.display]
        cls.screen = \
            pygame.display.set_mode(
                config.Screen.size,
                display=config.Screen.display, vsync=config.Screen.vsync,
                flags=flags
            )
        if config.Screen.full != pygame.display.is_fullscreen():
            pygame.display.toggle_fullscreen()
        pygame.display.flip()
        
        w_size = pygame.display.get_window_size()
        config.Screen.size = list(w_size)
        config.Screen.half_size = [w_size[0]//2, w_size[1]//2]
        print(w_size)
        
        # other pygame window settings
        pygame.display.set_caption(config.APPLICATION_NAME)
        pygame.display.set_icon(
            pygame.image.load(
                rf'{config.APPLICATION_PATH}/{config.APPLICATION_ICO_path}/{config.APPLICATION_ICO_name}'
            )
        )


def init(*, flags=pygame.DOUBLEBUF) -> None:
    global window
    pygame.init()
    """ Init Engine """
    window = __Graphic(flags)
    PhEngineV2.time.dt = 0
