import pickle

import PhEngineV2
from PhEngineV2.space.scene import Scene
from PhEngineV2.data import config

from pprint import pprint
from glm import vec2

from GameData import data
from core.save_reader import read_save


config.File.apply()
PhEngineV2.init()

PhEngineV2.scene = Scene('F:/project/Gravity Simulation 2/GameData/saves/solar system.gs')

PhEngineV2.window.camera = PhEngineV2.space.entities.Camera(
    position=-vec2(config.Screen.half_size),
    distance=data.relationship
)

PhEngineV2.time.roster['speed'] = 256

read_save('solar system')

PhEngineV2.scene.write()

with open('F:/project/Gravity Simulation 2/GameData/saves/solar system.gs', mode='rb') as f:
    data = pickle.load(f)

print('read data')
pprint(data)
