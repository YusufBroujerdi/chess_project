import pickle
import collections.abc
import datetime
import metadata





def check_is_move(move : str) -> bool:
    """Performs rudimentary checks on string to ensure it looks like a valid chess move in the PGN.
    
    Warning: This function may yield false positives."""

    #Check to see if the move has enough characters to constitute a move.
    if len(move) < 2:
        return False
    
    #A separate check to see if the move describes castling.
    if move == 'O-O-O' or move == 'O-O':
        return True

    #Check if the front starts with a valid piece (i.e. queen, king, pawn, etc.). This check also filters out lists.
    if ord(move[0]) not in range(97, 105) and move[0] not in {'Q', 'K', 'B', 'N', 'R'}:
        return False

    #Take out notation for captures, checks and checkmates.
    move = ''.join( [char for char in move if char not in {'#', '+'}] )

    #Check if the back ends with a valid coordinate (i.e. 'h2', 'a4', etc.).
    if ord(move[-2]) not in range(97, 105) or ord(move[-1]) not in range(49, 57):
        return False
    
    return True



def check_is_move_and_warn(move : str) -> bool:
    """Performs rudimentary checks on string to ensure it looks like a valid chess move in the PGN. Warns if it is not.
    
    Warning: This function may yield false positives."""

    result = check_is_move(move)

    if not result:
        print(f'Move {move} is not a valid move format.')

    return result



def split_string_list(string_list : list, *separators):
    """Splits a list of strings into a larger list of strings using the given separators."""

    #Takes a list of strings and returns a list of lists, where each list is a string split by a given separator.
    list_split_before_flattening = lambda l, separator : [element.split(separator) for element in l]

    #Flattens a list of lists.
    flatten = lambda l : [subelement for element in l for subelement in element]

    #Splits a list of strings into a larger list of strings using the given separator.
    lsplit = lambda l, separator : flatten(list_split_before_flattening(l, separator))

    for separator in separators:
        string_list = lsplit(string_list, separator)
    
    return string_list





class Chess_moves(collections.abc.MutableSequence):
    """Object for holding and manipulating sequences of chess moves."""

    list_of_moves = []

    
    def __init__(self, *moves_in_algebraic_notation : str):
        """Initializer can be initialized with one string of moves or multiple. Initializer can directly accept strings of unformatted PGN from Chess.com."""

        formatted_move_sequence : list = split_string_list(moves_in_algebraic_notation, ',', ' ', '\n', '\r')
        self.list_of_moves = [move for move in formatted_move_sequence if check_is_move(move)]


    
    def __getitem__(self, key):
        """Extends standard list behaviour to Chess_moves."""

        #If key is numeric, subscribing the list should yield a single move, necessitating the substitution of a single argument into the Chess_moves initializer.
        try:
            assert(check_is_move(self.list_of_moves[key]))
            return self.list_of_moves[key]
        
        #Otherwise, the key is a slice. And the list will yield multiple moves for multiple arguments.
        except:
            return Chess_moves(*self.list_of_moves[key])



    def __setitem__(self, key, value):
        """Extends standard list behaviour to Chess_moves."""

        #If the value is multiple moves, a check will need to be performed on each move to ensure it's formatted.
        if not hasattr(value, '__iter__'):
            if check_is_move_and_warn(value):
                self.list_of_moves[key] = value
                
        else:
            if all(check_is_move_and_warn(move) for move in value):
                self.list_of_moves[key] = value


    
    def __delitem__(self, key):
        """Extends standard list behaviour to Chess_moves."""

        del self.list_of_moves[key]



    def __len__(self):
        """Extends standard list behaviour to Chess_moves."""

        return len(self.list_of_moves)
    


    def insert(self, index, value):

        if check_is_move_and_warn(value):
            self.list_of_moves.insert(index, value)
    


    def __eq__(self, other):
        
        try:
            assert(len(other) == len(self))

            for move_num in range(len(other)):
                assert(self[move_num] == other[move_num])

            return True

        except:
            return False



    def __str__(self):
        """Ensures print and other str operations return the moves rather than the memory address."""

        #Separate case for empty list
        if self.list_of_moves == []: return ('1. ')

        #Split the moves into white moves and black moves then combine them by turn.
        white, black = self.list_of_moves[0::2], self.list_of_moves[1::2]
        turns = [f'{white[turn]} ' + f'{black[turn]}' if turn < len(black) \
                 else f'{white[turn]}' for turn in range(len(white))]
        
        #Add numbering to the start of turns.
        formatted_turns = ' '.join( [f'{turn + 1}. {turns[turn]}' for turn in range(len(turns))] )
        return(formatted_turns)



    def __hash__(self):
        return hash(tuple(self.list_of_moves))


    
    def add_move(self, *moves : str):
        """Adds moves specified in the argument."""

        for move in moves:

            if not check_is_move_and_warn(move):
                return
            
            self.list_of_moves.append(move)





