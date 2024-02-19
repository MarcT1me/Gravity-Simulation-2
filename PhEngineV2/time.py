""" Engine time counter
Total time management file for all engine functions
uses the time module

DESCRIPTION OF VARIABLES
dt - Время между 2-мя итерациями цикла App
start - Временная отметка с запуска программы (import)

roster - Список счётчиков
 """
import time

dt: float = 0
start: float = time.time()

roster: dict = {
}


def timer(time_list, name: str, cooldown: float):
    """ A timer is a function that decides whether a time cycle is suitable for performing some kind of action
    tied to waiting for time """
    current_time = time.time()
    if isinstance(time_list, dict):
        if current_time - time_list[name] >= cooldown:
            time_list[name] = current_time
            return True
        return False
    else:
        if current_time - time_list.name >= cooldown:
            time_list.name = current_time
            return True
        return False


class Animation:
    """ an unfinished class to mitigate changing the value of a variable """
    roster = set()
    
    def __init__(self, *, duration: float, **kwargs):
        """ Animate your variables """
        self.obj: object = None
        self.start_value = None
        self.start_time: float = None
        
        assert len(kwargs) != 1, AttributeError('too many/few attributes')
        self.name, self.end_value = kwargs.items()
        self.duration = duration
    
    def __update__(self):
        """ method, called every frame """
        cur_time = time.time() - self.start_time
        t = cur_time/self.duration
        t = min(max(t, 0), 1)
        value = self.start_value + (self.end_value - self.start_value)*t
        self.obj.__setattr__(self.name, value)
    
    def start(self, obj: object):
        """ start anim on the object """
        self.start_time = time.time()
        self.obj = obj
        self.start_value = obj.__getattribute__(self.name)
        
        Animation.roster.add(self)
