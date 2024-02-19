""" Main Engine Application.
Allows you to set up constants, run test versions of the application and create a world for simulation.
"""

from kivy.app import App  # main from kivy

# other
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar

# widgets
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# other
import ctypes
import time

from PhEngineV2.core.units import UnitTestsPage


def get_resolution():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize


def resize_window(size, pos=None):
    w_size = get_resolution()
    Window.size = size
    Window.left = w_size[0]//2 - size[0]//2 if pos is None else pos[0]
    Window.top = w_size[1]//2 - size[1]//2 if pos is None else pos[1]


def animated_resize(size, pos=None, duration=0.15):
    anim1 = Animation(size=size, duration=duration)
    
    w_size = get_resolution()
    
    l = w_size[0]//2 - size[0]//2 if pos is None else pos[0]
    anim2 = Animation(left=l, duration=duration)
    
    t = w_size[1]//2 - size[1]//2 if pos is None else pos[1]
    anim3 = Animation(top=t, duration=duration)
    
    anim1.start(Window)
    anim2.start(Window)
    anim3.start(Window)


class Starting(Screen):
    def __init__(self, **kwargs):
        """ Start screen, init all app dependencies """
        super().__init__(**kwargs)
        # Установка фонового изображения
        resize_window((480, 270))
        Window.borderless = True
        
        self.background_image = Image(
            source='data/start_background.jpg',  # screenshot from the game Elite Dangerous
            allow_stretch=True, keep_ratio=False
        )
        self.add_widget(self.background_image)
        
        self.pe_lbl = Label(
            text='PhEngine V2',
            size_hint=(1, 0.2),
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.8
            },
            font_size=50,
            font_name='Arial'
        )
        self.add_widget(self.pe_lbl)
        
        self.start_button = Button(
            text='Starting...',
            on_press=self.switch_to_main,
            disabled=True,
            size_hint=(0.3, 0.2),
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.2
            },
            background_color=(0.1, 0.1, 0.1)
        )
        self.add_widget(self.start_button)
        
        self.pb = ProgressBar(
            size_hint=(1, 0.15),
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.0
            },
        )
        self.add_widget(self.pb)
    
    def on_enter(self, *args):
        """ just event """
        self.start = time.time()
        self.event = Clock.schedule_interval(self.check_event, 0.1)  # Проверяем каждые 0.1 секунды
        Clock.schedule_once(self.set_start, 2)
    
    def set_start(self, dt): PhEngineApp.loading_complete = True
    
    def check_event(self, dt):
        """ check loading finishing """
        
        anim = Animation(value=(time.time() - self.start)*100, duration=0.09)
        anim.start(self.pb)
        
        if App.get_running_app().loading_complete:
            self.pb.disabled = True
            
            anim = Animation(value=100, duration=0.09)
            anim.start(self.pb)
            
            self.start_button.disabled = False  # switch on main tab
            self.start_button.text = 'To main page'
            self.animate_button_color()
            
            self.event.cancel()  # close timer
    
    def animate_button_color(self):
        # Анимация изменения цвета кнопки
        anim = Animation(background_color=(50/255, 80/255, 180/255, 0.8), duration=0.5)
        anim.start(self.start_button)
    
    def switch_to_main(self, instance):
        """ start """
        instance.disabled = True
        self.manager.current = 'main'
        
        Window.borderless = False
        # animated_resize((1920, 1010), pos=(0, 30))
        animated_resize((1000, 550))


class MainPage(Screen):
    def __init__(self, **kwargs):
        """ Some main page """
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.settings_btn = Button(
            text='Change config files',
            on_press=self.config_screen,
        
        )
        self.bl.add_widget(self.settings_btn)
        self.run_btn = Button(
            text='Run code',
            on_press=self.config_screen,
        )
        self.bl.add_widget(self.run_btn)
        self.run_btn = Button(
            text='Units tests',
            on_press=self.units_screen,
        )
        self.bl.add_widget(self.run_btn)
        
        self.add_widget(self.bl)
    
    def run_screen(self, instance):
        self.manager.current = 'run'
    
    def units_screen(self, instance):
        self.manager.current = 'units'
    
    def config_screen(self, instance):
        self.manager.current = 'config'


class PhEngineApp(App):
    loading_complete = BooleanProperty(False)  # Переменная, которая должна измениться на True после загрузки
    
    def build(self):
        sm = ScreenManager()
        
        """ All Engine Screens and Tabs """
        sm.add_widget(Starting(name='start'))
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(UnitTestsPage(name='units'))
        
        return sm


if __name__ == '__main__':
    PhEngineApp().run()
