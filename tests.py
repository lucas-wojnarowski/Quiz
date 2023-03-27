import game


class Test_Game:

    def test_check_name(self):
        Game = game.Game()

        #given
        names = ["John", "john", "J", "joHn", "0jo", "Źo"]

        #when
        result = []
        for name in names:
            result.append(Game.check_name(name))

        #then
        assert result == [True, False, False, False, False, False]

    def test_validate_answer(self):

        #given
        options = ["a", "b", "c", "g", "A", "1"]
        question_text = "What is your favorite color?"
        answer = "red"

        question = game.Question(question_text, options, answer)

        #when
        result = []
        for option in options:
            result.append(question.validate_answer(option))

        #then
        assert result == [True, True, True, False, False, False]

    def test_search_player(self):
        #given
        score_board = game.Score("players.txt")
        player_name = "Lucas"

        #when
        result = score_board.search_player(player_name)

        #then
        assert result.name == player_name
