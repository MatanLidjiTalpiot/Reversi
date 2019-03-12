import dill
class Pick:

    def __init__(self, name, number):
        self.number = number
        self.name = name
    def set_number(self, other_number):
        self.number = other_number

    def set_name(self, other_name):
        self.name = other_name

    def print(self):
        print(self.name, ", ", self.number)
    f = lambda self : print(self.number)
    def g(self):
        self.f()

p_yam = Pick("Yam", 1)
p_ripp = Pick("Ripp", 2)
p_droro = Pick("Droro", 3)
p_palti = Pick("Palti", 4)
p_lidji = Pick("Lidji", 5)
p_benny = Pick("Benny", 6)
with open('pklFiles/'+p_yam.name, 'wb') as output:
    dill.dump(p_yam, output, dill.HIGHEST_PROTOCOL)
del p_yam

with open('pklFiles/Yam', 'rb') as input:
    other_obj = dill.load(input)
    other_obj.print()
