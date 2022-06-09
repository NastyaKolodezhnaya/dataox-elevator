import random


class Building:
    def __init__(self):
        self.floors_num = random.randint(5, 20)
        self.people_on_floor = self.generate_people_on_floor()
        self.people_unloaded = {floor: []
                                for floor in range(1, self.floors_num+1)}

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
        self.people_inside = []
        self.direction = 1  # direction value: 1 - up, -1 - down

        self.floor_on = 1
        self.top_floor = building.floors_num

        self.stage = 0

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
            elif self.direction == -1 and person < self.floor_on:
                self.people_inside.append(person)
                building.people_on_floor[self.floor_on].remove(person)
            else:
                person_index += 1

    def unload_people(self, building):
        while self.floor_on in self.people_inside:
            self.people_inside.remove(self.floor_on)
            building.people_unloaded[self.floor_on].append(self.floor_on)

    def move(self, building):
        # on the start floor
        self.print_stage_output(building)
        self.load_people(building)
        self.set_top_floor(building)

        self.floor_on += self.direction

        # on the 'between' floors
        while self.floor_on != self.top_floor:
            self.unload_people(building)
            self.load_people(building)
            self.set_top_floor(building)

            self.print_stage_output(building)
            self.floor_on += self.direction

        # on the top_floor
        self.unload_people(building)
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
        # if the floor_on value is boundary
        elif self.floor_on in (1, building.floors_num):
            self.direction *= -1
        # keep the previous direction if there is no people
        else:
            pass

    def print_stage_output(self, building):
        self.stage += 1
        print('Stage {}'.format(self.stage))
        print('{:>35} {:>33} {:>31}'.format(
                                    'People on the floor',
                                    'People inside the elevator',
                                    'People uploaded at the floor'))

        for floor in range(building.floors_num, 0, -1):
            people_on_floor_str = ' '.join(
                str(p) for p in building.people_on_floor[floor])

            if self.floor_on == floor:
                people_in_elevator = ' '.join(
                    str(p) for p in self.people_inside)
                match self.direction:
                    case 1:
                        direction_sign = '^'
                    case -1:
                        direction_sign = 'v'
            else:
                people_in_elevator = ''
                direction_sign = ' '

            people_unloaded_str = ' '.join(
                str(p) for p in building.people_unloaded[floor])

            print('{:2} | {:^29} | {} {:^29} | {:^29}'.format(
                floor,
                people_on_floor_str,
                direction_sign,
                people_in_elevator,
                people_unloaded_str))
        print('\n')


if __name__ == '__main__':
    b = Building()
    e = Elevator(b)

    while any(b.people_on_floor.values()):
        e.move(b)

    # print the final stage
    e.print_stage_output(b)
