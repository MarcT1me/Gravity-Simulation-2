from kivy.uix.screenmanager import Screen

from kivy.uix.button import Button
from kivy.uix.label import Label

from core.source import *


class ConfigEditorPage(Screen):
    def __init__(self, **kwargs):
        """ Some main page """
        super().__init__(**kwargs)

        self.add_widget(DrawingWidget())
        # кнопка возврата на главный экран
        self.back_btn = Button(
            text='back', on_press=self.on_main_screen,
            background_color=(0.9, 0.6, 0.1),
            pos_hint={
                'x': 0.005,
                'y': 0.94
            }, size_hint=(0.05, 0.055)
        )
        self.add_widget(self.back_btn)
        
        # Заголовок
        self.header_lbl = Label(
            text='Sav changer', font_size=30,
            pos_hint={
                'x': 0.05,
                'y': 0.945
            }, size_hint=(0.15, 0.05)
        )
        self.add_widget(self.header_lbl)
        
        # предупреждение о не завершённости
        self.warning_lbl = Label(
            text='this tab is not fully ready, errors are possible',
            pos_hint={
                'x': 0.5,
                'y': 0.975
            }, size_hint=(0, 0)
        )
        self.add_widget(self.warning_lbl)
    
    def on_main_screen(self, instance): self.manager.current = 'main'
    
    def open_file(self, instance): self.manager.current = 'main'
    
    def save_file(self, instance): self.manager.current = 'main'
