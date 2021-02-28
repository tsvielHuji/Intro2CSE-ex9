VERTICAL, HORIZONTAL = 0, 1
MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT = "u", "d", "l", "r"
VALID_NAMES = {"Y", "B", "O", "W", "G", "R"}

# Message text:
INVALID_ORIENTATION = "You had entered an invalid orientation"
CAUSE_THE_CAR = "Causes the car to go"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation
        self.__location_h = location[1]
        self.__location_v = location[0]

    def car_coordinates(self):
        """
        :return: A list of coordinates(tuples) the car is in
        """
        output = []
        if self.__orientation is VERTICAL:  # Case for Vertical Orientation
            for v in range(self.__length):
                output.append((self.__location_v + v, self.__location_h))
        elif self.__orientation is HORIZONTAL:  # Case for Vertical Orientation
            for h in range(self.__length):
                output.append((self.__location_v, self.__location_h + h))
        else:
            return INVALID_ORIENTATION
        return output

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        result = {}
        if self.__orientation is VERTICAL:  # Case for Vertical Orientation
            result['u'] = CAUSE_THE_CAR + UP
            result['d'] = CAUSE_THE_CAR + DOWN
        if self.__orientation is HORIZONTAL:  # Case for Vertical Orientation
            result['l'] = CAUSE_THE_CAR + LEFT
            result['r'] = CAUSE_THE_CAR + RIGHT
        return result

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for
        this move to be legal.
        """
        result = []
        if movekey == MOVE_UP:
            result.append((int(self.car_coordinates()[0][0]) - 1,
                           self.car_coordinates()[0][1]))
        if movekey == MOVE_DOWN:
            result.append(((int(self.car_coordinates()[-1][0])) + 1,
                           self.car_coordinates()[-1][1]))
        if movekey == MOVE_LEFT:
            result.append((self.car_coordinates()[0][0],
                           int(self.car_coordinates()[0][1]) - 1))
        if movekey == MOVE_RIGHT:
            result.append((self.car_coordinates()[-1][0],
                           int(self.car_coordinates()[-1][1]) + 1))
        return result

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """

        # Tests for restricted movesr,r
        if self.__orientation == HORIZONTAL \
                and movekey not in [MOVE_RIGHT, MOVE_LEFT]:
            return False
        if self.__orientation == VERTICAL \
                and movekey not in [MOVE_UP, MOVE_DOWN]:
            return False

        # Moves the car
        if movekey == MOVE_RIGHT:  # Move Right
            self.__location = (self.__location_v, self.__location_h + 1)
        if movekey == MOVE_LEFT:  # Move Left
            self.__location = (self.__location_v, self.__location_h - 1)
        if movekey == MOVE_UP:  # Move up
            self.__location = (self.__location_v - 1, self.__location_h)
        if movekey == MOVE_DOWN:  # Move Down
            self.__location = (self.__location_v + 1, self.__location_h)
        self.__location_v, self.__location_h = self.__location
        return True  # If everything is cool, return

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
