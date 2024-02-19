import unittest
from PhEngineV2.space.phisic import calculate_gravitational_force
import glm
import sys

from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class UnitTestsPage(Screen):
    def __init__(self, **kwargs):
        """ Some main page """
        super().__init__(**kwargs)
        self.bl = BoxLayout(orientation='vertical', padding=10, spacing=50)
        
        self.header_lbl = Label(text='Unit Tests', size_hint=(1, 0.1), font_size=50)
        self.bl.add_widget(self.header_lbl)
        self.warning_lbl = Label(text='this tab is not fully ready, errors are possible', size_hint=(1, 0.05))
        self.bl.add_widget(self.warning_lbl)
        
        """ Buttons - actions """
        self.buttons_bl = BoxLayout(orientation='horizontal', spacing=10)
        
        self.run_btn = Button(
            text='back',
            on_press=self.on_main_screen,
            background_color=(0.9, 0.6, 0.1)
        )
        self.buttons_bl.add_widget(self.run_btn)
        
        self.settings_btn = Button(
            text='Run All tests',
            on_press=self.run_units,
            background_color=(0.3, 0.9, 0.1)
        )
        self.buttons_bl.add_widget(self.settings_btn)
        
        self.bl.add_widget(self.buttons_bl)  # add buttons on Main Layout
        
        self.add_widget(self.bl)  # add all on Screen
    
    def on_main_screen(self, instance):
        self.manager.current = 'main'
        
    def run_units(self, instance):
        old_stdout = sys.stdout
        
        new_stdout = sys.stdout
        runner = unittest.TextTestResult(new_stdout, True, verbosity=2)
        out = runner.startTest(TestPhysicalModule())
        
        sys.stdout = old_stdout
        
        print(runner.wasSuccessful())
        print(out)
        

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