class Log():
    """Object for holding a log entry on a specific date."""

    entry : dict


    def __init__(self, note : str):

        self.entry = dict()

        self.entry['date'] = datetime.datetime.now().date()
        self.entry['content'] = note
    


    def __str__(self):

        return f'''Date/time of entry: {self.entry['date']}

{self.entry['content']}'''





class Annotation(Chess_moves):
    """Object for holding notes about a particular sequence of chess moves."""

    notes : list


    def __init__(self, moves_to_annotate : Chess_moves):

        super().__init__(moves_to_annotate)
        self.notes = []
    


    def __str__(self):

        output = ''

        for note in self.notes:

            output += f'{str(note)} \n\n'



    def add_note(self, note : str):

        if self.notes[-1].entry['date'] == datetime.datetime.now().date():
            self.notes[-1].entry['content'] += '\n\n' + note

        else:
            self.notes.append(Log(note))





class Book(collections.abc.MutableMapping):
    """Object for holding notes about arbitrary sequences of chess moves."""

    name : str
    annotations : dict


    def __init__(self, name):

        self.name = name
    


    def __getitem__(self, key : Chess_moves):

        try:

            if any(not check_is_move_and_warn(move) for move in key):
                return
            
            if key in self.annotations.keys():
                return self.annotations[key]
            
            else:
                self.annotations[key] = []
                return self.annotations[key]

        except:
            print("key not iterable sequence of moves.")



    def __setitem__(self, key : Chess_moves, value):
        
        try:
            if any(not check_is_move_and_warn(move) for move in key):
                return
            self.annotations[key] = value

        except:
            print("key not iterable sequence of moves.")



    def __delitem__(self, key : Chess_moves):
        
        del self.annotations[key]



    def __iter__(self):
        
        return iter(self.annotations)
    


    def __len__(self):
        
        return len(self.annotations)





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
        date_tag_index : int = next(i for i in range(len(date_data)) if 'Date' in date_data[i])
        final_date_data = date_data[date_tag_index + 1].split('.')

        self.date = dict()
        self.date['Year'], self.date['Month'], self.date['Day'] = final_date_data[0], final_date_data[1], final_date_data[2]



    def __str__(self):

        my_colour = 'White' if self.i_was_white else 'Black'
        win_state = 'victory' if self.did_i_win else 'defeat'
        game_summary = 'was drawn' if self.ending_tag == 'drawn' else \
            f'ended in {win_state} by {self.ending_tag}'
        moves = super().__str__()

        output : str =  f'''{self.date['Day']}/{self.date['Month']}/{self.date['Year']}
Game as {my_colour} {game_summary}. Opponent ELO was {self.opponent_elo}
Move details:
{moves}'''

        return output





