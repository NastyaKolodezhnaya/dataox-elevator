import random


class Building():
    def __init__(self):
        # set a random number of floors:
        self.floors_num = random.randint(5, 20)
        # set a list of [random number of people] for each floor:
        for i in range(1, self.floors_num + 1):
            setattr(self, str(i), [random.randint(1, self.floors_num) for _ in range(random.randint(0, 10))])


class Elevator():
    pass


b = Building()
print(b.floors_num)
print(dir(b))
