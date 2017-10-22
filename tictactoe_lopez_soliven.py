#!/usr/bin/env python3

'''
    LOPEZ, LUIS ENRICO D.
    SOLIVEN, ADRIENNE FRANCESCA O.
    INTESYS S18

    A tic-tac-toe bot utilizing the Minimax algorithm
    with alpha-beta pruning.
        User given three options:
        1. Simulate game between two Minimax bots.
        2. Simulate game between one Minimax and one random bot.
        3. Play against a Minimax bot.
'''

import random

class State:
    # Horizontal and vertical win lines on the board.
    hvlines = ((0,1,2),(3,4,5),(6,7,8),\
                (0,3,6),(1,4,7),(2,5,8))
    # Diagonal win lines on the board.
    dlines = ((0,4,8),(2,4,6))

    def __init__(self):
        self.board = [' ' for x in range(9)]

    # Returns a clone of the State object.
    def clone(self):
        nb = State()
        for i in range(len(nb.board)):
            nb.board[i] = self.board[i]
        return nb

    def currPiece(self, xTurn):
        return (lambda x : 'x' if x==True else 'o')(xTurn)

    def freeSpaces(self):
        return [i for i in range(len(self.board)) if self.board[i] == ' ']

    '''
    Returns representation of game result as a string.
        'x': x wins
        'o': o wins
        'xo': draw
        ' ': game not done yet
    '''
    def winner(self):
        for combo in State.hvlines + State.dlines:
            if len(set([self.board[x] for x in combo])) == 1 and self.board[combo[0]] != ' ':
                return self.board[combo[0]]
        if self.freeSpaces() == []:
            return 'xo'
        else:
            return ' '

    # Returns result message based on return value of winner().
    def resultMessage(self):
        resultDict = {'x':"X wins!", 'o':"O wins!", \
            'xo':"It's a draw!", ' ':"Game isn't over yet!"}
        return resultDict[self.winner()]

    '''
    Returns local score of:
        x if xTurn == True
        o otherwise
    Diagonal lines are given more priority than horizontal/vertical.
    Blocking opponent is given a higher score, while allowing an opponent
        a win line on the next turn is given lower score.
    Attempting to complete a line (2 pieces on one line) is also given
        higher score.
    '''
    def score(self, xTurn):
        def count(lineSet, multiplier):
            count = 0
            for combo in lineSet:
                plr = 0
                opp = 0
                for index in combo:
                    if self.board[index] == self.currPiece(xTurn):
                        plr+=1
                    elif self.board[index] != ' ':
                        opp+=1
                count += check(plr, opp, multiplier)
            return count
        def check(plr, opp, multiplier):
            score = 0
            if plr == 3:
                score += 100
            elif opp == 3:
                score += -100
            elif plr == 2 and opp == 0:
                score += 2*multiplier
            elif plr == 0 and opp == 2:
                score += -3*multiplier
            elif plr == 1 and opp == 2:
                score += 3*multiplier
            elif plr == 1 and opp == 0:
                score += 1*multiplier
            return score
        score = 0
        score += count(State.hvlines, 1)
        score += count(State.dlines, 2)
        if xTurn:
            return score
        else:
            return -score

    '''
    Returns list of next states. xTurn's value determines whose turn is
        considered (x or o).
    '''
    def nextStates(self, xTurn):
        ns = []
        for i in self.freeSpaces():
            tmp = self.clone()
            tmp.board[i] = self.currPiece(xTurn)
            ns.append(tmp)
        return ns

    # The minimax function with a-b pruning implemented.
    def minimax(self, xTurn, depth, a, b):
        children = self.nextStates(xTurn)
        scores = []
        if children == [] or depth == 0:
            return (self, self.score(xTurn))
        for c in children:
            cs = c.score(xTurn) + c.minimax(not xTurn, depth-1, a, b)[1]
            if xTurn and cs >= b or not xTurn and cs <= a:
                return (c, cs)
            else:
                scores.append(cs)
            if xTurn:
                a = max(a, cs)
            else:
                b = min(b, cs)
            
        if xTurn:
            bestIndex = scores.index(max(scores))
        else:
            bestIndex = scores.index(min(scores))
        return (children[bestIndex], scores[bestIndex])

    '''
    Returns a random next state. New placement is determined by xTurn and
        chosen from list of free spaces on the board.
    If the board is full, return the current state itself.
    '''
    def randomChild(self, xTurn):
        fs = self.freeSpaces()
        if fs != []:
            rc = self.clone()
            rc.board[random.choice(fs)] = self.currPiece(xTurn)
            return rc
        return self

    
    '''
    Returns a next state. New placement is determined by xTurn and
        a manually input index (taken as parameter).
    If the index is invalid, return the current state itself.
    '''
    def manualChild(self, xTurn, index):
        try:
            index = int(index)
        except (NameError, ValueError):
            print('Not an integer!')
            return self
        if index in self.freeSpaces():
            mc = self.clone()
            mc.board[index] = self.currPiece(xTurn)
            return mc
        else:
            print('Invalid tile!')
            return self

    # Displays the board.
    def display(self):
        for i in range(len(self.board)):
            print(self.board[i], end='')
            if (i+1)%3 == 0: print('')
        print('')

# Displays menu and takes input for start() function.
def menu():
    print('1: MINIMAX VS. MINIMAX\n' + \
        '2: MINIMAX VS. RANDOM\n' + \
        '3: MINIMAX VS. USER INPUT\n' + \
        '4: EXIT')
    mode = input('> ')
    if mode in ('1','2','3'):
        start(int(mode))
    elif mode == '4':
        return False
    else:
        print('Invalid entry!')
    return True

'''
Starts simulation.
    1. Minimax vs. Minimax
    2. Minimax vs. Random
    3. Minimax vs. User
'''
def start(mode=1):
    currState = State()
    turn = True

    if mode == 1:
        while (currState.winner() == ' '):
            currState = currState.minimax(turn, 3, -1000, 1000)[0]
            currState.display()
            turn = not turn
    elif mode == 2:
        print('Note: Minimax bot is X')
        while (currState.winner() == ' '):
            if turn:
                currState = currState.minimax(turn, 3, -1000, 1000)[0]
            else:
                currState = currState.randomChild(turn)
            currState.display()
            turn = not turn
    elif mode == 3:
        print('Note: Minimax bot is X')
        while (currState.winner() == ' '):
            if turn:
                currState = currState.minimax(turn, 3, -1000, 1000)[0]
            else:
                newcs = currState.manualChild(turn, \
                    input('Enter tile to place on (0-8): '))
                while newcs == currState:
                    newcs = currState.manualChild(turn, \
                        input('Enter tile to place on (0-8): '))
                currState = newcs
            currState.display()
            turn = not turn
        
    print('Result: ' + currState.resultMessage())   

random.seed()

print('='*10 + 'TIC-TAC-TOE (WITH MINIMAX!)' + '='*10)

while (menu()):
    pass
