import random


class Building:
    def __init__(self):
        self.floors_num = random.randint(5, 20)
        self.people_on_floor = self.generate_people_on_floor()
        self.people_unloaded = {}

    def generate_people_on_floor(self):
        # a person value == the floor he needs to get on
        people_dict = {}
        for i in range(1, self.floors_num + 1):
            floors_list = list(range(1, self.floors_num+1))
            floors_list.remove(i)
            people_dict[i] = [random.choice(floors_list)
                              for _ in range(random.randint(0, 10))]
        return people_dict


class Elevator:
    def __init__(self, building):
        self.capacity = 5
        self.floor_on = 1
        self.people_inside = []
        self.direction = 1  # direction value: 1 - up, -1 - down
        self.top_floor = building.floors_num

    def set_top_floor(self, building):
        if self.people_inside:
            if self.direction == 1:
                self.top_floor = max(self.people_inside)
            else:
                self.top_floor = min(self.people_inside)
        else:
            if self.direction == 1:
                self.top_floor = building.floors_num
            else:
                self.top_floor = 1

    def load_people(self, building):
        person_index = 0

        # check available place & index increment
        while len(self.people_inside) < self.capacity and \
                person_index < len(building.people_on_floor[self.floor_on]):
            person = building.people_on_floor[self.floor_on][person_index]
            if self.direction == 1 and person > self.floor_on:
                self.people_inside.append(person)
                building.people_on_floor[self.floor_on].remove(person)
            elif self.direction == 0 and person < self.floor_on:
                self.people_inside.append(person)
                building.people_on_floor[self.floor_on].remove(person)
            else:
                person_index += 1

    def unload_people(self):
        while self.floor_on in self.people_inside:
            self.people_inside.remove(self.floor_on)

        # self.print_stage_output()
        # add accepting 'building' arg

    def move(self, building):
        # on the start floor
        self.load_people(building)
        self.set_top_floor(building)

        # on the 'between' floors
        for floor in range(self.floor_on+1, self.top_floor,
                           self.direction):
            self.floor_on = floor
            self.unload_people()
            self.load_people(building)
            self.set_top_floor(building)

        # on the top_floor
        self.floor_on += self.direction
        self.unload_people()
        self.set_direction(building)

    def set_direction(self, building):
        if building.people_on_floor[self.floor_on]:
            people_up = [p for p in building.people_on_floor[self.floor_on]
                         if p > self.floor_on]
            people_down = [p for p in building.people_on_floor[self.floor_on]
                           if p < self.floor_on]
            if len(people_up) > len(people_down):
                self.direction = 1
            elif people_down > people_up:
                self.direction = -1
            else:
                pass
        # keep the previous direction if there is no people
        else:
            pass

    def print_stage_output(self):
        # values we need to output/
        # (cycle count) floor_on, people_on_floor, people_inside,
        #               people_unloaded, direction
        pass


def print_people_at_floors(obj):
    for key, value in obj.people_on_floor.items():
        print(f'Floor {key}: {value}')


if __name__ == '__main__':
    b = Building()
    e = Elevator(b)
    print_people_at_floors(b)

    while b.people_on_floor:
        e.move(b)
