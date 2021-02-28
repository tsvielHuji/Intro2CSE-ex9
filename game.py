from board import *
from car import *
from sys import argv as parameters
from sys import exit as exit_game
from helper import *
# Constants
VERTICAL, HORIZONTAL = 0, 1
MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT = "u", "d", "l", "r"
VALID_NAMES = {"Y", "B", "O", "W", "G", "R"}
GAME_OVER = "!"
VALID_DIRECTIONS = {MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT}
MAKE_A_MOVE = "Make your move (ex: O,u):\n"


class Game:
    """
    Add class description here
    """
    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        self.__board = board
        self.__filename = parameters[1]  # Uncomment for Command
        # self.__filename = DEFAULT_JSON_PATH_NAME # Uncomment for debugging

        file = load_json(self.__filename)
        keys = list(file.keys())
        values = list(file.values())
        self.__car_list = []
        for i in range(len(keys)):  # Create Cars
            car = Car(keys[i], values[i][0], values[i][1], values[i][2])
            if car.get_name() not in VALID_NAMES:
                continue
            self.__car_list.append(car)
            i += 1
        for car in self.__car_list:  # add all cars to board
            self.__board.add_car(car)
        print(self.__board)
        self.play()

    def __check_move(self, car_name, movekey):
        """Check possible moves for car"""
        possible_move = [item[1] if item[0] == car_name else None
                         for item in self.__board.possible_moves()]
        if movekey not in possible_move:
            return False
        return True

    def __single_turn(self, move):
        """
        A single turn recursive function
        :return True if win, False if not
        """
        name, movekey = move[0], move[1]
        if movekey not in VALID_DIRECTIONS:
            print("Invalid move key, valid choices are ",
                  ","  .join(VALID_DIRECTIONS))
            return
        if name not in VALID_NAMES:
            print("You are trying to move an invalid car")
            return
        if not self.__check_move(name, movekey):
            print("Can't move car in this direction")
            return
        self.__board.move_car(str(move[0]).upper(), str(move[1]).lower())

    def __is_win(self):
        """
        :param target: tuple - winning coordinate
        :return: true if win, false if not
        """
        row, col = self.__board.target_location()
        target = self.__board.cell_content((row,col))
        prev = self.__board.cell_content((row, col-1))
        if target and prev:
            return True
        return False

    def play(self):
        """The main driver of the Game. Manages the game until completion"""
        print("Welcome to Rush-hour")
        user_input = input(MAKE_A_MOVE)
        print(self.__board)
        print(user_input)
        while user_input != GAME_OVER:
            if user_input == "" or not(len(user_input) in range(2, 4)):
                print("Please provide a move and car to move")
                print(self.__board)
                user_input = input(MAKE_A_MOVE)
                continue
            move = tuple(user_input.split(","))
            self.__single_turn(move)
            print(self.__board)
            if self.__is_win():
                # if __win returns print win message and break the game loop
                print("You win")
                break
            user_input = input(MAKE_A_MOVE) # Wait for next users input
            # If nothing breaks the turn, iterate to next one

        # If game loop was terminated
        print("Thank you and Goodbye")
        return


def main():
    """
    This is the main function of the program which calls and combines all the
    functions of the program.
    This function of the program handles its integrity.
    :return: None if fail to run game
    """
    try:
        if len(parameters) <= 1 or len(parameters) > 2:
            # if not given exact amount of parameters
            raise ValueError
        new_board = Board()
        Game(new_board)
    except ValueError:  # Should be Manually Raised
        print("Not Enough Arguments was entered. make sure to enter correct",
              "filename and path")
        return
    except FileNotFoundError:   # If config file not found except FileNotFound
        print("Python FileNotFound Error")
        print("Can't load game because car config File was not found")
        return
    exit_game()  # sys.exit


if __name__ == "__main__":
    main()