class Line_space(collections.abc.MutableSet):
    """Object for holding data about preferred chess lines."""


    name : str
    is_white : bool
    lines : set


    def __init__(self, name, is_white, lines):

        self.name = name
        self.is_white = is_white

        #For any line in the line space, all its sub-lines should also be present.
        take_sub_lines = lambda line : { line[:n] for n in range(len(line) + 1) }
        self.lines = set.union( *(take_sub_lines(line) for line in lines) )



    def is_your_move(self, move_number : int):
        """Verifies if it is our move based on move number our colour."""
        
        #If move_number is even, it is black's turn.
        return (move_number % 2) != self.is_white
    


    def filter_for_length(self, length : int):

        return {line[:length] for line in self.lines if len(line) >= length}
    


    def __contains__(self, line):
        """Extends standard set behaviour to Line_space."""

        return True if line in self.lines else False
    


    def __iter__(self):
        """Extends standard set behaviour to Line_space."""
        
        return iter(self.lines)
    


    def __len__(self):
        """Extends standard set behaviour to Line_space."""
        
        return len(self.lines)
    


    def add(self, line):
        """Extends standard set behaviour to Line_space."""
        
        #Ensure all sublines of the added line are also added.
        take_sub_lines = lambda line : { line[:n] for n in range(len(line) + 1) }
        self.lines |= take_sub_lines(line)



    def discard(self, line_to_discard):
        """Extends standard set behaviour to Line_space."""

        #Discard any lines for which the discarded line is a subline.
        condition = lambda line : line[ : len(line_to_discard) ] != line_to_discard
        self.lines = {line for line in self.lines if not condition}
    




class Unique_line_space(Line_space):
    """Object for holding data about preferred chess line, but a single unique response to each opponent move is necessitated, for moves greater than a certain "uniqueness_number"."""

    u_num : int

    def __init__(self, name, is_white, lines, uniqueness_number):
        
        super().__init__(name, is_white, lines)
        self.u_num = uniqueness_number

        uniqueness_iter = iter(line for line in super().lines if not self.check_uniqueness(line))

        while True:

            try: super().discard(next(uniqueness_iter))
            except: break



    def add(self, line):

        super().add(line)
        uniqueness_iter = next(l for l in super().lines if not self.check_uniqueness(l) and l != line)

        while True:

            try: super().discard(uniqueness_iter)
            except: break
    


    def check_uniqueness(self, line):

        uniqueness_is_needed = lambda num : divmod(num, 2)[0] + 1 >= self.u_num
        is_opponent_turn = lambda num : not super().is_your_turn(num)

        for move_num in range(len(line)):
            if uniqueness_is_needed(move_num) and is_opponent_turn(move_num):
                if len({l for l in super().lines if len(l) == move_num + 1 and l[:move_num] == line}) > 1:
                    return False
        
        return True





class Data_tree:

    books : dict
    games : dict
    line_spaces : dict





class Node(Data_tree):

    address : Chess_moves


    def __init__(self, data):
        
        self.data = data



    def __getitem__(self, key):

        if key == '..':
            del self.address[-1]

        else:
            self.address.add_move(key)
    


    def travel(self, *keys):

        for key in keys:
            self[key]





class Node_traverser:

    node : Node


    def __init__(self, data):

        self.node = Node(data)

        print('Program start. \n\n')

        self.loop_menu()

    

    def loop_menu(self):

        menu_options = metadata.menu_options

        while True:

            for option in menu_options.keys():
                print(f'Enter {option} to {menu_options[option]}.\n\n')

            response = input()

            match response:

                case 1:
                    self.configure_line_space()

                case 2:
                    self.configure_book()

                case 3:
                    self.navigate_to_new()

                case _:
                    print('Input not recognized. Enter a number for the corresponding option.\n\n')
                    continue
    
    

    def configure_line_space(self):
        pass


    def configure_book(self):
        pass


    def navigate_to_new(self):
        pass





            






if __name__ == '__main__':
    

    # games = []

    # for data_point in metadata.chess_data:
    #     games.append(Chess_game(data_point))
    
    # for game in games:
    #     print(game)
    
    # myspace = Line_space('test', True, games)

    # x = Chess_moves('1. d4 d5 2. c4 e6 3. cxd5 exd5 4. a3 Nf6 5. Bg5 Be7 6. Bxf6 Bxf6 7. Nc3 O-O')
    # print(x)
    # myspace.add(x)

    # for line in myspace:
    #     print(line)

    myset = set()

    x = Chess_game('''[Event "Live Chess"]
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
    Qxg2 9. Rh2 Qxg1# 0-1''')

    y = Chess_moves('1. g4 e5 2. Bg2 Bb4 3. Nc3 Nf6 4. a3 Ba5 5. g5 Ng4 6. f3 Qxg5 7. fxg4 Qxg4 8. h3 Qxg2 9. Rh2 Qxg1#')

    myset.add(x)

    myset.add(y)

    print(x == y)
    print(len(myset))
    

