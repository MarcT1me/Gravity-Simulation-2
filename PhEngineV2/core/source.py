import ctypes

from glm import vec4
from dataclasses import dataclass
import os

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line


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


@dataclass
class P:
    points: list
    width: int
    close: bool
    color: tuple


class DrawingWidget(FloatLayout):
    line_points = list()
    
    def __init__(self, **kwargs):
        super(DrawingWidget, self).__init__(**kwargs)
        
        with self.canvas.before:
            # Очищаем канву
            Color(0.25, 0.27, 0.26, 1)  # Черный цвет
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update, pos=self.update)
    
    @classmethod
    def add_line(cls, p): cls.line_points.append(p)
    
    def update(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
        self.canvas.clear()
        res = vec4(list(value)*2)
        with self.canvas:
            for p in DrawingWidget.line_points:
                Color(*p.color)
                # Нарисуем красную линию, которая будет масштабироваться вместе с окном
                Line(
                    points=p.points*res,
                    width=p.width, close=p.close
                )
