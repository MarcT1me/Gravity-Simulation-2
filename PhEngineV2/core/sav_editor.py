
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from threading import Thread

from core.source import *


class SavReaderPage(Screen):
    def __init__(self, **kwargs):
        """ Some main page """
        super().__init__(**kwargs)

        self.add_widget(DrawingWidget())
        # кнопка возврата на главный экран
        self.back_btn = Button(
            text='back', on_press=self.on_main_screen,
            background_color=(0.9, 0.6, 0.1),
            pos_hint={
                'x': 0.945,
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
        
        self.file_btn = Button(
            text='File',
            on_press=self.file_font,
            pos_hint={
                'x': 0.005,
                'y': 0.94
            }, size_hint=(0.05, 0.05)
        )
        self.add_widget(self.file_btn)
        
        """ File folder on UI """
        self.file_fold = BoxLayout(
            size_hint = (0.2, 0.2),
            pos_hint={
                'x': 0.01,
                'y': 0.74
            },
            orientation='vertical'
        )
        
        # чтение пути
        self.path = TextInput(
            text='path/to/your/sav.sav',
            background_color=(0.15, 0.15, 0.1),
            hint_text_color=(0.3, 0.4, 0.4),
            cursor_color=(0.9, 0.9, 0.9),
            cursor_width=3,
            size_hint=(1, 0.1)
        )
        self.path.foreground_color = (0.9, 0.9, 0.9)
        self.path.multiline = False
        self.file_fold.add_widget(self.path)
        
        # кнопка чтения
        self.read_btn = Button(
            text='read',
            background_color=(0.1, 0.3, 0.9),
            size_hint=(1, 0.1)
        )
        self.read_btn.bind(
            on_press=lambda *args, **kwargs: Thread(
                target=self.open_file, args=args, kwargs=kwargs
            ).start()
        )
        self.file_fold.add_widget(self.read_btn)

        self.save_btn = Button(
            text='save',
            on_press=self.save_file,
            background_color=(0.3, 0.9, 0.1),
            size_hint=(1, 0.1)
        )
        self.file_fold.add_widget(self.save_btn)
        self.file_fold.enable = True
        
    def on_main_screen(self, instance): self.manager.current = 'main'

    def file_font(self, instance):
        self.file_fold.enable = not self.file_fold.enable
        
        if self.file_fold.enable:
            self.remove_widget(self.file_fold)
        else:
            self.add_widget(self.file_fold)
    
    def open_file(self, instance): self.manager.current = 'main'
    
    def save_file(self, instance): self.manager.current = 'main'
