""" Collection of utilities for working with the application class.
"""
import pygame
from abc import abstractmethod

# App import
from PhEngineV2.messages import err_screen
import PhEngineV2


class App:
    """
    Main App class.
    The main parent class for creating logic and running it in the main loop
    
    FEATURES
        it does not have an initializer to simplify inheritance and management
    
    METHODS
        1) events: Event method. Needs to be overwritten after inheritance:
        2) update_app: Updating program data. Needs to be overwritten after inheritance:
        3) update_window: Rendering of the program window. Needs to be overwritten after inheritance
        4) run: the main cycle of the program
        
    CLASS FIELD
        running (bool): a variable is a condition for the operation of the main loop
    """
    running: bool = True

    @abstractmethod
    def events(self) -> None: ...
    @abstractmethod
    def update(self) -> None: ...
    @abstractmethod
    def render(self) -> None: ...
    
    def run(self) -> None:
        """ Run game.
        The method that starts the event loop.
        This is a while loop that uses the current variable in the App class field as a condition. 3 methods are
        called in the loop itself: events, update_app, update_window
        
        :return: Nothing
        :raises KeyboardInterrupt: if the cycle is not completed correctly. """
        while App.running:
            self.events()
            self.update()
            self.render()


def mainloop(app: App):
    """
    :param app: application class with initializer
    :return: Nothing
    :rtype: None
    :raise AssertionError: if there are problems with the argument
    """
    assert issubclass(app, App), 'Arg `QuantumGame` must be inherited by `QuantumCore.app.App`'
    
    while App.running and (App.running is not None):
        try:
            app().run()
        except Exception as err:
            App.running = err_screen.showWindow(err) if PhEngineV2.data.config.Settings.IS_RELEASE \
                else err_screen.showTraceback(err)
        finally:
            pygame.quit()