import random


class Building():
    def __init__(self):
        self.floors_num = random.randint(5, 20)
        self.people_at_floor = {}

    def generate_people_at_floor(self):
        # a person value == the floor he needs to get to
        for i in range(1, self.floors_num + 1):
            floors_list = list(range(1, self.floors_num+1))
            floors_list.remove(i)
            self.people_at_floor[i] = [random.choice(floors_list)
                                       for _ in range(random.randint(0, 10))]


class Elevator():
    def __init__(self):
        self.capacity = 5
        self.floor_at = 1
        self.people_inside = []
        # direction value: 1 - up, 0 - down
        self.direction = 1
        self.top_floor = 1

    def load_people(self, building):
        person_index = 0

        while len(self.people_inside) < self.capacity and \
                person_index < len(building.people_at_floor[self.floor_at]):
            person = building.people_at_floor[self.floor_at][person_index]
            if self.direction == 1 and person > self.floor_at:
                self.people_inside.append(person)
                building.people_at_floor[self.floor_at].remove(person)
            elif self.direction == 0 and person < self.floor_at:
                self.people_inside.append(person)
                building.people_at_floor[self.floor_at].remove(person)
            else:
                person_index += 1

        # case when the elevator is empty
        # self.top_floor = max(self.people_inside)

    def unload_people(self, building):
        while self.floor_at in self.people_inside:
            self.people_inside.remove(self.floor_at)

    def move_up(self, building):
        while self.people_inside:
            self.floor_at = min(self.people_inside)
            self.unload_people(self, building)
            self.load_people(self, building)

    def move_down(self):
        self.direction = 0
        pass


def print_people_at_floors(obj):
    for key, value in obj.people_at_floor.items():
        print(f'Floor {key}: {value}')


if __name__ == '__main__':
    b = Building()
    b.generate_people_at_floor()
    print(dir(b))
    print_people_at_floors(b)

    e = Elevator()
    e.load_people(b)
    print(e.people_inside)
