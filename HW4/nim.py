## Name : Akshay Peshave
## Campus ID: DA74652
## Homework 4

#! /usr/bin/python

""" A program to play Nim with any number of heaps that uses the AIMA
Python games.py framework."""

from games import *
from utils import infinity, Struct
import sys

class Nim(Game):

    """ Nim is a two player game where the players are identified as 1
    and 2.  Player 1 is first to move. The state of the game is a
    class instance with two attributes: to_move (the player whose turn
    it is to move) and board (a Python data structure representing how
    many heaps there are and how many objects are in each)."""

    def __init__(self, heaps):

        ##heaps given at command prompt is of the form [Heap1,Heap2,....,HeapN]
        ##where Heaps(i) gives the number of items in the i'th heap
        self.initial = Struct(to_move='P1', board=heaps)
    
    def legal_moves(self, state):
        """ Given a state, return a list of legal moves.  How you
        represent a move is up to you and will depend on how you
        represent the board"""

        ##a legal move is the new configuration of the heaps
        ##after some items have been taken away by the player
        legal_moves = []
        for heap in range(0,len(state.board)):
            if(state.board[heap] >0): ##if heap has items
                for items_to_remove in range(1,state.board[heap]+1):
                    heaps_after_move = state.board[:]
                    heaps_after_move[heap] = heaps_after_move[heap] - items_to_remove
                    legal_moves.append(heaps_after_move)
            
        return legal_moves        

    def make_move(self, move, state):
        """Given a move and a state, returns a representation of the
        new state that results after making the move."""

        ## return the same state if the move suggested is not part of the legal moves for the state
        if move not in self.legal_moves(state):
            return state

        
        return Struct(to_move=if_(state.to_move=='P1','P2','P1'), board=move)    

    def terminal_test(self, state):
        """ Returns True iff state is a terman state, i.e., one in
        which no moves are possible."""

        ##if an un-empty heap exists then state is not terminal
        for heap in state.board:
            if heap>0:
                return False

        return True
 

    def utility(self, state, player):
        """ Given a state, returns a a number representing the state's
        utility w.r.t. player. This could be as simple as +infinity if
        it is a win for the player and -infinity if it is a win for
        the player's oponent and 0 if it is not a terminal state.  A
        better utility function would assign intermediate values for
        non-terminal states."""

        ## if player 1 wins the utility is 100
        ## if player 2 wins the utility is -100
        ## for all other non-leaf nodes the utility is 0
        
        if self.terminal_test(state):
            return if_( player == state.to_move , -100 , 100)

        return 0
                   

def query_player(game, state):
    """Make a move by querying standard input.  You will have to get a
    string as input and then twnsform it into the Python object that
    represents the mve.  You should probably conform that the result
    is a legal move using the legal_move method."""
    # game.display(state)
    while True:
        m = eval(raw_input('Your move? '))        
        if m in game.legal_moves(state):
            return m
        else:
            print "I'm sorry, Dave. I'm afraid I can't do that."

# PLAYERS is a dictionary mapping player names to the python functions
# that implement them.

PLAYER = {'me':query_player, 'random':random_player}

def make_alphabeta_player(N):
    """ returns a player function that uses alpha_beta search to depth N """
    return lambda game, state: alphabeta_search(state, game,d=N)

# add to the PLAYER dictionary player function named ab1,ab2,...ab20
# that use alpha_beta search with depth cutoffs between 1 and 20
 
for i in range(20):
    PLAYER['ab'+str(i)] = make_alphabeta_player(i)

def main(initial_state, player1, player2):
    """ Called if the file is invoked from the command line. """
    game = Nim(initial_state)
    result = play_game(game, True, player1, player2)
    if result == 100:
        print 'Player 1 wins'
    elif result == -100:
        print 'Player 2 wins'
    else:
        print 'No one wins?!?'

# if called from the command line, invoke main using the optional
# arguments for the intial and goal states if provided

if __name__ == "__main__":
    # 1st command line arg is always the command name (e.g., nim.py)
    nargs = len(sys.argv)
    args = sys.argv
    if nargs < 2 or nargs > 4:
        print "Usage: python nim.py initial [player1 player2]]"
        print "  where initial is a string representing the initial board (e.g., [5,4,3]) and\n  player1 and player 2 can be any of of: me, random, ab1, ab2 ... ab20 and default to random."
        sys.exit()
    # Assume the board representation is a Python expression, so eval the string argument
    initial_state = eval(args[1])
    print initial_state
    # defaults
    player1 = player2 = random_player
    if nargs > 2:
        try:
            player1 = PLAYER[args[2]]
        except:
            print "I don't know what kind of player", args[2], "is"
            exit()
    if nargs > 3:
        try:
            player2 = PLAYER[args[3]]
        except:
            print "I don't know what kind of player", args[3], "is"
            exit()
    main(initial_state, player1, player2)
