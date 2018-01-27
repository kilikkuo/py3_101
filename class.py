class Animal(object):
    def __init__(self, name='Unknown'):
        self.name = name
    def make_sound(self):
        print('')
    def getName(self):
        return self.name

class Dog(Animal):
    def __init__(self, name):
        Animal.__init__(self, name)
    def make_sound(self):
        print('WOOF ~~')
    def shake_hand(self):
        pass

class Cat(Animal):
    def __init__(self, name):
        # 遮蔽父類別的初始化, 若有使用到父類別屬性/方法, 會發生例外
        Animal.__init__(self, name)
        pass
    def make_sound(self):
        print('MEOw ~~')

a = Animal()
a.make_sound()
print('A name : {}'.format(a.getName()))
d = Dog('Lassie')
d.make_sound()
print('D name : {}, Instance of Animal : {}'.format(d.getName(), isinstance(d, Animal)))
c = Cat('Dora')
c.make_sound()
print('C name : {}'.format(c.getName()))