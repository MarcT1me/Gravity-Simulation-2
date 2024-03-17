import unittest
from space.phisic import calculate_gravitational_force
import glm
import sys
import io
from threading import Thread

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from core.source import *
from data.config import APPLICATION_PATH, APPLICATION_VERSION, APPLICATION_NAME

standard_ti_text = f"""Unit Test out
dir: `{APPLICATION_PATH}`
name: {APPLICATION_NAME}\tversion: {APPLICATION_VERSION}

________________________________________________________

"""


class UnitTestsPage(Screen):
    def __init__(self, **kwargs):
        """ Some main page """
        super().__init__(**kwargs)

        DrawingWidget.add_line(P(points=[0, 0.93, 1, 0.93], width=2, close=False, color=(0.45, 0.47, 0.36, 1)))
        DrawingWidget.add_line(P(points=[0.5, 0.8, 0.5, 0.93], width=2, close=False, color=(0.45, 0.47, 0.36, 1)))
        DrawingWidget.add_line(P(points=[0, 0.8, 1, 0.8], width=3, close=False, color=(0.45, 0.47, 0.36, 1)))
        
        self.add_widget(DrawingWidget())
        """ Верхнее табло """
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
            text='Unit Tests', font_size=30,
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
        # self.add_widget(self.warning_lbl)
        
        # запуск тестов
        self.run_btn = Button(
            text='Run',
            background_color=(0.3, 0.9, 0.1),
            pos_hint={
                'x': 0.945,
                'y': 0.945
            }, size_hint=(0.05, 0.05)
        )
        self.run_btn.bind(
            on_press=lambda *args, **kwargs: Thread(
                target=self.run_units, args=args, kwargs=kwargs
            ).start()
        )
        self.add_widget(self.run_btn)
        
        # очищение онсоли
        self.clear_btn = Button(
            text='Clear console',
            on_press=self.clear_output,
            background_color=(0.1, 0.3, 0.9),
            pos_hint={
                'x': 0.84,
                'y': 0.945
            }, size_hint=(0.1, 0.05)
        )
        self.add_widget(self.clear_btn)
        
        """ Надписи статуса """
        self.status = Label(
            text='there is no result', font_size=30,
            pos_hint={
                'x': 0.05,
                'y': 0.81
            }, size_hint=(0.45, 0.12)
        )
        self.add_widget(self.status)
        
        self.failures_console = TextInput(
            text='There are no mistakes',
            auto_indent='bash',
            readonly=True,
            background_color=(0.15, 0.15, 0.1),
            hint_text_color=(0.3, 0.4, 0.4),
            cursor_color=(0.9, 0.9, 0.9),
            cursor_width=3,
            pos_hint={
                'x': 0.5,
                'y': 0.81
            }, size_hint=(0.5, 0.12)
        )
        self.failures_console.foreground_color = (0.9, 0.9, 0.9)
        self.failures_console.multiline = False
        self.add_widget(self.failures_console)
        
        """ консоль да и только """
        # консольный вывод
        self.console = TextInput(
            text=standard_ti_text,
            auto_indent='bash',
            readonly=True,
            background_color=(0.15, 0.15, 0.1),
            hint_text_color=(0.3, 0.4, 0.4),
            cursor_color=(0.9, 0.9, 0.9),
            cursor_width=3,
            size_hint=(1, 0.8)
        )
        self.console.pos = (0, 0)
        self.console.foreground_color = (0.9, 0.9, 0.9)
        self.console.multiline = False
        self.add_widget(self.console)
    
    def on_main_screen(self, instance): self.manager.current = 'main'
    
    def clear_output(self, instance):
        self.console.text = standard_ti_text
        self.console.scroll_y = 1
        self.failures_console.text = 'cleared'
    
    def update_console(self, console, text): console.text = text
    
    def run_units(self, instance):
        old_stdout = sys.stdout
        
        new_stdout = io.StringIO()  # создание вывода консоли
        sys.stdout = new_stdout  # прикрепление консоли к новому выводу
        
        runner = unittest.TextTestRunner(stream=new_stdout, verbosity=2)
        result = runner.run(unittest.makeSuite(TestPhysicalModule))  # запуск теста
        
        sys.stdout = old_stdout  # возвращение вывода на прошлые значения
        
        """ изменение текстовых переменных в UI """
        success = result.wasSuccessful()
        self.status.text = f'was successful: {success}'
        failures_text = None
        if success:
            self.console.cursor_color = (0.2, 0.9, 0.2)

            failures_text = 'There are no mistakes'
        else:
            self.console.cursor_color = (0.9, 0.9, 0.1)
            
            failures_text = f'failed tests: {len(result.failures) + len(result.errors)}'
            
            failures_text += '\ntests failed: '
            for test, _ in result.failures:
                failures_text += f'{test}; '
                
            failures_text += '\nended with an error: '
            for test, _ in result.errors:
                failures_text += f'{test}; '
        
        Clock.schedule_once(
            lambda dt: self.update_console(
                self.failures_console,
                failures_text
            )
        )
        
        Clock.schedule_once(
            lambda dt: self.update_console(
                self.console,
                self.console.text + new_stdout.getvalue() + '\n'
            )
        )


class TestPhysicalModule(unittest.TestCase):
    test_outputs = {}
    
    def test_force(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(1, 1), 1, 1)
        self.assertEqual(
            res,
            glm.vec2(2.3597213948366865e-11, 2.3597213948366865e-11)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_reversal_coordinates(self):
        res = calculate_gravitational_force(glm.vec2(1, 1), glm.vec2(0, 0), 1, 1)
        self.assertEqual(
            res,
            glm.vec2(-2.359721394836686e-11, -2.3597213948366865e-11)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_zero_mass(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(1, 1), 0, 1)
        self.assertEqual(
            res,
            glm.vec2(0.0, 0.0)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_same_position(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(0, 0), 1, 1)
        self.assertEqual(
            res,
            glm.vec2(0.0, 0.0)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_large_mass(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(1, 1), 1, 64)
        self.assertEqual(
            res,
            glm.vec2(1.5102216926954793e-09, 1.5102216926954793e-09)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_large_distance(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(10, 10), 1, 1)
        self.assertEqual(
            res,
            glm.vec2(2.3597213948366865e-13, 2.3597213948366865e-13)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_negative_mass(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(1, 1), -1.0, 1.0)
        self.assertEqual(
            res,
            glm.vec2(-2.3597213948366865e-11, -2.3597213948366865e-11)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_all_negative_mass(self):
        res = calculate_gravitational_force(glm.vec2(0, 0), glm.vec2(1, 1), -1.0, -1.0)
        self.assertEqual(
            res,
            glm.vec2(2.359721394836686e-11, 2.3597213948366865e-11)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res
    
    def test_real_data(self):
        res = calculate_gravitational_force(glm.vec2(10, 15555), glm.vec2(15, -155544), 4544456, 464645)
        self.assertEqual(
            res,
            glm.vec2(1.4068133618748406e-13, -4.814087188050797e-09)
        )
        self.test_outputs[sys._getframe().f_code.co_name] = res


if __name__ == '__main__':
    unittest.main()
