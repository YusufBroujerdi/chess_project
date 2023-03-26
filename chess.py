import pickle





def check_is_move(move : str) -> bool:
    """Performs rudimentary checks on string to ensure it looks like a valid chess move in the PGN.
    
    Warning: This function may yield false positives."""

    #Take out notation for captures, checks and checkmates.
    move = ''.join( [char for char in move if char not in {'#', '+', 'x'}] )


    #Check to see if the move has enough characters to constitute a move.
    if len(move) < 2:
        return False

    #A separate check to see if the move describes castling.
    if move == 'O-O-O' or move == 'O-O':
        return True

    #Check if the front starts with a valid piece (i.e. queen, king, pawn, etc.).
    if ord(move[0]) not in range(97, 105) and move[0] not in {'Q', 'K', 'B', 'N', 'R'}:
        return False

    #Check if the back ends with a valid coordinate (i.e. 'h2', 'a4', etc.).
    if ord(move[-2]) not in range(97, 105) or ord(move[-1]) not in range(49, 57):
        return False
    
    return True



def check_is_move_and_warn(move : str) -> bool:
    """Performs rudimentary checks on string to ensure it looks like a valid chess move in the PGN. Warns if it is not.
    
    Warning: This function may yield false positives."""

    result = check_is_move(move)

    if not result:
        print("Invalid move format found.")

    return result



def split_string_list(string_list : list, *separators):
    '''Splits a list of strings into a larger list of strings using the given separators.'''

    #Takes a list of strings and returns a list of lists, where each list is a string split by a given separator.
    list_split_before_flattening = lambda list, separator : [element.split(separator) for element in list]

    #Flattens a list of lists.
    flatten = lambda list : [subelement for element in list for subelement in element]

    #Splits a list of strings into a larger list of strings using the given separator.
    lsplit = lambda list, separator : flatten(list_split_before_flattening(list, separator))

    for separator in separators:

        string_list = lsplit(string_list, separator)
    
    return string_list





class Chess_moves:
    """Object for holding and manipulating lists of chess moves."""

    list_of_moves = []


    
    def __init__(self, *moves_in_algebraic_notation : str):
        """Initializer can be initialized with one string of moves or multiple. Initializer can directly accept strings of unformatted PGN from Chess.com."""

        for move_sequence in moves_in_algebraic_notation:

            formatted_move_sequence : list = split_string_list([move_sequence], ',', ' ', '\n', '\r')
            formatted_move_sequence = [move for move in formatted_move_sequence if check_is_move(move)]
            self.list_of_moves = self.list_of_moves + formatted_move_sequence


    
    def __getitem__(self, key):
        """Extends standard list behaviour to Chess_moves."""
        return self.list_of_moves[key]


    
    def __setitem__(self, key, value):
        """Extends standard list behaviour to Chess_moves."""

        if not check_is_move_and_warn(value):
            return

        self.list_of_moves[key] = value


    
    def __delitem__(self, key):
        """Extends standard list behaviour to Chess_moves."""
        del self.list_of_moves[key]


    
    def add_move(self, *moves : str):
        """Adds moves specified in the argument."""

        for move in moves:

            if not check_is_move_and_warn(move):
                return
            
            self.list_of_moves.append(move)





class Chess_game(Chess_moves):
    """Object for holding all data about a game."""


    i_was_white: bool
    did_i_win : bool
    opponent_elo : float
    date : dict
    ending_tag : str



    def __init__(self, game_data : str):
        """Initializer intended to be initialized with chess data from Chess.com"""

        formatted_game_data : list = split_string_list([game_data], '[', ']')


        #Generate the list of game moves using base class init.
        super().__init__(*formatted_game_data)



        #Find strings with relevant data.
        termination_phrase : str = next(phrase for phrase in formatted_game_data if 'Termination' in phrase)
        date_phrase : str = next(phrase for phrase in formatted_game_data if 'Date' in phrase)
        white_player_phrases : str = [phrase for phrase in formatted_game_data if 'White' in phrase]
        black_player_phrases : str = [phrase for phrase in formatted_game_data if 'Black' in phrase]


        #My name will appear in the white player phrases if I was white.
        self.i_was_white = 'TheRealYzb25' in ''.join(white_player_phrases)


        #Find my opponent's ELO in the phrase I wasn't in. It must appear in quotation marks immediately after an ELO tag.
        if self.i_was_white:
            black_data : list = split_string_list(black_player_phrases, '"')
            elo_tag_index : int = next(i for i in range(len(black_data)) if 'Elo' in black_data[i])
            self.opponent_elo = float(black_data[elo_tag_index + 1])

        else:
            white_data : list = split_string_list(white_player_phrases, '"')
            elo_tag_index : int = next(i for i in range(len(white_data)) if 'Elo' in white_data[i])
            self.opponent_elo = float(white_data[elo_tag_index + 1])


        #My name will appear in the termination phrase if I won.
        self.did_i_win = 'TheRealYzb25' in termination_phrase


        #Look for details about how the game ended in the termination phrase.
        if 'drawn' in termination_phrase:
            self.ending_tag = 'draw'

        elif 'time' in termination_phrase:
            self.ending_tag = 'time'

        elif 'checkmate' in termination_phrase:
            self.ending_tag = 'checkmate'

        else:
            self.ending_tag = 'resignation'
        

        #Derive date details from date data. The details must appear immediately after a date tag.
        date_data : list = split_string_list([date_phrase], '"')
        date_tag_index : int = next(i for i in range(len(date_data)) if '' in date_data[i])
        final_date_data = date_data[date_tag_index + 1].split('.')

        self.date = dict()
        self.date['Year'] = final_date_data[0]
        self.date['Month'] = final_date_data[1]
        self.date['Day'] = final_date_data[2]





class Node:

    node_origin : Chess_moves

    #game_number : int
    #win_loss: float
    #avg_opponent_elo : float
    #responses : list

    node_data : list




class decision_tree:

    tree_struct : dict



    def search_for_game(self, game : str) -> list:
        pass




    def search_for_formatted_game(self, formatted_game : list) -> list:

        for move_number in formatted_game:
            pass



if __name__ == '__main__':
    
    chess_data = '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2022.11.06"]
    [Round "?"]
    [White "209joey"]
    [Black "TheRealYzb25"]
    [Result "0-1"]
    [ECO "A00"]
    [WhiteElo "533"]
    [BlackElo "706"]
    [TimeControl "600"]
    [EndTime "11:53:54 PST"]
    [Termination "TheRealYzb25 won by checkmate"]

    1. g4 e5 2. Bg2 Bb4 3. Nc3 Nf6 4. a3 Ba5 5. g5 Ng4 6. f3 Qxg5 7. fxg4 Qxg4 8. h3
    Qxg2 9. Rh2 Qxg1# 0-1'''

    game = Chess_game(chess_data)

    print(chess_data)
    print(game.i_was_white)
    print(game.did_i_win)
    print(game.ending_tag)
    print(game.date)
    print(game.list_of_moves)

