""" Game settings.
 in present be rewrite from settings.json
 """
from os.path import dirname, abspath  # path
from inspect import stack
import toml

from pygame.display import init as display_init, get_desktop_sizes  # screen size variable

from dataclasses import dataclass
from collections.abc import Mapping

""" Engine settings """
APPLICATION_NAME = 'Gravity simulation'  # I do not recommend changing
APPLICATION_VERSION: str = '2.4.2'  # I do not recommend changing

""" Path settings """
APPLICATION_PATH: str = dirname(abspath(stack()[1].filename)).removesuffix('\\PyInstaller\\loader').removesuffix(f"\\PhEngineV2\\messages")
TEXTURE_path = rf'core/presets/textures'  # DO NOT CHANGE
MUSIC_path = rf'core/presets/sounds/music'  # DO NOT CHANGE
SAVES_path = rf'GameData/saves'  # DO NOT CHANGE
# ico settings
APPLICATION_ICO_path, APPLICATION_ICO_name = TEXTURE_path, 'GravitySimulation.ico'  # do not change


class Settings:
    IS_RELEASE = False
    
    @classmethod
    def update(cls, changes: dict): [setattr(cls, key, value) for key, value in changes.items()]


@dataclass(init=False)
class Screen(Settings):
    """ Screen settings """
    fps: int = 0
    
    vsync: bool = False
    display: int | None = 0  # I do not recommend changing
    
    full: bool = True
    _, size = display_init(), get_desktop_sizes()[display]
    half_size: tuple = size[0]//2, size[1]//2  # DO NOT CHANGE


@dataclass(kw_only=True, init=False)
class File(Settings):
    """ Import data from file """
    name: str = 'config'
    data = {}
    
    @staticmethod
    def _read_():
        """ Read CONFIG files """
        with open(rf"{APPLICATION_PATH}/GameData/{File.name}.toml", mode='r') as file:
            return toml.load(file)
    
    @classmethod
    def change_data(cls, changes: dict, data: dict = None):
        if data is None:
            data = File.data
        for key, value in changes.items():
            if isinstance(value, Mapping):
                data[key] = cls.change_data(value, data.get(key, {}))
            else:
                data[key] = value
        return data
    
    @classmethod
    def write(cls, *, changes: dict = None):
        """ Write CONFIG files """
        if len(File.data) == 0:
            File.data = cls._read_()
        File.change_data(changes) if changes is not None else Ellipsis
        
        with open(rf"{APPLICATION_PATH}/GameData/config.toml", mode='w') as file:
            toml.dump(File.data, file)
    
    @classmethod
    def apply(cls, data=None):
        if data is None:
            data = cls._read_()
            File.data = data
        if len(File.data) == 0:
            data = File.data
        for key, value in data.items():
            if isinstance(value, dict):
                # Если значение является словарем, рекурсивно обновляем переменные
                cls.apply(value)
            if key in {'Screen'}:
                exec(f"""{key}.update(value)""")
