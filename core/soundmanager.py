import random

import pygame

from PhEngineV2.data.config import *
from GameData.data import *

from pathlib import Path
FOLDER = Path(rf'{APPLICATION_PATH}/{MUSIC_path}/soundtrack')
print(f'\nmusic    folder - {FOLDER}')
# global audio variables
LEN_MUSIC_FOLDER = len(list(FOLDER.iterdir()))
print(f'music folder len = {LEN_MUSIC_FOLDER}\n\n')

# creating a new event at the end of OST playback
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)


music_types: dict = {
    'menu':    {
        'name': 'menu', 'ratio': (6.5, 250)
    },
}


class MenuOST:
    def __init__(self, loading_sound) -> None:

        pygame.mixer.music.load(
            rf"{APPLICATION_PATH}/{MUSIC_path}/{music_types[loading_sound]['name']}.mp3"
        )

        pygame.mixer.music.set_volume(sound_volume)
        pygame.mixer.music.play(-1,
                                music_types[loading_sound]['ratio'][0],
                                music_types[loading_sound]['ratio'][1])


class InGameSoundtrack:
    def __init__(self) -> None:

        self.music_num = random.randint(1, LEN_MUSIC_FOLDER)

        pygame.mixer.music.load(
            self.choice_decision()
        )
        OST.queue_name = self.choice_decision()

        pygame.mixer.music.set_volume(sound_volume)
        pygame.mixer.music.play()

    def choice_decision(self) -> str:

        if self.music_num < LEN_MUSIC_FOLDER:
            self.music_num += 1
        else:
            self.music_num = 1

        name = rf"{APPLICATION_PATH}/{MUSIC_path}/soundtrack/{self.music_num}.mp3"
        return name


class OST(InGameSoundtrack):

    def __init__(self) -> None:
        super(OST, self).__init__()
        self.change_sound()
        pygame.mixer.music.set_volume(sound_volume)
        print('OST - init')

    @staticmethod
    def change_sound() -> None:
        if game_status[0] in {'start', 'loading'}:
            pygame.mixer.music.unload()
            print('OST - unloading')

        elif game_status == ['in game', 'pause']:
            pygame.mixer.music.set_volume(sound_volume)
            print('OST - unpause')
        elif game_status == ['pause', 'in game']:
            pygame.mixer.music.set_volume(sound_volume/4)
            print('OST - pause')

        elif game_status[0] == 'menu':
            _ = MenuOST('menu')
            print('OST - switch to MenuOST')
        elif game_status == ['in game', None]:
            _ = InGameSoundtrack()
            print('OST - switch to InGameSoundtrack')

        print(game_status)

    def play_new_soundtrack(self) -> None:
        OST.playing_name = OST.queue_name
        OST.queue_name = self.choice_decision()

        pygame.mixer.music.load(OST.playing_name)
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(100)
        print('OST - radio use')
