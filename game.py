import json
import re


class Player:

    def __init__(self, name: str, points: int = 0):
        self.name = name
        self.points = points

    def add_point(self):
        self.points += 1

    def save_points(self):
        #Create a dictionary
        dict_list = []
        points_dict = {}
        points_dict["player"] = self.name
        points_dict["points"] = self.points
        dict_list.append(points_dict)
        with open("players.json", "w") as f:
            json.dump(dict_list, f)


class Score:

    def __init__(self, file_name: str):
        with open(file_name, "r") as f:
            self.players_list = []
            data = []
            for line in f:
                player_data = line.strip().split(',')
                data.append({
                    "player": player_data[0],
                    "points": int(player_data[1])
                })

            for d in data:
                self.players_list.append(Player(d["player"], d["points"]))

    def search_player(self, name: str):
        for p in self.players_list:
            if p.name == name:
                return p
        return None

    def update_player(self, player: Player):
        for p in self.players_list:
            if p.name == player.name:
                p.points = player.points
                return
        print("Player not found.")

    def save_points(self):
        with open("players.txt", "w") as f:
            data = []
            for p in self.players_list:
                data.append(p.name + ', ' + str(p.points))

            for item in data:
                f.write("%s\n" % item)

    def add_player(self, player: Player):
        self.players_list.append(player)


class Question:

    def __init__(self, options: list, question: str, answer: str):
        self.options = options
        self.question = question
        self.answer = answer

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_options(self):
        return self.options

    def __str__(self) -> str:
        formated_question = self.question + "\n"

        #Append all the options
        for option in self.options:
            formated_question = formated_question + option + ") " + self.options[
                option] + "\n"
        return formated_question

    def check_answer(self, answer: str) -> bool:
        if answer == self.answer:
            return True
        return False

    def validate_answer(self, answer: str) -> bool:
        possible_answers = ["a", "b", "c", "d"]
        if answer in possible_answers:
            return True
        print(str(answer) + " is not a valid answer!")
        return False


class Game:

    def __init__(self):
        #Load the questions
        with open("questions.json", "r") as f:
            questions_json = json.load(f)
            self.question_list = []
            for question in questions_json:
                self.question_list.append(
                    Question(question["options"], question["question"],
                             question["answer"]))
        self.score_board = Score("players.txt")
        self.player = None

    def play(self):
        #Load player info
        name = self.name_input()

        #Load player data
        self.load_player_data(name)

        #Ask the player for the questions
        self.ask_questions()

        #Print result
        self.print_result()

        #Save result
        self.save_result()

    def name_input(self) -> str:
        while (True):
            name = input("Please enter your name: ")
            if (self.check_name(name)):
                return name
            else:
                print("Invalid name. Please enter a valid name.")

    def load_player_data(self, name: str):
        self.player = self.score_board.search_player(name)
        if self.player is None:
            print("Welcome " + name + "!\n")
            self.player = Player(name)
            self.score_board.add_player(self.player)
        else:
            print("Welcome back " + name + "!\n")
            if (self.player.points == 1):
                print("Last time you had " + str(self.player.points) +
                      " point. Let's try again.")
            else:
                print("Last time you had " + str(self.player.points) +
                      " points. Let's try again.")
            #Reset points
            self.player.points = 0

    def ask_questions(self):
        for question in self.question_list:
            #While the answer is not valid, repeat it:
            while True:
                print(question)
                answer = input("Please enter your answer: ")
                if question.validate_answer(answer):
                    break

            #Check if the answer is correct:
            if question.check_answer(answer):
                print("Correct!")
                #Add a point to the player:
                self.player.add_point()
            else:
                print("Incorrect!\n")

    def print_result(self):
        print("Your points are: " + str(self.player.points) + "/" +
              str(len(self.question_list)))

    def save_result(self):
        #Update the score board:
        self.score_board.update_player(self.player)

        #Save the player's points:
        self.score_board.save_points()

    def check_name(self, name: str) -> bool:
        if (len(name) >= 2 and len(name) <= 50) and re.match(
                r'^[A-Z][a-z]+$', name):
            return True
        else:
            return False
