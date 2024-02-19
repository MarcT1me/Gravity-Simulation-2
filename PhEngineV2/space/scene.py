import os
import pickle

from typing import TypedDict
from dataclasses import dataclass, field

import PhEngineV2


class AttributesKeeper:
    """ A class that should store attributes and replace the dictionary """
    def __init__(self, default):
        self.default = default
    
    def __getattr__(self, item):
        super().__setattr__(item, self.default)
        return self.default


""" TypeDict for data from a file """


class _Data(TypedDict):
    objects: dict[str, PhEngineV2.space.entities.Body]
    lights: dict
    camera: PhEngineV2.space.entities.Camera


class _FormatSav(TypedDict):
    time: dict[str, float]
    events: dict
    data: _Data


@dataclass(init=True)
class Scene:
    """ A scene is a class that stores data about the simulation space """
    _path: str
    
    time = AttributesKeeper(default=0.0)
    events = AttributesKeeper(default=False)
    
    entities = dict()
    lights = dict()
    
    data: _FormatSav = field(init=False, default_factory=lambda: dict())
    
    def add(self, obj: PhEngineV2.space.entities.Body, abbr: str = None) -> str:
        if abbr is not None:
            assert abbr in self.entities.keys(), f"Object with abbreviation '{abbr}' already exists"
            self.entities[abbr] = obj
            return abbr
        self.entities[obj.id] = obj
        return obj.id
    
    def __events__(self, event) -> None: [entity.event(event) for entity in self.entities.values()]
    
    def __update__(self) -> None: [entity.update() for entity in self.entities.values()]
    
    def __render__(self) -> None: [entity.render() for entity in self.entities.values()]
    
    def __post_init__(self):
        self._root = lambda: os.path.dirname(self._path)
        self._name = lambda: os.path.basename(self._path)[:-3]
        
        """ load data from save.sav file """
        if os.path.isfile(path=self._path):
            with open(self._path, 'rb') as file:
                self.data = pickle.load(file)
        else:
            with open(self._path, 'wb') as file:
                pickle.dump(self.data, file)
    
    def dell(self) -> bool:
        """ dell save.sav file """
        if os.path.isfile(path=self._path):
            os.remove(self._path)
            return True
        raise FileNotFoundError(f'there is no save with the name {self._name()} in the directory {self._root()}')
    
    def change_name(self, name):
        self._path = self._root() + '/' + str(name) + '.gs'
    
    def __on_init__(self):
        [entity.__on_init__() for entity in self.entities.values()]
    
    def __in_pickles__(self):
        [entity.__in_pickles__() for entity in self.entities.values()]
    
    def _format_sav(self) -> _FormatSav:
        self.__in_pickles__()
        return {
            'time': PhEngineV2.time.roster,
            'data': {
                'objects': self.entities,
                'lights':  self.lights,
                'camera':  PhEngineV2.window.camera,
            },
        }
    
    def write(self, *, name: str = None):
        """ write scene in file """
        self.change_name(name) if name is not None else Ellipsis
        self.data = self._format_sav() if len(self.data) == 0 else self.data
        
        with open(self._path, 'wb') as file:
            pickle.dump(self.data, file)
    
    def load(self) -> _FormatSav:
        """ scene space reading """
        PhEngineV2.time.roster = self.data['time']
        space = self.data['data']
        
        # bodies
        self.entities = space['objects']
        # camera
        PhEngineV2.window.camera = space['camera'] if space['camera'] is not None else \
            PhEngineV2.space.entities.Camera(position=(0, 0), distance=1)
        
        self.__on_init__()
