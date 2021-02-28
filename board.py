BOARD_RANGE = range(7)
EMPTY = "_"
EXIT = "E"
VERTICAL, HORIZONTAL = 0, 1
MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT = "u", "d", "l", "r"
# Message text:
INVALID_COORDINATE = "You had entered an invalid Coordinate"
CAUSE_THE_CAR = "Causes the car to go"


class Board:
    """
    The class creates a board for a new game and updates it accordingly to the
    users input
    """

    def __init__(self):
        initiate_board = []
        self.__cars_cache = []
        for j in BOARD_RANGE:
            initiate_board.append([EMPTY for i in BOARD_RANGE])
        initiate_board[self.target_location()[0]].insert(
            self.target_location()[1], EXIT)
        self.__board = initiate_board

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        return '\n'.join(['\t'.join([str(cell) for cell in row])
                          for row in self.__board])

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        result = []
        for i in BOARD_RANGE:
            for j in BOARD_RANGE:
                result.append((i, j))
        result.append(self.target_location())
        return result

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file,
        # the return value could be
        # [('O','d',"some description"),
        # ('R','r',"some description"),
        #

        moves_list = []
        for single_car in self.__cars_cache:
            for move in single_car.possible_moves().keys():
                next_cell = single_car.movement_requirements(move)[0]
                if next_cell in self.cell_list() and self.cell_content(
                        next_cell) is None:
                    moves_list.append((single_car.get_name(), move,
                                       (single_car.possible_moves())[move]))
        return moves_list

    def target_location(self):
        """
        This function returns the coordinates of the location which
        is to be filled for victory.
        :return: (row,col) of goal location
        """
        return 3, 7

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if coordinate in self.cell_list():
            if self.__board[coordinate[0]][coordinate[1]] == EMPTY or \
                    self.__board[coordinate[0]][coordinate[1]] == EXIT:
                return None
            else:
                return self.__board[coordinate[0]][coordinate[1]]
    """        else:
            return INVALID_COORDINATE"""

    def check_intersections(self, coordinates):
        """
        The functions checks if a given car, intersecting another car by
        checking the intended cells
        :param coordinates:
        :return: False for yes, True for no
        """
        for coordinate in coordinates:
            if self.cell_content(coordinate) is not None:
                return False
        return True

    def check_car_exist(self, car_name):
        """
        The function validate if the car is in the game already
        :param car_name: The name of the car we want to check
        :return: False for yes, True for name
        """
        for car in self.__cars_cache:
            if car_name == car.get_name():
                return True  # Car exists
        return False  # Car do not exist

    def check_valid_moves(self, coordinates):
        """
        Check if the car is in the range of the board
        :param coordinates:
        :return: True if yes, No if it flies to the moon
        """
        for coordinate in coordinates:  # Test if car in the range of the board
            if coordinate not in self.cell_list():
                return False
        return True

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_name = car.get_name()
        coordinates = car.car_coordinates()
        if self.check_car_exist(car_name):  # if Car exist
            return False
        if not self.check_valid_moves(coordinates):
            return False
        if not self.check_intersections(coordinates):
            return False
        self.__cars_cache.append(car)
        for cell in car.car_coordinates():
            self.__board[cell[0]][cell[1]] = car.get_name()
        return True

    def __update_board(self, car, old_tail):
        """Update board according to old tail(tuple) of a car"""
        for cell in car.car_coordinates():
            self.__board[cell[0]][cell[1]] = car.get_name()
            self.__board[old_tail[0][0]][old_tail[0][1]] = EMPTY
        return True

    def __make_car_move(self,movekey, car, old_tail):
        """Make car object move to movekeys direction using old tail tuple"""
        if movekey == MOVE_UP:  # Moves the car upwards
            old_tail.append(car.car_coordinates()[-1])  # Old Coords
            car.move(MOVE_UP)  # Make a move
            self.__update_board(car, old_tail)  # Update the board
        if movekey == MOVE_DOWN:  # Moves the car downward
            old_tail.append(car.car_coordinates()[0])
            car.move(MOVE_DOWN)  # Make a move
            self.__update_board(car, old_tail)  # Update the board
        if movekey == MOVE_RIGHT:  # Moves the car in right direction
            old_tail.append(car.car_coordinates()[0])  # Old Coords
            car.move(MOVE_RIGHT)  # Make a move
            self.__update_board(car, old_tail)  # Update the board
        if movekey == MOVE_LEFT:  # Moves the car in left direction
            old_tail.append(car.car_coordinates()[-1])  # Old coords
            car.move(MOVE_LEFT)  # Make a move
            self.__update_board(car, old_tail)  # Update the board

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        old_tail = []  # Cache for old coordinates
        # Check if given car name is in possible moves list:
        # If all is cool make the appropriate move with for loop
        if len(self.__cars_cache) == 0:
            return False
        possible_move = [item[1] if item[0] == name else None
                         for item in self.possible_moves()]
        if movekey not in possible_move:
            return False

        for car in self.__cars_cache:
            # Checks for the function:
            if name == car.get_name():  # Check if we are talking about the
                self.__make_car_move(movekey, car, old_tail)
        return True