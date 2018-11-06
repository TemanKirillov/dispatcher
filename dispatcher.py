#!/usr/bin/python3 
''' 
Модуль с объектами для организации диспетчеризации
'''

class I:
    'imported objects'

    import collections
    import copy

class Dispatcher:

    def __init__(self):
        self.checkers = I.collections.OrderedDict()
        self.default = None
        self.key = None

    def bind_default(self, func):
        self.default = func
        return func

    def bind(self, checker, func=None):
        if func is None: #использовать как декоратор
            def wrapper(function):
                self.checkers[checker] = function
                return function
            return wrapper
        else:
            self.checkers[checher] = func
            return func

    def __call__(self, *args, **kwargs):
        for checker, func in self.checkers.items():
            if self.key is None:
                if checker(*args, **kwargs):
                    return func(*args, **kwargs)

            else:
                temp = self.key(*args, **kwargs)
                if checker(temp):
                    return func(*args, **kwargs)

        return self.default(*args, **kwargs)

class DataDispatcher(Dispatcher):
    
    def __call__(self, *args, **kwargs):
        kwargs['disp'] = self
        return super().__call__(*args, **kwargs)

    def copy(self):
        return I.copy.copy(self)

def test():
    fruit = Dispatcher()

    @fruit.bind_default
    def _(name, num):
        print('{}: {}'.format(name, num))

    def is_apples(name, num):
        if name.lower() == 'apples': return True
        else: return False

    def is_watermelon(name, num):
        if name.lower() == 'watermelon': return True
        else: return False

    def is_eggs(name, num):
        if name.lower() == 'eggs': return True
        else: return False

    @fruit.bind(is_apples)
    def _(name, num):
        print('{}: {} (кг)'.format(name, num))

    @fruit.bind(is_watermelon)
    def _(name, num):
        print('{}: {} (шт)'.format(name, num))

    @fruit.bind(is_eggs)
    def _(name, num):
        print('{}: {} (дес)'.format(name, num))

    examples = [('apples', 5), ('watermelon', 7), ('eggs', 9), ('oranges', 2)]

    for example in examples:
        fruit(*example)

def test_DataDispatcher():

    class MyDD(DataDispatcher):
        CONST = 5

    dd = MyDD()

    @dd.bind_default
    def _(name, num, disp):
        print('Default: {}: {}'.format(name, num * disp.CONST))

    copydd = dd.copy()
    copydd.CONST = 10

    dd('Apple', 1)
    copydd('Apple', 1)

if __name__ == '__main__':
    test()
    test_DataDispatcher()
